"""Painel web: lista as vagas, recebe a descrição colada e gera o currículo adaptado.

Local (`/`, sem token): dados de Pedro, pastas padrão — uso pessoal, como sempre foi.
Produto (`/c/<token>/...`): dados isolados por conta (CTA-03), comprada na Kiwify.
Nada é enviado: o painel gera o PDF e para."""
import json
import os
import threading
import uuid
import webbrowser
from dataclasses import asdict
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

from curriculos import contas, kiwify
from curriculos.coleta import PASTA_VAGAS, carregar_vagas
from curriculos.coleta.modelo import Vaga
from curriculos.contas import Caminhos
from curriculos.ia import CURRICULO as CURRICULO_PADRAO
from curriculos.pdf import SAIDA

PAGINA = Path("templates/painel.html")
ENTRAR = """<!doctype html><meta charset="utf-8"><title>Entrar</title>
<body style="font:15px system-ui;max-width:420px;margin:60px auto;padding:0 16px">
<h1>Acessar minha conta</h1>
<p>Digite o e-mail usado na compra.</p>
<input id="email" type="email" placeholder="seu@email.com" style="width:100%;padding:8px;margin-bottom:8px">
<button id="ir">Entrar</button>
<p id="msg" style="color:#b91c1c"></p>
<script>
document.getElementById("ir").onclick = async () => {
  const email = document.getElementById("email").value.trim();
  const r = await fetch("/api/entrar", {method: "POST", headers: {"Content-Type": "application/json"}, body: JSON.stringify({email})});
  const d = await r.json();
  if (r.ok) location.href = "/c/" + d.token; else document.getElementById("msg").textContent = d.erro || "não encontrado";
};
</script>""".encode("utf-8")
STATUS = {"nova", "gerada", "candidatada", "descartada"}
# Uso local (Pedro): 1 por vez, como sempre foi (evita sessões concorrentes do `claude -p`).
# Produto hospedado com ANTHROPIC_API_KEY: sem esse motivo, pode subir via GERACOES_SIMULTANEAS
# (limitado pelos recursos do servidor — cada geração abre um Chromium do Playwright).
_trava = threading.Semaphore(int(os.getenv("GERACOES_SIMULTANEAS", "1")))

# Limitador simples (memória, por processo) pra /entrar e o webhook — ambos são endpoints
# públicos sem login; sem isso dariam pra força-bruta de e-mail ou do segredo do webhook.
_tentativas: dict[str, list[float]] = {}
_tentativas_trava = threading.Lock()


def _limitar(chave: str, maximo: int = 20, janela: float = 60.0) -> bool:
    """True = pode seguir; False = excedeu o limite (bloquear com 429)."""
    import time

    agora = time.monotonic()
    with _tentativas_trava:
        hist = [t for t in _tentativas.get(chave, []) if agora - t < janela]
        hist.append(agora)
        _tentativas[chave] = hist
        return len(hist) <= maximo


def _padrao() -> Caminhos:
    # função (não constante): lê PASTA_VAGAS/SAIDA/CURRICULO_PADRAO do módulo a cada chamada,
    # pra respeitar monkeypatch nos testes e qualquer troca em runtime
    return Caminhos(vagas=PASTA_VAGAS, saida=SAIDA, curriculo=CURRICULO_PADRAO)


def _arquivo(pasta_vagas: Path, vaga_id: str) -> Path | None:
    return next(pasta_vagas.glob(f"*_{vaga_id}.json"), None) if vaga_id.isalnum() else None


def _json_vaga(v: Vaga) -> dict:
    return {**asdict(v), "id": v.id}


def gerar(vaga: Vaga, cam: Caminhos) -> Vaga:
    from curriculos.ia import adaptar, carregar_curriculo
    from curriculos.pdf import gerar_pdf

    cv = adaptar(vaga, base=carregar_curriculo(cam.curriculo))
    pdf = gerar_pdf(cv, vaga.empresa, vaga.titulo, idioma=cv.get("idioma", "pt"), saida=cam.saida)
    pdf.with_suffix(".json").write_text(json.dumps(cv, ensure_ascii=False, indent=2), encoding="utf-8")
    vaga.status, vaga.pdf, vaga.analise = "gerada", pdf.name, cv.get("analise") or {}
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

    def _rota(self):
        """(caminhos da conta, partes do caminho sem o prefixo /c/<token>, token|None).
        caminhos=None quando o token não corresponde a nenhuma conta."""
        partes = [p for p in urlsplit(self.path).path.strip("/").split("/") if p]
        if partes[:1] == ["c"] and len(partes) >= 2:
            return contas.caminhos(partes[1]), partes[2:], partes[1]
        return _padrao(), partes, None

    def do_GET(self):
        partes_cruas = [p for p in urlsplit(self.path).path.strip("/").split("/") if p]
        if not partes_cruas or (partes_cruas[:1] == ["c"] and len(partes_cruas) == 2):
            return self._responder(200, PAGINA.read_bytes(), "text/html; charset=utf-8")
        if partes_cruas == ["entrar"]:
            return self._responder(200, ENTRAR, "text/html; charset=utf-8")
        cam, partes, token = self._rota()
        if cam is None:
            return self._responder(404, {"erro": "conta não encontrada"})
        if partes == ["api", "vagas"]:
            return self._responder(200, [_json_vaga(v) for v in sorted(carregar_vagas(cam.vagas), key=lambda v: -v.afinidade)])
        if partes == ["api", "conta"] and token:
            conta = contas.carregar(token)
            return self._responder(200, {"email": conta["email"], "creditos": conta["creditos"]})
        if partes == ["api", "curriculo"] and token:
            return self._responder(200, {"yaml": cam.curriculo.read_text(encoding="utf-8") if cam.curriculo.exists() else ""})
        if len(partes) == 2 and partes[0] == "pdf":
            nome = Path(partes[1]).name
            arq = cam.saida / nome
            if nome.endswith(".pdf") and arq.exists():
                return self._responder(200, arq.read_bytes(), "application/pdf")
        self._responder(404, {"erro": "não encontrado"})

    def do_POST(self):
        caminho = urlsplit(self.path).path
        if caminho == "/webhook/kiwify":
            return self._webhook_kiwify()
        if caminho == "/api/entrar":
            return self._entrar(self._corpo())
        cam, partes, token = self._rota()
        if cam is None:
            return self._responder(404, {"erro": "conta não encontrada"})
        try:
            if partes == ["api", "coletar"] and token is None:  # coleta automática só no uso local (Fase 10)
                return self._coletar(int(self._corpo().get("dias", 7)))
            if partes == ["api", "vagas"]:
                return self._criar(cam, self._corpo())
            if partes == ["api", "curriculo"] and token:
                return self._curriculo(cam, self._corpo())
            if len(partes) == 4 and partes[:2] == ["api", "vagas"] and (arq := _arquivo(cam.vagas, partes[2])):
                return self._acao(Vaga.carregar(arq), arq, partes[3], self._corpo(), cam, token)
            self._responder(404, {"erro": "não encontrado"})
        except Exception as e:  # o painel mostra o erro em vez de cair
            self._responder(500, {"erro": str(e)})

    def _coletar(self, dias: int):
        from curriculos.coleta import coletar, coletar_abertas
        from curriculos.coleta.gmail import servico
        from curriculos.ia import carregar_curriculo

        base = carregar_curriculo()
        with _trava:
            abertas = coletar_abertas(PASTA_VAGAS, base=base)
            try:
                gmail = coletar(servico(), dias=dias, pasta=PASTA_VAGAS, base=base)
            except Exception:  # sem token/rede: segue só com as fontes abertas
                gmail = []
        self._responder(200, {"novas": len(abertas) + len(gmail)})

    def _criar(self, cam: Caminhos, corpo: dict):
        """ENT-01: cria uma vaga colando os dados direto, sem precisar coletar antes."""
        titulo = str(corpo.get("titulo", "")).strip()
        if not titulo:
            return self._responder(400, {"erro": "título é obrigatório"})
        vaga = Vaga(
            titulo=titulo, link=f"manual://{uuid.uuid4()}", fonte="manual",
            empresa=str(corpo.get("empresa", "")).strip(), local=str(corpo.get("local", "")).strip(),
            descricao=str(corpo.get("descricao", "")).strip(),
        )
        vaga.salvar(cam.vagas)
        self._responder(200, _json_vaga(vaga))

    def _acao(self, vaga: Vaga, arq: Path, acao: str, corpo: dict, cam: Caminhos, token: str | None):
        if acao == "descricao":
            vaga.descricao = str(corpo.get("descricao", "")).strip()
        elif acao == "status" and corpo.get("status") in STATUS:
            vaga.status = corpo["status"]
        elif acao == "gerar":
            if not vaga.descricao:
                return self._responder(400, {"erro": "cole a descrição da vaga antes de gerar"})
            with _trava:
                if token and not contas.consumir(token):  # COB-02
                    return self._responder(402, {"erro": "sem créditos — compre mais para continuar gerando"})
                try:
                    vaga = gerar(vaga, cam)
                except Exception:
                    if token:  # geração falhou: devolve o crédito, cliente não perde nada
                        contas.creditar(token, 1)
                    raise
        else:
            return self._responder(400, {"erro": "ação inválida"})
        arq.write_text(json.dumps(asdict(vaga), ensure_ascii=False, indent=2), encoding="utf-8")
        self._responder(200, _json_vaga(vaga))

    def _curriculo(self, cam: Caminhos, corpo: dict):
        """CTA-02: currículo base por conta, colado como YAML (sem editar arquivo à mão)."""
        import yaml

        texto = str(corpo.get("yaml", ""))
        try:
            dados = yaml.safe_load(texto) or {}
        except yaml.YAMLError as e:
            return self._responder(400, {"erro": f"YAML inválido: {e}"})
        if not isinstance(dados, dict) or not dados.get("nome"):
            return self._responder(400, {"erro": "YAML precisa ter pelo menos o campo 'nome'"})
        cam.curriculo.parent.mkdir(parents=True, exist_ok=True)
        cam.curriculo.write_text(texto, encoding="utf-8")
        self._responder(200, {"ok": True})

    def _entrar(self, corpo: dict):
        """LAN-03 sem e-mail: cliente confirma o e-mail da compra e entra direto na conta."""
        if not _limitar(f"entrar:{self.client_address[0]}"):
            return self._responder(429, {"erro": "muitas tentativas, aguarde um pouco"})
        email = str(corpo.get("email", "")).strip()
        token = email and contas.email_para_token(email)
        if not token:
            return self._responder(404, {"erro": "e-mail não encontrado — confira se é o mesmo da compra"})
        self._responder(200, {"token": token})

    def _webhook_kiwify(self):
        if not _limitar(f"webhook:{self.client_address[0]}", maximo=30):
            return self._responder(429, {"erro": "muitas tentativas, aguarde um pouco"})
        segredo = (parse_qs(urlsplit(self.path).query).get("secret") or [""])[0]
        try:
            kiwify.validar_segredo(segredo)
            resultado = kiwify.processar(self._corpo())
        except kiwify.WebhookInvalido as e:
            return self._responder(400, {"erro": str(e)})
        self._responder(200, resultado)

    def log_message(self, *args):  # silencia o log de cada requisição
        pass


def rodar(porta: int | None = None, abrir: bool | None = None, host: str | None = None):
    """HOS-01: host/porta configuráveis por env var para rodar hospedado, não só local."""
    host = host or os.getenv("HOST", "127.0.0.1")
    porta = porta or int(os.getenv("PORTA", "8765"))
    abrir = abrir if abrir is not None else host == "127.0.0.1"
    servidor = ThreadingHTTPServer((host, porta), Handler)
    url = f"http://{host}:{porta}"
    print(f"Painel em {url} (Ctrl+C para sair)")
    if abrir:
        webbrowser.open(url)
    try:
        servidor.serve_forever()
    except KeyboardInterrupt:
        pass
