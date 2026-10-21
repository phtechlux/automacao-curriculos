"""Contas do produto: isola dados por cliente pagante (CTA-01..03).

Sem senha — a chave é um token no link enviado após a compra (ver kiwify.py).
Uso local do Pedro (sem token na URL) continua intacto, usando as pastas padrão."""
import json
import re
import secrets
from dataclasses import dataclass
from pathlib import Path

RAIZ = Path("data/contas")
_TOKEN_OK = re.compile(r"^[A-Za-z0-9_-]{8,64}$")


@dataclass
class Caminhos:
    """Pastas de uma conta — mesma forma que os módulos coleta/ia/pdf já esperam."""
    vagas: Path
    saida: Path
    curriculo: Path


def novo_token() -> str:
    return secrets.token_urlsafe(18)


def _pasta(token: str) -> Path | None:
    if not token or not _TOKEN_OK.match(token):
        return None
    p = RAIZ / token
    return p if p.is_dir() else None


def caminhos(token: str) -> Caminhos | None:
    p = _pasta(token)
    if not p:
        return None
    return Caminhos(vagas=p / "vagas", saida=p / "output", curriculo=p / "curriculo.yaml")


def criar(email: str, creditos: int = 0, token: str | None = None) -> str:
    token = token or novo_token()
    p = RAIZ / token
    (p / "vagas").mkdir(parents=True, exist_ok=True)
    (p / "output").mkdir(parents=True, exist_ok=True)
    salvar(token, {"email": email, "creditos": creditos})
    return token


def carregar(token: str) -> dict | None:
    p = _pasta(token)
    if not p or not (p / "conta.json").exists():
        return None
    return json.loads((p / "conta.json").read_text(encoding="utf-8"))


def salvar(token: str, conta: dict):
    (RAIZ / token / "conta.json").write_text(json.dumps(conta, ensure_ascii=False, indent=2), encoding="utf-8")


def creditar(token: str, quantidade: int) -> dict | None:
    conta = carregar(token)
    if conta is None:
        return None
    conta["creditos"] = conta.get("creditos", 0) + quantidade
    salvar(token, conta)
    return conta


def consumir(token: str) -> bool:
    """COB-02: True se consumiu 1 crédito; False se não havia saldo."""
    conta = carregar(token)
    if not conta or conta.get("creditos", 0) <= 0:
        return False
    conta["creditos"] -= 1
    salvar(token, conta)
    return True


def email_para_token(email: str) -> str | None:
    """Busca o token de uma conta existente pelo e-mail (recompra do mesmo cliente)."""
    if not RAIZ.is_dir():
        return None
    for p in RAIZ.iterdir():
        arq = p / "conta.json"
        if arq.exists():
            try:
                if json.loads(arq.read_text(encoding="utf-8")).get("email") == email:
                    return p.name
            except (json.JSONDecodeError, OSError):
                continue
    return None
