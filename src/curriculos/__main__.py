"""python -m curriculos [painel|coletar] — roda a partir da raiz do projeto."""
import os
import sys
from pathlib import Path

os.chdir(Path(__file__).resolve().parents[2])

from dotenv import load_dotenv  # noqa: E402

load_dotenv()


def main():
    comando = sys.argv[1] if len(sys.argv) > 1 else "painel"
    if comando == "painel":
        from curriculos.painel import rodar

        rodar()
    elif comando == "coletar":
        from curriculos.coleta import coletar
        from curriculos.coleta.gmail import servico

        dias = int(sys.argv[2]) if len(sys.argv) > 2 else 7
        print(f"{len(coletar(servico(), dias=dias))} vagas novas")
    else:
        sys.exit("uso: python -m curriculos [painel|coletar [dias]]")


main()
