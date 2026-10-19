"""Painel web local: lista as vagas, recebe a descrição colada e gera o currículo adaptado.

Só escuta em 127.0.0.1. Nada é enviado: o painel gera o PDF e para."""
import json
import threading
import webbrowser
from dataclasses import asdict
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from curriculos.coleta import PASTA_VAGAS, carregar_vagas
from curriculos.coleta.modelo import Vaga
from curriculos.pdf import SAIDA

PAGINA = Path("templates/painel.html")
STATUS = {"nova", "gerada", "candidatada", "descartada"}
_trava = threading.Lock()  # uma geração/coleta por vez (Claude Code e Gmail)


def _arquivo(vaga_id: str) -> Path | None:
    return next(PASTA_VAGAS.glob(f"*_{vaga_id}.json"), None) if vaga_id.isalnum() else None


def _json_vaga(v: Vaga) -> dict:
    return {**asdict(v), "id": v.id}


def gerar(vaga: Vaga) -> Vaga:
    from curriculos.ia import adaptar
    from curriculos.pdf import gerar_pdf

    cv = adaptar(vaga)
    pdf = gerar_pdf(cv, vaga.empresa, vaga.titulo, idioma=cv.get("idioma", "pt"))
    pdf.with_suffix(".json").write_text(json.dumps(cv, ensure_ascii=False, indent=2), encoding="utf-8")
    vaga.status, vaga.pdf = "gerada", pdf.name
    return vaga


class Handler(BaseHTTPRequestHandler):
    def _responder(self, codigo: int, corpo, tipo: str = "application/json"):
        dados = corpo if isinstance(corpo, bytes) else json.dumps(corpo, ensure_ascii=False).encode()
        self.send_response(codigo)
        self.send_header("Content-Type", tipo)
        self.send_header("Content-Length", str(len(dados)))
        self.end_headers()
        self.wfile.write(dados)

    def _corpo(self) -> dict:
        tamanho = int(self.headers.get("Content-Length") or 0)
        return json.loads(self.rfile.read(tamanho) or b"{}")

    def do_GET(self):
        if self.path == "/":
            return self._responder(200, PAGINA.read_bytes(), "text/html; charset=utf-8")
        if self.path == "/api/vagas":
            return self._responder(200, [_json_vaga(v) for v in carregar_vagas(PASTA_VAGAS)])
        if self.path.startswith("/pdf/"):
            nome = Path(self.path[5:]).name  # sem subpastas
            caminho = SAIDA / nome
            if nome.endswith(".pdf") and caminho.exists():
                return self._responder(200, caminho.read_bytes(), "application/pdf")
        self._responder(404, {"erro": "não encontrado"})

    def do_POST(self):
        partes = self.path.strip("/").split("/")  # api/coletar | api/vagas/<id>/<acao>
        try:
            if partes == ["api", "coletar"]:
                return self._coletar(int(self._corpo().get("dias", 7)))
            if len(partes) == 4 and partes[:2] == ["api", "vagas"] and (arq := _arquivo(partes[2])):
                return self._acao(Vaga.carregar(arq), arq, partes[3], self._corpo())
            self._responder(404, {"erro": "não encontrado"})
        except Exception as e:  # o painel mostra o erro em vez de cair
            self._responder(500, {"erro": str(e)})

    def _coletar(self, dias: int):
        from curriculos.coleta import coletar
        from curriculos.coleta.gmail import servico

        with _trava:
            novas = coletar(servico(), dias=dias)
        self._responder(200, {"novas": len(novas)})

    def _acao(self, vaga: Vaga, arq: Path, acao: str, corpo: dict):
        if acao == "descricao":
            vaga.descricao = str(corpo.get("descricao", "")).strip()
        elif acao == "status" and corpo.get("status") in STATUS:
            vaga.status = corpo["status"]
        elif acao == "gerar":
            if not vaga.descricao:
                return self._responder(400, {"erro": "cole a descrição da vaga antes de gerar"})
            with _trava:
                vaga = gerar(vaga)
        else:
            return self._responder(400, {"erro": "ação inválida"})
        arq.write_text(json.dumps(asdict(vaga), ensure_ascii=False, indent=2), encoding="utf-8")
        self._responder(200, _json_vaga(vaga))

    def log_message(self, *args):  # silencia o log de cada requisição
        pass


def rodar(porta: int = 8765, abrir: bool = True):
    servidor = ThreadingHTTPServer(("127.0.0.1", porta), Handler)
    url = f"http://127.0.0.1:{porta}"
    print(f"Painel em {url} (Ctrl+C para sair)")
    if abrir:
        webbrowser.open(url)
    try:
        servidor.serve_forever()
    except KeyboardInterrupt:
        pass
