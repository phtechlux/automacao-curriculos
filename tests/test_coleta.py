import base64

from curriculos.coleta import coletar
from curriculos.coleta.descricao import extrair_descricao
from curriculos.coleta.gmail import corpo_html
from curriculos.coleta.modelo import Vaga
from curriculos.coleta.parsers import extrair_vagas, fonte_do_remetente

LINKEDIN = """
<table><tr><td>
  <a href="https://www.linkedin.com/comm/jobs/view/123456/?trk=x">Senior Python Developer</a>
  <p>Acme Corp · Remote</p>
</td></tr><tr><td>
  <a href="https://www.linkedin.com/comm/jobs/view/123456/?trk=y">Senior Python Developer</a>
</td></tr><tr><td>
  <a href="https://www.linkedin.com/jobs/view/999/">Data Engineer</a>
  <p>Globex</p><p>Lisbon, Portugal</p>
</td></tr>
<a href="https://www.linkedin.com/help">Ajuda</a></table>
"""


def test_linkedin_extrai_e_deduplica():
    vagas = extrair_vagas(LINKEDIN, "linkedin")
    assert [(v.titulo, v.empresa, v.local) for v in vagas] == [
        ("Senior Python Developer", "Acme Corp", "Remote"),
        ("Data Engineer", "Globex", "Lisbon, Portugal"),
    ]
    assert vagas[0].link == "https://www.linkedin.com/jobs/view/123456/"


def test_indeed():
    html = '<div><a href="https://br.indeed.com/rc/clk?jk=abc">Backend Dev</a><span>Foo Ltd - Remoto</span></div>'
    (v,) = extrair_vagas(html, "indeed")
    assert (v.titulo, v.empresa, v.local) == ("Backend Dev", "Foo Ltd", "Remoto")


def test_fonte_do_remetente():
    assert fonte_do_remetente("LinkedIn <jobalerts-noreply@linkedin.com>") == "linkedin"
    assert fonte_do_remetente("x@outro.com") is None


def test_descricao_e_bloqueio():
    texto = "Requisitos " * 40
    assert extrair_descricao(f'<div id="jobDescriptionText">{texto}</div>').startswith("Requisitos")
    assert extrair_descricao("<title>Just a moment...</title>") is None


def test_corpo_html_multipart():
    b64 = lambda s: base64.urlsafe_b64encode(s.encode()).decode()
    payload = {"mimeType": "multipart/alternative", "parts": [
        {"mimeType": "text/plain", "body": {"data": b64("texto")}},
        {"mimeType": "text/html", "body": {"data": b64("<b>html</b>")}},
    ]}
    assert corpo_html(payload) == "<b>html</b>"


def test_coletar_salva_e_pula(tmp_path, monkeypatch):
    import curriculos.coleta.gmail as gmail
    monkeypatch.setattr(gmail, "buscar_alertas", lambda svc, dias: iter([("jobs@linkedin.com", "", LINKEDIN)]))
    buscar = lambda link: "desc" if "123456" in link else None  # segunda vaga "bloqueada"
    novas = coletar(None, pasta=tmp_path, buscar=buscar)
    assert len(novas) == 1
    assert Vaga.carregar(next(tmp_path.glob("*.json"))).descricao == "desc"
    assert coletar(None, pasta=tmp_path, buscar=buscar) == []  # já coletada
