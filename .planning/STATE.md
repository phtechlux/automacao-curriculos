---
gsd_state_version: '1.0'
status: planning
progress:
  total_phases: 10
  completed_phases: 1
  total_plans: 1
  completed_plans: 1
  percent: 10
---
<!-- STATE-MD-SCHEMA:END:frontmatter -->

# Project State

## Project Reference

See: .planning/PROJECT.md (updated 2026-10-21)

**Core value:** Um currículo adaptado e verdadeiro por vaga, sem trabalho manual: a IA nunca inventa fatos.
**Current focus:** Phase 2 — Entrada manual (pivô: produto multiusuário, lançamento na Kiwify, sem depender de Gmail)

## Current Position

Phase: 2 of 10 (Entrada manual)
Plan: 0 of ? in current phase
Status: Ready to plan
Last activity: 2026-10-21 — pivô para produto pago (Kiwify, fluxo "colar vaga" sem Gmail); roadmap e requirements reescritos

Progress: [█░░░░░░░░░] 10%

## Accumulated Context

### Decisions

Decisions are logged in PROJECT.md Key Decisions table.

- [Phase 1]: PDF via Playwright; currículo base em YAML; validação anti-invenção em código
- [Phase 1]: `estudando` nunca vira habilidade
- [2026-10-21]: pivô de projeto pessoal para produto multiusuário vendido na Kiwify; fluxo "colar vaga" substitui Gmail como caminho principal; Gmail automático vira Fase 10 (futuro/avançado)

### Pending Todos

- Fase 2: permitir criar vaga do zero colando título/empresa/descrição no painel (hoje só existe colar *descrição* numa vaga já coletada)
- Fase 3: decidir preço dos créditos a partir do custo real por geração via `ANTHROPIC_API_KEY`

### Blockers/Concerns

- Gmail OK (token.json criado 2026-10-19): 35 alertas Indeed / 169 vagas em 30 dias; nenhum alerta LinkedIn/VanHack/Turing — válido só para o uso pessoal/Fase 10, não bloqueia o produto
- Indeed responde HTTP 403 ao script → descrição colada no painel (não contornar). Filtro de relevância + dedupe prontos: 169 → 11 vagas
- Gmail OAuth para múltiplos usuários provavelmente exige verificação do Google (escopo sensível) — por isso ficou fora do produto v1

## Session Continuity

Last session: 2026-10-21
Stopped at: planejamento do pivô concluído (PROJECT/REQUIREMENTS/ROADMAP/STATE atualizados); próximo passo é codar a Fase 2 (criar vaga colando descrição, sem precisar de coleta prévia)
Resume file: None
