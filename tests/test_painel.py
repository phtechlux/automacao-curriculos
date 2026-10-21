import json
import threading
import urllib.error
import urllib.request
from http.server import ThreadingHTTPServer

import pytest

from curriculos import contas, painel
from curriculos.coleta.modelo import Vaga


@pytest.fixture
def servidor(tmp_path, monkeypatch):
    monkeypatch.setattr(painel, "PASTA_VAGAS", tmp_path)
    v = Vaga(titulo="Dev Web", link="https://x.com/1", fonte="indeed", empresa="Acme")
    v.salvar(tmp_path)
    s = ThreadingHTTPServer(("127.0.0.1", 0), painel.Handler)
    threading.Thread(target=s.serve_forever, daemon=True).start()
    yield f"http://127.0.0.1:{s.server_address[1]}", v, tmp_path
    s.shutdown()


@pytest.fixture
def servidor_conta(tmp_path, monkeypatch):
    monkeypatch.setattr(contas, "RAIZ", tmp_path / "contas")
    monkeypatch.setattr(painel.kiwify, "SEGREDO", "s3gredo")
    token = contas.criar("cliente@x.com", creditos=1)
    s = ThreadingHTTPServer(("127.0.0.1", 0), painel.Handler)
    threading.Thread(target=s.serve_forever, daemon=True).start()
    yield f"http://127.0.0.1:{s.server_address[1]}", token
    s.shutdown()


def post(url, corpo):
    req = urllib.request.Request(url, json.dumps(corpo).encode(), {"Content-Type": "application/json"})
    return json.loads(urllib.request.urlopen(req).read())


def get(url):
    return json.loads(urllib.request.urlopen(url).read())


def test_lista_status_e_descricao(servidor):
    url, v, pasta = servidor
    (item,) = json.loads(urllib.request.urlopen(url + "/api/vagas").read())
    assert item["id"] == v.id and item["status"] == "nova"
    assert post(f"{url}/api/vagas/{v.id}/descricao", {"descricao": " Requisitos: React "})["descricao"] == "Requisitos: React"
    assert post(f"{url}/api/vagas/{v.id}/status", {"status": "descartada"})["status"] == "descartada"
    assert Vaga.carregar(next(pasta.glob("*.json"))).status == "descartada"


def test_gerar_sem_descricao_e_id_invalido(servidor):
    url, v, _ = servidor
    with pytest.raises(urllib.error.HTTPError) as e:
        post(f"{url}/api/vagas/{v.id}/gerar", {})
    assert e.value.code == 400
    with pytest.raises(urllib.error.HTTPError) as e:
        post(f"{url}/api/vagas/..%2F..%2Fx/status", {"status": "nova"})
    assert e.value.code == 404


def test_limitador_bloqueia_apos_o_maximo():
    painel._tentativas.clear()
    chave = "teste:1.2.3.4"
    resultados = [painel._limitar(chave, maximo=5) for _ in range(6)]
    assert resultados == [True, True, True, True, True, False]


def test_entrar_por_email(servidor_conta):
    url, token = servidor_conta
    assert post(f"{url}/api/entrar", {"email": "cliente@x.com"})["token"] == token
    with pytest.raises(urllib.error.HTTPError) as e:
        post(f"{url}/api/entrar", {"email": "nao-e-cliente@x.com"})
    assert e.value.code == 404


def test_conta_isola_curriculo_e_vagas(servidor_conta):
    url, token = servidor_conta
    base = f"{url}/c/{token}"
    assert get(f"{base}/api/vagas") == []
    assert get(f"{base}/api/conta") == {"email": "cliente@x.com", "creditos": 1}

    yaml_texto = "nome: Fulano\nexperiencias: []\n"
    assert post(f"{base}/api/curriculo", {"yaml": yaml_texto}) == {"ok": True}
    assert get(f"{base}/api/curriculo")["yaml"] == yaml_texto

    with pytest.raises(urllib.error.HTTPError):
        post(f"{base}/api/curriculo", {"yaml": "- so uma lista, sem nome"})

    criada = post(f"{base}/api/vagas", {"titulo": "Dev", "empresa": "Acme", "descricao": "..."})
    assert len(get(f"{base}/api/vagas")) == 1

    # conta de outro cliente não vê nada disso (CTA-03)
    outro = contas.criar("outro@x.com", creditos=0)
    assert get(f"{url}/c/{outro}/api/vagas") == []


def test_gerar_sem_credito_responde_402_sem_chamar_ia(servidor_conta):
    url, token = servidor_conta
    base = f"{url}/c/{token}"
    criada = post(f"{base}/api/vagas", {"titulo": "Dev", "empresa": "Acme", "descricao": "bastante texto aqui"})
    assert post(f"{base}/api/vagas/{criada['id']}/status", {"status": "nova"})["status"] == "nova"
    # consome o único crédito direto, sem passar pela IA/PDF
    assert contas.consumir(token) is True
    with pytest.raises(urllib.error.HTTPError) as e:
        post(f"{base}/api/vagas/{criada['id']}/gerar", {})
    assert e.value.code == 402


def test_gerar_com_erro_devolve_credito(servidor_conta, monkeypatch):
    url, token = servidor_conta
    base = f"{url}/c/{token}"
    criada = post(f"{base}/api/vagas", {"titulo": "Dev", "empresa": "Acme", "descricao": "bastante texto aqui"})

    def _falha(*a, **k):
        raise RuntimeError("IA indisponível")

    monkeypatch.setattr(painel, "gerar", _falha)
    with pytest.raises(urllib.error.HTTPError) as e:
        post(f"{base}/api/vagas/{criada['id']}/gerar", {})
    assert e.value.code == 500
    assert get(f"{base}/api/conta")["creditos"] == 1  # não perdeu o crédito na falha


def test_webhook_kiwify_credita_conta(servidor_conta):
    url, token = servidor_conta
    r = post(f"{url}/webhook/kiwify?secret=s3gredo", {"order_status": "paid", "Customer": {"email": "cliente@x.com"}})
    assert r["token"] == token and r["creditos"] == 11  # 1 que já tinha + 10 padrão
    with pytest.raises(urllib.error.HTTPError) as e:
        post(f"{url}/webhook/kiwify?secret=errado", {"order_status": "paid", "Customer": {"email": "cliente@x.com"}})
    assert e.value.code == 400
