import json
import threading
import urllib.error
import urllib.request
from http.server import ThreadingHTTPServer

import pytest

from curriculos import painel
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


def post(url, corpo):
    req = urllib.request.Request(url, json.dumps(corpo).encode(), {"Content-Type": "application/json"})
    return json.loads(urllib.request.urlopen(req).read())


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
