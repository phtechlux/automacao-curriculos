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

Phase: 8 of 10 (Lançamento) — código das Fases 2 a 8 completo nesta sessão, sem rodar testes (combinado: testes ficam para o fim)
Plan: 0 of ? in current phase
Status: Código pronto; falta ação manual do Pedro fora do editor (ver Pending Todos) e a bateria de testes combinada
Last activity: 2026-10-21 — produto multiusuário completo: entrada manual, contas por token, créditos, webhook Kiwify, Dockerfile, páginas de vendas/termos/privacidade

Progress: [████████░░] 80%

## Accumulated Context

### Decisions

Decisions are logged in PROJECT.md Key Decisions table.

- [Phase 1]: PDF via Playwright; currículo base em YAML; validação anti-invenção em código
- [Phase 1]: `estudando` nunca vira habilidade
- [2026-10-21]: pivô de projeto pessoal para produto multiusuário vendido na Kiwify; fluxo "colar vaga" substitui Gmail como caminho principal; Gmail automático vira Fase 10 (futuro/avançado)
- [2026-10-21]: contas sem senha (token direto no link); acesso recuperado por e-mail em `/entrar`, sem precisar de serviço de e-mail transacional
- [2026-10-21]: dados de conta em arquivo JSON local (`data/contas/<token>/`), não banco de dados — simples pra validar o produto, mas **não sobrevive a redeploy sem volume persistente** (ver Hospedagem)

### Pending Todos (ações fora do código, não fiz por não ter acesso/credenciais)

- Escolher onde hospedar (Railway/Render/Fly/VPS) e configurar domínio com HTTPS — `Dockerfile` já pronto
- Montar volume persistente em `data/contas/` no host escolhido (senão créditos/clientes somem a cada deploy)
- Criar o produto na Kiwify (preço, planos) usando `docs/pagina-vendas.md`; configurar a URL do webhook como `https://seuservidor/webhook/kiwify?secret=<KIWIFY_WEBHOOK_SECRET>`
- Testar o webhook com uma compra real/sandbox da Kiwify e conferir os nomes de campo do payload contra `kiwify.py` (pode precisar ajustar `status`/`email`/`product_id`)
- Revisar `docs/privacidade.md` e `docs/termos.md` com advogado e preencher dados reais antes de publicar
- Definir preço dos créditos a partir do custo real por geração via `ANTHROPIC_API_KEY` (IA-01..03/COB-03 funcionam; falta medir)
- Rodar a bateria de testes das Fases 2-8 (combinado: só no fim do projeto)

### Blockers/Concerns

- Gmail OK (token.json criado 2026-10-19): 35 alertas Indeed / 169 vagas em 30 dias; nenhum alerta LinkedIn/VanHack/Turing — válido só para o uso pessoal/Fase 10, não bloqueia o produto
- Indeed responde HTTP 403 ao script → descrição colada no painel (não contornar). Filtro de relevância + dedupe prontos: 169 → 11 vagas
- Gmail OAuth para múltiplos usuários provavelmente exige verificação do Google (escopo sensível) — por isso ficou fora do produto v1
- Persistência de `data/contas/` em produção precisa de volume ou, melhor no médio prazo, um banco de dados de verdade

## Session Continuity

Last session: 2026-10-21
Stopped at: código das Fases 2-8 completo e commitado, sem rodar testes (combinado). Falta: ações manuais de hospedagem/Kiwify listadas acima e a bateria de testes final.
Resume file: None
