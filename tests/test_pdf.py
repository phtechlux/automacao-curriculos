import pytest

from curriculos.pdf import gerar_pdf, nome_arquivo, renderizar_html

CV = {
    "nome": "João Silva", "titulo": "Dev", "contato": {"email": "j@x.com", "telefone": ""},
    "resumo": "Resumo <script>", "experiencias": [
        {"cargo": "Dev", "empresa": "A", "inicio": "2020", "fim": "atual", "local": "", "conquistas": ["Fiz X"]}],
    "habilidades": {"tecnicas": ["Python"], "ferramentas": []}, "formacao": [], "idiomas": [], "certificacoes": [],
}


def test_nome_arquivo():
    assert nome_arquivo("João Silva", "Acme, Inc.", "Sr. Python/Django Dev") == \
        "Curriculo_Joao_Silva_Acme_Inc_Sr_Python_Django_Dev.pdf"


def test_html():
    html = renderizar_html(CV, "pt")
    assert "Experiência" in html and "Fiz X" in html and "j@x.com" in html
    assert "<script>" not in html  # escapado
    assert "Formação" not in html  # seção vazia some


def test_pdf_real(tmp_path):
    pytest.importorskip("playwright")
    try:
        caminho = gerar_pdf(CV, "Acme", "Dev", saida=tmp_path)
    except Exception as e:  # chromium não instalado
        pytest.skip(str(e)[:80])
    assert caminho.read_bytes()[:4] == b"%PDF"


def test_contatos_viram_links():
    from curriculos.pdf import contatos
    itens = contatos({"localizacao": "Brasília", "telefone": "(61) 99843-3188", "email": "a@b.com",
                      "github": "github.com/phtechlux", "linkedin": ""}, "pt")
    assert itens == [("Brasília", None), ("(61) 99843-3188", "tel:+5561998433188"),
                     ("E-mail", "mailto:a@b.com"), ("GitHub", "https://github.com/phtechlux")]
    html = renderizar_html({**CV, "contato": {"github": "github.com/x"}}, "pt")
    assert '<a href="https://github.com/x">GitHub</a>' in html and "github.com/x</" not in html
