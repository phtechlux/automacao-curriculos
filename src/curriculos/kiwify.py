"""Webhook da Kiwify (COB-01): compra aprovada vira créditos na conta do cliente.

A autenticação é um segredo que você mesmo escolhe e coloca na URL configurada no
painel da Kiwify (ex.: https://seuservidor/webhook/kiwify?secret=XYZ) — não depende
de conhecer o esquema de assinatura interno da Kiwify.

ATENÇÃO: os nomes de campo do payload (status, e-mail, id do produto) seguem o
formato mais comum de webhook de checkout: confirme contra um envio real/teste da
Kiwify ao configurar o produto (fica para a Fase 8 de lançamento, não bloqueia o código)."""
import os

from curriculos import contas

SEGREDO = os.getenv("KIWIFY_WEBHOOK_SECRET", "")
CREDITOS_PADRAO = int(os.getenv("KIWIFY_CREDITOS_PADRAO", "10"))
# créditos por produto/oferta específico da Kiwify, se quiser diferenciar planos:
# PLANOS = {"<product_id>": 20}
PLANOS: dict[str, int] = {}


class WebhookInvalido(Exception):
    pass


def validar_segredo(recebido: str):
    if not SEGREDO or recebido != SEGREDO:
        raise WebhookInvalido("segredo do webhook ausente ou incorreto (confira KIWIFY_WEBHOOK_SECRET)")


def processar(corpo: dict) -> dict:
    """Credita a conta do cliente a partir do JSON do webhook (já autenticado por validar_segredo)."""
    status = str(corpo.get("order_status") or corpo.get("status") or corpo.get("event") or "").lower()
    if status not in ("paid", "approved", "order_approved", "completed"):
        return {"ignorado": status or "sem status"}

    cliente = corpo.get("Customer") or corpo.get("customer")
    cliente = cliente if isinstance(cliente, dict) else {}
    email = cliente.get("email") or corpo.get("email")
    if not email:
        raise WebhookInvalido("webhook sem e-mail do cliente")

    produto_obj = corpo.get("product")
    produto_obj = produto_obj if isinstance(produto_obj, dict) else {}
    produto = str(produto_obj.get("product_id") or corpo.get("product_id") or "")
    creditos = PLANOS.get(produto, CREDITOS_PADRAO)

    token = contas.email_para_token(email)
    conta = contas.creditar(token, creditos) if token else None
    if conta is None:
        token = contas.criar(email, creditos)
        conta = contas.carregar(token)
    return {"token": token, "email": email, "creditos": conta["creditos"]}
