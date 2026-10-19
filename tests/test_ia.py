import json
from types import SimpleNamespace

import pytest

from curriculos.coleta.modelo import Vaga
from curriculos.ia import CurriculoInvalido, adaptar, validar

BASE = {
    "nome": "Fulano",
    "contato": {"email": "f@x.com"},
    "resumo": "Dev com 5 anos.",
    "experiencias": [
        {"cargo": "Dev", "empresa": "A", "inicio": "2020-01", "fim": "atual", "local": "SP",
         "conquistas": ["Reduzi custo em 30%"]},
    ],
    "formacao": [{"curso": "CC", "instituicao": "USP", "conclusao": "2019"}],
    "habilidades": {"tecnicas": ["Python", "SQL"], "ferramentas": ["Git"]},
    "certificacoes": [],
}
BOM = {
    "titulo": "Dev", "resumo": "Dev Python com 5 anos.",
    "experiencias": [dict(BASE["experiencias"][0], conquistas=["Cortei 30% do custo"])],
    "formacao": BASE["formacao"], "habilidades": {"tecnicas": ["python"], "ferramentas": []},
    "certificacoes": [], "palavras_chave": ["Python"],
}
VAGA = Vaga(titulo="Python Dev", link="http://x", fonte="linkedin", descricao="Python")


def test_validar_ok():
    assert validar(BASE, BOM) == []


@pytest.mark.parametrize("alteracao, trecho", [
    ({"habilidades": {"tecnicas": ["Kubernetes"]}}, "habilidade"),
    ({"resumo": "Dev com 10 anos."}, "número"),
    ({"experiencias": [dict(BASE["experiencias"][0], empresa="Google")]}, "experiência"),
    ({"certificacoes": ["AWS"]}, "certificação"),
])
def test_validar_pega_invencao(alteracao, trecho):
    assert any(trecho in p for p in validar(BASE, {**BOM, **alteracao}))


class FakeClient:
    def __init__(self, respostas):
        self.respostas, self.chamadas = list(respostas), []
        self.messages = self

    def create(self, **kw):
        self.chamadas.append(kw)
        return SimpleNamespace(content=[SimpleNamespace(text=self.respostas.pop(0))])


def test_adaptar_corrige_na_segunda():
    ruim = json.dumps({**BOM, "habilidades": {"tecnicas": ["Rust"]}})
    client = FakeClient([ruim, "```json\n" + json.dumps(BOM) + "\n```"])
    r = adaptar(VAGA, BASE, client)
    assert r["nome"] == "Fulano" and len(client.chamadas) == 2
    assert "Rust" in client.chamadas[1]["messages"][-1]["content"]


def test_adaptar_desiste():
    ruim = json.dumps({**BOM, "resumo": "99 anos"})
    with pytest.raises(CurriculoInvalido):
        adaptar(VAGA, BASE, FakeClient([ruim, ruim]))


def test_validar_projeto_inventado():
    base = {**BASE, "projetos": [{"nome": "ERP", "destaques": ["Fiz logout"]}]}
    adaptado = {**base, "projetos": [{"nome": "App Bancário", "destaques": ["Atendi 1000 usuários"]}]}
    problemas = validar(base, adaptado)
    assert any("projeto inexistente" in p for p in problemas)
    assert any("1000" in p for p in problemas)


def test_validar_estudando_nao_vira_habilidade():
    base = {**BASE, "estudando": ["TypeScript"]}
    adaptado = {**base, "habilidades": {"tecnicas": ["TypeScript"]}}
    assert any("TypeScript" in p for p in validar(base, adaptado))


def test_cliente_cli_monta_chamada(monkeypatch):
    from curriculos import ia

    chamada = {}

    def fake_run(cmd, input, **kw):
        chamada.update(cmd=cmd, input=input)
        return SimpleNamespace(returncode=0, stdout='{"ok": 1}', stderr="")

    monkeypatch.setattr(ia.shutil, "which", lambda _: "claude")
    monkeypatch.setattr(ia.subprocess, "run", fake_run)
    resp = ia.ClaudeCLI().messages.create(
        system=[{"type": "text", "text": "REGRAS"}, {"type": "text", "text": "BASE"}],
        messages=[{"role": "user", "content": "VAGA X"}])
    assert resp.content[0].text == '{"ok": 1}'
    assert chamada["cmd"][-1] == "REGRAS" and "--tools" in chamada["cmd"]
    assert "BASE" in chamada["input"] and "VAGA X" in chamada["input"]
