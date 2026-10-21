import pytest

from curriculos import contas


@pytest.fixture(autouse=True)
def raiz_isolada(tmp_path, monkeypatch):
    monkeypatch.setattr(contas, "RAIZ", tmp_path)


def test_criar_carregar_creditar_consumir():
    token = contas.criar("a@b.com", creditos=2)
    assert contas.carregar(token) == {"email": "a@b.com", "creditos": 2}
    assert contas.email_para_token("a@b.com") == token
    assert contas.creditar(token, 3)["creditos"] == 5
    assert contas.consumir(token) is True
    assert contas.carregar(token)["creditos"] == 4


def test_consumir_sem_saldo():
    token = contas.criar("sem@credito.com", creditos=0)
    assert contas.consumir(token) is False
    assert contas.carregar(token)["creditos"] == 0


def test_token_invalido_ou_inexistente_nao_atravessa_pastas():
    assert contas.caminhos("../../etc") is None
    assert contas.caminhos("inexistente12345") is None
    assert contas.carregar("tambem-nao-existe-123") is None


def test_email_sem_conta_retorna_none():
    contas.criar("existe@x.com", creditos=1)
    assert contas.email_para_token("naoexiste@x.com") is None
