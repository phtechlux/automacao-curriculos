from pathlib import Path

from .descricao import buscar_descricao
from .filtro import chave, relevante
from .modelo import Vaga
from .parsers import extrair_vagas, fonte_do_remetente

PASTA_VAGAS = Path("data/vagas")
# fontes que bloqueiam o script (HTTP 403): nem tenta, a descrição é colada no painel
SEM_BUSCA = {"indeed"}


def carregar_vagas(pasta: Path = PASTA_VAGAS) -> list[Vaga]:
    return [Vaga.carregar(c) for c in sorted(pasta.glob("*.json"))]


def coletar(svc, dias: int = 2, pasta: Path = PASTA_VAGAS, buscar=buscar_descricao, filtro=relevante) -> list[Vaga]:
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
            vistas.add(chave(vaga))
            if fonte not in SEM_BUSCA:
                vaga.descricao = buscar(vaga.link) or ""
            vaga.salvar(pasta)
            novas.append(vaga)
    return novas
