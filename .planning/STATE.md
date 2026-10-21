---
gsd_state_version: '1.0'
status: planning
progress:
  total_phases: 10
  completed_phases: 8
  total_plans: 8
  completed_plans: 8
  percent: 80
---
<!-- STATE-MD-SCHEMA:END:frontmatter -->

# Project State

## Project Reference

See: .planning/PROJECT.md (updated 2026-10-21)

**Core value:** Um currículo adaptado e verdadeiro por vaga, sem trabalho manual: a IA nunca inventa fatos.
**Current focus:** ações manuais de lançamento (fora de código) — escolher hospedagem e configurar o produto na Kiwify

## Current Position

Phase: 8 of 10 (Lançamento) — código completo e **testado** (43 testes, incluindo os novos de contas/Kiwify/painel multiusuário + 1 ponta-a-ponta manual no servidor real)
Plan: 0 of ? in current phase
Status: Código pronto e testado; falta ação manual do Pedro fora do editor (ver Pending Todos)
Last activity: 2026-10-21 — Python 3.12 e Playwright/Chromium instalados nesta máquina; bateria de testes rodada e 4 bugs reais corrigidos (ver Decisions); testado ao vivo o fluxo webhook→entrar→conta→vaga

Progress: [████████░░] 80%

## Accumulated Context

### Decisions

Decisions are logged in PROJECT.md Key Decisions table.

- [Phase 1]: PDF via Playwright; currículo base em YAML; validação anti-invenção em código
- [Phase 1]: `estudando` nunca vira habilidade
- [2026-10-21]: pivô de projeto pessoal para produto multiusuário vendido na Kiwify; fluxo "colar vaga" substitui Gmail como caminho principal; Gmail automático vira Fase 10 (futuro/avançado)
- [2026-10-21]: contas sem senha (token direto no link); acesso recuperado por e-mail em `/entrar`, sem precisar de serviço de e-mail transacional
- [2026-10-21]: dados de conta em arquivo JSON local (`data/contas/<token>/`), não banco de dados — simples pra validar o produto, mas **não sobrevive a redeploy sem volume persistente** (ver Hospedagem)
- [2026-10-21]: bugs achados pela bateria de testes e corrigidos: (1) HTML embutido como `bytes` literal quebrava com acento — virou `str.encode()`; (2) `PADRAO` congelava os caminhos na importação do módulo, monkeypatch/troca em runtime não tinha efeito — virou função `_padrao()`; (3) **crédito era consumido mesmo quando a geração falhava** (cliente perdia crédito sem receber nada) — agora devolve o crédito se `gerar()` lançar exceção; (4) payload do webhook com `product`/`customer` em formato inesperado (não-dict) derrubava o processamento — agora tolera
- [2026-10-21]: `_trava` virou `Semaphore` configurável (`GERACOES_SIMULTANEAS`, padrão 1) em vez de `Lock` fixo — serializar todas as gerações de todos os clientes seria um gargalo real em produção
- [2026-10-21]: limitador de tentativas (memória, por IP) em `/entrar` e `/webhook/kiwify` — eram os dois endpoints públicos sem autenticação forte

### Pending Todos (ações fora do código, não fiz por não ter acesso/credenciais)

- Escolher onde hospedar (Railway/Render/Fly/VPS) e configurar domínio com HTTPS — `Dockerfile` já pronto
- Montar volume persistente em `data/contas/` no host escolhido (senão créditos/clientes somem a cada deploy)
- Criar o produto na Kiwify (preço, planos) usando `docs/pagina-vendas.md`; configurar a URL do webhook como `https://seuservidor/webhook/kiwify?secret=<KIWIFY_WEBHOOK_SECRET>`
- Testar o webhook com uma compra real/sandbox da Kiwify e conferir os nomes de campo do payload contra `kiwify.py` (pode precisar ajustar `status`/`email`/`product_id`)
- Revisar `docs/privacidade.md` e `docs/termos.md` com advogado e preencher dados reais antes de publicar
- Definir preço dos créditos a partir do custo real por geração via `ANTHROPIC_API_KEY` (IA-01..03/COB-03 funcionam; falta medir)
- ~~Rodar a bateria de testes das Fases 2-8~~ — feito: 43 testes passando (`pytest -q`), Python 3.12 + Playwright/Chromium instalados nesta máquina em `.venv/`

### Blockers/Concerns

- Gmail OK (token.json criado 2026-10-19): 35 alertas Indeed / 169 vagas em 30 dias; nenhum alerta LinkedIn/VanHack/Turing — válido só para o uso pessoal/Fase 10, não bloqueia o produto
- Indeed responde HTTP 403 ao script → descrição colada no painel (não contornar). Filtro de relevância + dedupe prontos: 169 → 11 vagas
- Gmail OAuth para múltiplos usuários provavelmente exige verificação do Google (escopo sensível) — por isso ficou fora do produto v1
- Persistência de `data/contas/` em produção precisa de volume ou, melhor no médio prazo, um banco de dados de verdade

## Session Continuity

Last session: 2026-10-21
Stopped at: código das Fases 2-8 completo, testado (43 testes + fluxo ponta-a-ponta manual no servidor real) e com 4 bugs reais corrigidos. Falta só as ações manuais de hospedagem/Kiwify listadas acima.
Resume file: None
