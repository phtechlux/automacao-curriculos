"""Adapta o currículo base a uma vaga via API do Claude, com validação anti-invenção."""
import json
import os
import re
import shutil
import subprocess
import tempfile
from pathlib import Path
from types import SimpleNamespace

import yaml

from curriculos.coleta.modelo import Vaga

PROMPT = Path("prompts/adaptar_curriculo.md")
CURRICULO = Path("data/curriculo_base/curriculo.yaml")
MODELO = os.getenv("CLAUDE_MODEL", "claude-sonnet-5-5")


class CurriculoInvalido(Exception):
    pass


class ClaudeCLI:
    """Usa o Claude Code instalado (`claude -p`, plano do usuário) no lugar da API paga.

    Imita `client.messages.create` para o resto do código não mudar."""

    def __init__(self, modelo: str = os.getenv("CLAUDE_CLI_MODEL", "sonnet"), timeout: int = 300):
        self.exe = shutil.which("claude")
        if not self.exe:
            raise RuntimeError("Claude Code não encontrado; instale-o ou defina ANTHROPIC_API_KEY no .env")
        self.modelo, self.timeout = modelo, timeout
        self.messages = self

    def create(self, model=None, max_tokens=None, system=(), messages=()):
        instrucoes, *contexto = [b["text"] for b in system]
        conversa = [f"[{m['role'].upper()}]\n{m['content']}" for m in messages]
        entrada = "\n\n".join(contexto + conversa)
        # roda fora do projeto para não carregar CLAUDE.md, hooks nem ferramentas
        with tempfile.TemporaryDirectory() as pasta:
            r = subprocess.run(
                [self.exe, "-p", "--output-format", "text", "--model", self.modelo, "--tools", "",
                 "--no-session-persistence", "--strict-mcp-config", "--system-prompt", instrucoes],
                input=entrada, capture_output=True, text=True, encoding="utf-8", cwd=pasta, timeout=self.timeout,
            )
        if r.returncode != 0:
            raise RuntimeError(f"claude -p falhou: {r.stderr.strip()[:500]}")
        return SimpleNamespace(content=[SimpleNamespace(text=r.stdout)])


def cliente_padrao():
    """API paga se houver chave; senão o Claude Code do usuário."""
    if os.getenv("ANTHROPIC_API_KEY"):
        import anthropic

        return anthropic.Anthropic()
    return ClaudeCLI()


def carregar_curriculo(caminho: Path = CURRICULO) -> dict:
    return yaml.safe_load(caminho.read_text(encoding="utf-8"))


def _json(texto: str) -> dict:
    inicio, fim = texto.find("{"), texto.rfind("}")
    if inicio < 0 or fim < 0:
        raise CurriculoInvalido("resposta sem JSON")
    return json.loads(texto[inicio : fim + 1])


def _numeros(texto: str) -> set[str]:
    return set(re.findall(r"\d+(?:[.,]\d+)?", texto))


def validar(base: dict, adaptado: dict) -> list[str]:
    """Lista de problemas; vazia = ok."""
    problemas = []
    chave = lambda e: (e.get("cargo"), e.get("empresa"), str(e.get("inicio")), str(e.get("fim")))
    exps_base = {chave(e) for e in base.get("experiencias", [])}
    for e in adaptado.get("experiencias", []):
        if chave(e) not in exps_base:
            problemas.append(f"experiência inexistente ou alterada: {chave(e)}")

    projetos_base = {p.get("nome") for p in base.get("projetos") or []}
    for p in adaptado.get("projetos") or []:
        if p.get("nome") not in projetos_base:
            problemas.append(f"projeto inexistente: {p.get('nome')}")

    cursos_base = {(f.get("curso"), f.get("instituicao")) for f in base.get("formacao", [])}
    for f in adaptado.get("formacao", []):
        if (f.get("curso"), f.get("instituicao")) not in cursos_base:
            problemas.append(f"formação inexistente: {f.get('curso')}")

    hab_base = {h.lower() for grupo in (base.get("habilidades") or {}).values() for h in grupo or []}
    for grupo in (adaptado.get("habilidades") or {}).values():
        for h in grupo or []:
            if h.lower() not in hab_base:
                problemas.append(f"habilidade inexistente: {h}")

    cert_base = {str(c).lower() for c in base.get("certificacoes") or []}
    for c in adaptado.get("certificacoes") or []:
        if str(c).lower() not in cert_base:
            problemas.append(f"certificação inexistente: {c}")

    # números (métricas, anos) no texto livre precisam existir no base
    nums_base = _numeros(yaml.safe_dump(base, allow_unicode=True))
    livre = [adaptado.get("resumo", "")] + [c for e in adaptado.get("experiencias", []) for c in e.get("conquistas", [])]
    livre += [d for p in adaptado.get("projetos") or [] for d in p.get("destaques", [])]
    for n in _numeros(" ".join(livre)) - nums_base:
        problemas.append(f"número não encontrado no base: {n}")
    return problemas


def adaptar(vaga: Vaga, base: dict | None = None, client=None, tentativas: int = 2) -> dict:
    base = base or carregar_curriculo()
    client = client or cliente_padrao()
    # currículo no system com cache: igual para todas as vagas, barateia as chamadas seguintes
    system = [
        {"type": "text", "text": PROMPT.read_text(encoding="utf-8")},
        {
            "type": "text",
            "text": "CURRÍCULO BASE:\n" + yaml.safe_dump(base, allow_unicode=True, sort_keys=False),
            "cache_control": {"type": "ephemeral"},
        },
    ]
    mensagens = [{"role": "user", "content": f"VAGA: {vaga.titulo} — {vaga.empresa} ({vaga.local})\n\n{vaga.descricao}"}]

    for _ in range(tentativas):
        resp = client.messages.create(model=MODELO, max_tokens=4000, system=system, messages=mensagens)
        texto = resp.content[0].text
        try:
            adaptado = _json(texto)
            problemas = validar(base, adaptado)
        except (json.JSONDecodeError, CurriculoInvalido) as e:
            problemas = [str(e)]
        if not problemas:
            # dados pessoais sempre do base, nunca do modelo
            adaptado["nome"], adaptado["contato"] = base.get("nome"), base.get("contato")
            return adaptado
        mensagens += [
            {"role": "assistant", "content": texto},
            {"role": "user", "content": "Corrija, usando só o currículo base:\n- " + "\n- ".join(problemas)},
        ]
    raise CurriculoInvalido("; ".join(problemas))
