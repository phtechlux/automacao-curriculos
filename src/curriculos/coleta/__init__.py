from pathlib import Path

from .descricao import buscar_descricao
from .filtro import afinidade, chave, relevante
from .modelo import Vaga
from .parsers import extrair_vagas, fonte_do_remetente

PASTA_VAGAS = Path("data/vagas")
# fontes que bloqueiam o script (HTTP 403): nem tenta, a descrição é colada no painel
SEM_BUSCA = {"indeed"}


def carregar_vagas(pasta: Path = PASTA_VAGAS) -> list[Vaga]:
    return [Vaga.carregar(c) for c in sorted(pasta.glob("*.json"))]


def _guardar(vaga: Vaga, pasta: Path, vistas: set, filtro, base) -> bool:
    if chave(vaga) in vistas or (pasta / f"{vaga.fonte}_{vaga.id}.json").exists() or not filtro(vaga):
        return False
    vistas.add(chave(vaga))
    if base:
        vaga.afinidade, vaga.em_comum = afinidade(vaga, base)
    vaga.salvar(pasta)
    return True


def coletar_abertas(pasta: Path = PASTA_VAGAS, filtro=relevante, base: dict | None = None, buscar=None) -> list[Vaga]:
    """Fontes abertas (GitHub, Remotive, Arbeitnow, Himalayas): já vêm com descrição."""
    from .fontes import buscar_todas

    vistas = {chave(v) for v in carregar_vagas(pasta)}
    return [v for v in (buscar or buscar_todas)() if v.descricao and _guardar(v, pasta, vistas, filtro, base)]


def coletar(svc, dias: int = 2, pasta: Path = PASTA_VAGAS, buscar=buscar_descricao, filtro=relevante,
            base: dict | None = None) -> list[Vaga]:
    """Lê os alertas, descarta repetidas e fora da área, tenta buscar a descrição e salva.

    Vaga sem descrição é salva mesmo assim: a descrição pode ser colada no painel."""
    from .gmail import buscar_alertas

    vistas = {chave(v) for v in carregar_vagas(pasta)}
    novas = []
    for remetente, _assunto, html in buscar_alertas(svc, dias):
        fonte = fonte_do_remetente(remetente)
        if not fonte:
            continue
        for vaga in extrair_vagas(html, fonte):
            if chave(vaga) in vistas or (pasta / f"{vaga.fonte}_{vaga.id}.json").exists() or not filtro(vaga):
                continue
            if fonte not in SEM_BUSCA:
                vaga.descricao = buscar(vaga.link) or ""
            if _guardar(vaga, pasta, vistas, filtro, base):
                novas.append(vaga)
    return novas
