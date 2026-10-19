"""Filtro de relevância pelo título e chave para achar a mesma vaga em alertas diferentes."""
import re
import unicodedata

# termos procurados como palavra inteira no título, sem acento e em minúsculas
INCLUIR = [
    "desenvolvedor", "desenvolvedora", "developer", "dev", "programador", "programadora", "programacao",
    "front", "frontend", "front-end", "back", "backend", "back-end", "full", "fullstack", "full-stack",
    "software", "web", "react", "javascript", "typescript", "node", "mobile", "sistemas",
    "ti", "tecnologia", "suporte", "qa", "tester", "dados", "data",
]
EXCLUIR = [
    "senior", "sr", "pleno", "pl", "lead", "lider", "staff", "principal", "especialista", "coordenador",
    "gerente", "head", "manager", "director", "diretor", "consultant",
    # vagas afirmativas exclusivas (Pedro não é público-alvo)
    "women", "mulheres", "mulher", "people with disabilities", "pcd", "pessoas com deficiencia",
    "educacao fisica", "enfermagem", "contabil", "direito", "vendedor", "motorista",
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
    # só letras e números: "Dev Jr | Acme" e "Dev Jr - Acme" (empresa no título) viram a mesma chave
    return re.sub(r"[^a-z0-9]", "", normalizar(f"{vaga.titulo}{vaga.empresa}"))


def afinidade(vaga, base: dict) -> tuple[int, list[str]]:
    """Nota grátis (sem IA): quantas habilidades do currículo base a descrição cita."""
    texto = normalizar(f"{vaga.titulo} {vaga.descricao}")
    habilidades = [h for grupo in (base.get("habilidades") or {}).values() for h in grupo or []]
    achadas = []
    for h in habilidades:
        nome = normalizar(re.sub(r"\s*\(.*?\)", "", h))  # "Java (acadêmico)" -> "java"
        if len(nome) > 1 and _tem(texto, [nome]):
            achadas.append(h)
    return min(100, round(100 * len(achadas) / 6)), achadas  # 6+ em comum = 100
