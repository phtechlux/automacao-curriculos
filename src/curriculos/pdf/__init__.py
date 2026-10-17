"""Renderiza o currículo adaptado no template HTML e gera o PDF com Playwright."""
import re
import unicodedata
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape

TEMPLATES = Path("templates")
SAIDA = Path("output")

TITULOS = {
    "pt": dict(resumo="Resumo", experiencia="Experiência", projetos="Projetos", habilidades="Habilidades",
               formacao="Formação", certificacoes="Certificações", idiomas="Idiomas"),
    "en": dict(resumo="Summary", experiencia="Experience", projetos="Projects", habilidades="Skills",
               formacao="Education", certificacoes="Certifications", idiomas="Languages"),
}


def _slug(texto: str, limite: int = 40) -> str:
    texto = unicodedata.normalize("NFKD", texto or "").encode("ascii", "ignore").decode()
    return re.sub(r"[^A-Za-z0-9]+", "_", texto).strip("_")[:limite].rstrip("_") or "X"


def nome_arquivo(nome: str, empresa: str, vaga: str) -> str:
    return f"Curriculo_{_slug(nome)}_{_slug(empresa)}_{_slug(vaga)}.pdf"


def renderizar_html(curriculo: dict, idioma: str = "en", templates: Path = TEMPLATES) -> str:
    env = Environment(loader=FileSystemLoader(templates), autoescape=select_autoescape())
    return env.get_template("curriculo.html").render(c=curriculo, t=TITULOS.get(idioma, TITULOS["en"]), idioma=idioma)


def html_para_pdf(html: str, destino: Path) -> Path:
    from playwright.sync_api import sync_playwright

    destino.parent.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.set_content(html, wait_until="load")
        page.pdf(path=str(destino), format="A4", print_background=True, prefer_css_page_size=True)
        browser.close()
    return destino


def gerar_pdf(curriculo: dict, empresa: str, vaga: str, idioma: str = "en", saida: Path = SAIDA) -> Path:
    destino = saida / nome_arquivo(curriculo.get("nome", ""), empresa, vaga)
    return html_para_pdf(renderizar_html(curriculo, idioma), destino)
