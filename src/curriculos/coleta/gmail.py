import base64
import os
from pathlib import Path

SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.compose",  # rascunhos (Fase 4)
]
QUERY = "from:(linkedin.com OR indeed.com OR vanhack.com OR turing.com) newer_than:{dias}d"


def servico():
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build

    token = Path(os.getenv("GMAIL_TOKEN_PATH", "token.json"))
    creds = Credentials.from_authorized_user_file(token, SCOPES) if token.exists() else None
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                os.getenv("GMAIL_CREDENTIALS_PATH", "credentials.json"), SCOPES
            )
            creds = flow.run_local_server(port=0)
        token.write_text(creds.to_json(), encoding="utf-8")
    return build("gmail", "v1", credentials=creds)


def corpo_html(payload: dict) -> str:
    """Percorre as partes MIME e devolve o text/html (ou text/plain como fallback)."""
    achados = {}

    def visitar(parte):
        tipo = parte.get("mimeType", "")
        dados = parte.get("body", {}).get("data")
        if dados and tipo in ("text/html", "text/plain"):
            achados.setdefault(tipo, base64.urlsafe_b64decode(dados).decode("utf-8", errors="replace"))
        for p in parte.get("parts", []):
            visitar(p)

    visitar(payload)
    return achados.get("text/html") or achados.get("text/plain", "")


def buscar_alertas(svc, dias: int = 2):
    """Gera (remetente, assunto, html) de cada alerta."""
    req = svc.users().messages().list(userId="me", q=QUERY.format(dias=dias))
    while req is not None:
        resp = req.execute()
        for m in resp.get("messages", []):
            msg = svc.users().messages().get(userId="me", id=m["id"], format="full").execute()
            cab = {h["name"].lower(): h["value"] for h in msg["payload"].get("headers", [])}
            yield cab.get("from", ""), cab.get("subject", ""), corpo_html(msg["payload"])
        req = svc.users().messages().list_next(req, resp)
