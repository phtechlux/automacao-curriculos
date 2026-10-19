"""Extrai vagas do HTML dos alertas. Heurístico: links de vaga + texto do bloco vizinho."""
import re
from urllib.parse import urlparse

from bs4 import BeautifulSoup

from .modelo import Vaga

# padrão de link de vaga por fonte
PADROES = {
    "linkedin": re.compile(r"linkedin\.com/(?:comm/)?jobs/view/(\d+)"),
    "indeed": re.compile(r"indeed\.com/(?:rc/clk|viewjob|pagead/clk)"),
    "vanhack": re.compile(r"vanhack\.com/.*jobs?/"),
    "turing": re.compile(r"turing\.com/.*jobs?/"),
}

REMETENTES = {
    "linkedin.com": "linkedin",
    "indeed.com": "indeed",
    "vanhack.com": "vanhack",
    "turing.com": "turing",
}


def fonte_do_remetente(remetente: str) -> str | None:
    remetente = remetente.lower()
    return next((f for dominio, f in REMETENTES.items() if dominio in remetente), None)


def _normalizar_link(link: str, fonte: str) -> str:
    if fonte == "linkedin" and (m := PADROES["linkedin"].search(link)):
        return f"https://www.linkedin.com/jobs/view/{m.group(1)}/"
    if fonte == "indeed":
        # o jk identifica a vaga; o resto do link muda a cada alerta
        if m := re.search(r"[?&]jk=([0-9a-f]+)", link):
            return f"https://{urlparse(link).netloc}/viewjob?jk={m.group(1)}"
        return link
    u = urlparse(link)
    return f"{u.scheme}://{u.netloc}{u.path}"


def _bloco(a):
    """Menor ancestral com mais de uma linha de texto (título + empresa/local)."""
    for pai in a.parents:
        if len(list(pai.stripped_strings)) >= 2:
            return pai
    return a


def extrair_vagas(html: str, fonte: str) -> list[Vaga]:
    padrao = PADROES[fonte]
    soup = BeautifulSoup(html, "html.parser")
    vagas: dict[str, Vaga] = {}
    for a in soup.find_all("a", href=padrao):
        titulo = a.get_text(" ", strip=True)
        if not titulo or len(titulo) < 3:
            continue
        link = _normalizar_link(a["href"], fonte)
        if link in vagas:
            continue
        linhas = [s for s in _bloco(a).stripped_strings if s != titulo]
        empresa, local = "", ""
        if linhas:
            partes = re.split(r"\s+[·•|-]\s+", linhas[0], maxsplit=1)
            empresa = partes[0]
            local = partes[1] if len(partes) > 1 else (linhas[1] if len(linhas) > 1 else "")
        vagas[link] = Vaga(titulo=titulo, link=link, fonte=fonte, empresa=empresa, local=local)
    return list(vagas.values())
