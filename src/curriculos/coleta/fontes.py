"""Fontes abertas de vagas (APIs públicas e gratuitas). Já trazem a descrição completa.

Só endpoints públicos e documentados; erro ou bloqueio = a fonte é pulada."""
import json
import re
import urllib.error
import urllib.request

from bs4 import BeautifulSoup

from .modelo import Vaga

AGENTE = {"User-Agent": "curriculos-pessoal/0.1", "Accept": "application/json"}
REPOS_GITHUB = ["frontendbr/vagas", "backend-br/vagas", "soujava/vagas-java"]
# vaga remota que aceita alguém no Brasil
LOCAIS_OK = re.compile(r"worldwide|anywhere|global|brazil|brasil|latam|latin america|americas|south america", re.I)


def _get(url: str, timeout: int = 20):
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers=AGENTE), timeout=timeout) as r:
            return json.loads(r.read().decode("utf-8", errors="replace"))
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError):
        return None


def _texto(html: str) -> str:
    return BeautifulSoup(html or "", "html.parser").get_text("\n", strip=True)


def github(repos=REPOS_GITHUB) -> list[Vaga]:
    vagas = []
    for repo in repos:
        for i in _get(f"https://api.github.com/repos/{repo}/issues?state=open&per_page=50") or []:
            if "pull_request" in i:
                continue
            titulo = i["title"]
            local = m.group(1) if (m := re.match(r"\s*\[([^\]]+)\]", titulo)) else ""
            titulo = re.sub(r"^\s*\[[^\]]+\]\s*", "", titulo)
            empresa = ""
            if m := re.search(r"\s(?:na|no|at|@)\s+(.+)$", titulo):
                empresa, titulo = m.group(1).strip(), titulo[: m.start()].strip()
            vagas.append(Vaga(titulo=titulo, link=i["html_url"], fonte="github", empresa=empresa,
                              local=local, descricao=i.get("body") or ""))
    return vagas


def remotive(busca: str = "developer") -> list[Vaga]:
    dados = _get(f"https://remotive.com/api/remote-jobs?search={busca}&limit=100") or {}
    return [
        Vaga(titulo=j["title"], link=j["url"], fonte="remotive", empresa=j["company_name"],
             local=j.get("candidate_required_location", ""), descricao=_texto(j["description"]))
        for j in dados.get("jobs", [])
        if LOCAIS_OK.search(j.get("candidate_required_location") or "")
    ]


def arbeitnow() -> list[Vaga]:
    dados = _get("https://www.arbeitnow.com/api/job-board-api") or {}
    return [
        Vaga(titulo=j["title"], link=j["url"], fonte="arbeitnow", empresa=j["company_name"],
             local=f"Remoto ({j.get('location', '')})", descricao=_texto(j["description"]))
        for j in dados.get("data", [])
        if j.get("remote")
    ]


def himalayas() -> list[Vaga]:
    dados = _get("https://himalayas.app/jobs/api?limit=100") or {}
    vagas = []
    for j in dados.get("jobs", []):
        locais = j.get("locationRestrictions") or []
        if locais and not any(LOCAIS_OK.search(str(l)) for l in locais):
            continue
        vagas.append(Vaga(titulo=j["title"], link=j.get("applicationLink") or j.get("guid", ""), fonte="himalayas",
                          empresa=j.get("companyName", ""), local=", ".join(map(str, locais)) or "Worldwide",
                          descricao=_texto(j.get("description", ""))))
    return vagas


FONTES = {"github": github, "remotive": remotive, "arbeitnow": arbeitnow, "himalayas": himalayas}


def buscar_todas(fontes=FONTES) -> list[Vaga]:
    vagas = []
    for buscar in fontes.values():
        try:
            vagas += buscar()
        except Exception:  # uma fonte fora do ar não derruba as outras
            continue
    return [v for v in vagas if v.link]
