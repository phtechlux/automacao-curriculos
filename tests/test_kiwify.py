import pytest

from curriculos import contas, kiwify


@pytest.fixture(autouse=True)
def isolado(tmp_path, monkeypatch):
    monkeypatch.setattr(contas, "RAIZ", tmp_path)
    monkeypatch.setattr(kiwify, "SEGREDO", "s3gredo")
    monkeypatch.setattr(kiwify, "CREDITOS_PADRAO", 10)


def test_validar_segredo():
    kiwify.validar_segredo("s3gredo")
    with pytest.raises(kiwify.WebhookInvalido):
        kiwify.validar_segredo("errado")
    with pytest.raises(kiwify.WebhookInvalido):
        kiwify.validar_segredo("")


def test_processar_cria_conta_e_credita_de_novo_na_recompra():
    r1 = kiwify.processar({"order_status": "paid", "Customer": {"email": "x@y.com"}})
    assert r1["creditos"] == 10
    r2 = kiwify.processar({"order_status": "paid", "customer": {"email": "x@y.com"}})
    assert r2["token"] == r1["token"]
    assert r2["creditos"] == 20


def test_processar_ignora_status_nao_pago():
    assert kiwify.processar({"status": "pending"})["ignorado"] == "pending"


def test_processar_sem_email_falha():
    with pytest.raises(kiwify.WebhookInvalido):
        kiwify.processar({"order_status": "paid"})


def test_processar_payload_com_formato_inesperado_nao_quebra():
    # "product" e "customer" em formato diferente do esperado não devem derrubar o webhook
    r = kiwify.processar({"order_status": "paid", "customer": "nao-e-dict", "email": "a@a.com", "product": "x"})
    assert r["creditos"] == 10
