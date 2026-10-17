# Roadmap

Um módulo por vez, testado isolado. Revisão curta ao fim de cada fase; revisão completa só na Fase 5.

## Decisões (padrão adotado, pode mudar)

- Orquestração: script Python (`python -m curriculos`). n8n fica para depois, se precisar.
- Currículo base: YAML em `data/curriculo_base/curriculo.yaml` (estruturado e fácil de editar à mão).
- PDF: Playwright (`page.pdf()`), já é dependência e evita o GTK que o weasyprint exige no Windows.

## Fase 0 — Setup
- `pyproject.toml` com dependências
- Modelo do currículo base em YAML
- Pronto quando: `pip install -e .[dev]` e `pytest` rodam

## Fase 1 — Coleta
- OAuth do Gmail (`credentials.json` → `token.json`)
- Buscar alertas por remetente (LinkedIn, Indeed, VanHack, Turing)
- Parser por fonte → `Vaga(titulo, empresa, link, descricao, fonte)` salva em `data/vagas/*.json`
- BeautifulSoup só se a descrição do e-mail vier incompleta; site bloqueado = pula
- Testes com e-mails de exemplo (sem rede)

## Fase 2 — IA
- Prompt em `prompts/adaptar_curriculo.md`
- Claude recebe currículo base + vaga, devolve currículo adaptado em JSON
- Validação: nenhum cargo, empresa, data ou habilidade fora do base
- Testes com cliente mockado

## Fase 3 — PDF
- Template HTML em `templates/curriculo.html` (ATS-friendly, uma coluna)
- Gera `output/Curriculo_<Nome>_<Empresa>_<Vaga>.pdf`

## Fase 4 — Submissão
- Cover letter (prompt em `prompts/cover_letter.md`)
- Vaga por e-mail: rascunho no Gmail com PDF anexado
- Vaga em plataforma: Playwright preenche campos de texto e pausa
- Nunca envia nada

## Fase 5 — Orquestração e revisão final
- CLI que liga as 4 etapas
- Revisão completa do código
