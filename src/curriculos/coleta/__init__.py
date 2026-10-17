from pathlib import Path

from .descricao import buscar_descricao
from .modelo import Vaga
from .parsers import extrair_vagas, fonte_do_remetente

PASTA_VAGAS = Path("data/vagas")


def coletar(svc, dias: int = 2, pasta: Path = PASTA_VAGAS, buscar=buscar_descricao) -> list[Vaga]:
    """Lê os alertas, extrai vagas novas, busca a descrição e salva. Vaga sem descrição é pulada."""
    from .gmail import buscar_alertas

    novas = []
    for remetente, _assunto, html in buscar_alertas(svc, dias):
        fonte = fonte_do_remetente(remetente)
        if not fonte:
            continue
        for vaga in extrair_vagas(html, fonte):
            if (pasta / f"{vaga.fonte}_{vaga.id}.json").exists():
                continue
            vaga.descricao = buscar(vaga.link) or ""
            if not vaga.descricao:
                continue
            vaga.salvar(pasta)
            novas.append(vaga)
    return novas
