"""Filtro de relevância pelo título e chave para achar a mesma vaga em alertas diferentes."""
import re
import unicodedata

# termos procurados como palavra inteira no título, sem acento e em minúsculas
INCLUIR = [
    "desenvolvedor", "desenvolvedora", "developer", "dev", "programador", "programadora", "programacao",
    "front", "frontend", "front-end", "back", "backend", "back-end", "full", "fullstack", "full-stack",
    "software", "web", "react", "javascript", "typescript", "node", "mobile", "sistemas", "ads",
    "ti", "tecnologia", "suporte", "qa", "tester", "dados", "data",
]
EXCLUIR = [
    "senior", "sr", "pleno", "pl", "lead", "lider", "staff", "principal", "especialista", "coordenador",
    "gerente", "head", "educacao fisica", "enfermagem", "contabil", "direito", "vendedor", "motorista",
]


def normalizar(texto: str) -> str:
    texto = unicodedata.normalize("NFKD", texto or "").encode("ascii", "ignore").decode().lower()
    return re.sub(r"\s+", " ", texto).strip()


def _tem(texto: str, termos: list[str]) -> bool:
    return any(re.search(rf"(?<![a-z]){re.escape(t)}(?![a-z])", texto) for t in termos)


def relevante(vaga) -> bool:
    titulo = normalizar(vaga.titulo)
    return _tem(titulo, INCLUIR) and not _tem(titulo, EXCLUIR)


def chave(vaga) -> str:
    """Mesmo título + empresa = mesma vaga, mesmo com links diferentes."""
    return f"{normalizar(vaga.titulo)}|{normalizar(vaga.empresa)}"
