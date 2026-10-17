"""Busca a descrição na página da vaga. Se o site bloquear, devolve None e a vaga é pulada."""
import urllib.error
import urllib.request

from bs4 import BeautifulSoup

SELETORES = [
    ".show-more-less-html__markup",  # LinkedIn público
    "#jobDescriptionText",  # Indeed
    "[class*=description]",
    "main",
]
SINAIS_BLOQUEIO = ("cf-challenge", "captcha", "just a moment", "access denied", "authwall")


def bloqueado(html: str) -> bool:
    baixo = html.lower()
    return any(s in baixo for s in SINAIS_BLOQUEIO)


def extrair_descricao(html: str) -> str | None:
    if bloqueado(html):
        return None
    soup = BeautifulSoup(html, "html.parser")
    for sel in SELETORES:
        if (el := soup.select_one(sel)) and len(texto := el.get_text("\n", strip=True)) > 200:
            return texto
    return None


def buscar_descricao(link: str, timeout: int = 15) -> str | None:
    req = urllib.request.Request(link, headers={"User-Agent": "Mozilla/5.0", "Accept-Language": "en,pt"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            html = r.read().decode("utf-8", errors="replace")
    except (urllib.error.URLError, TimeoutError):
        return None  # 403/429/rede: pula, sem retry agressivo
    return extrair_descricao(html)
