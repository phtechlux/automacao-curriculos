---
gsd_state_version: '1.0'
status: planning
progress:
  total_phases: 10
  completed_phases: 2
  total_plans: 2
  completed_plans: 2
  percent: 20
---
<!-- STATE-MD-SCHEMA:END:frontmatter -->

# Project State

## Project Reference

See: .planning/PROJECT.md (updated 2026-10-21)

**Core value:** Um currículo adaptado e verdadeiro por vaga, sem trabalho manual: a IA nunca inventa fatos.
**Current focus:** Phase 3 — IA (rodar sempre via ANTHROPIC_API_KEY em produção, medir custo por geração)

## Current Position

Phase: 3 of 10 (IA)
Plan: 0 of ? in current phase
Status: Ready to plan
Last activity: 2026-10-21 — Fase 2 concluída: botão "Nova vaga" no painel cria vaga direto (título/empresa/local/descrição), sem depender de coleta prévia nem de Gmail (painel.py `_criar`, endpoint `POST /api/vagas`)

Progress: [██░░░░░░░░] 20%

## Accumulated Context

### Decisions

Decisions are logged in PROJECT.md Key Decisions table.

- [Phase 1]: PDF via Playwright; currículo base em YAML; validação anti-invenção em código
- [Phase 1]: `estudando` nunca vira habilidade
- [2026-10-21]: pivô de projeto pessoal para produto multiusuário vendido na Kiwify; fluxo "colar vaga" substitui Gmail como caminho principal; Gmail automático vira Fase 10 (futuro/avançado)

### Pending Todos

- Fase 3: decidir preço dos créditos a partir do custo real por geração via `ANTHROPIC_API_KEY`

### Blockers/Concerns

- Gmail OK (token.json criado 2026-10-19): 35 alertas Indeed / 169 vagas em 30 dias; nenhum alerta LinkedIn/VanHack/Turing — válido só para o uso pessoal/Fase 10, não bloqueia o produto
- Indeed responde HTTP 403 ao script → descrição colada no painel (não contornar). Filtro de relevância + dedupe prontos: 169 → 11 vagas
- Gmail OAuth para múltiplos usuários provavelmente exige verificação do Google (escopo sensível) — por isso ficou fora do produto v1

## Session Continuity

Last session: 2026-10-21
Stopped at: Fase 2 codada (sem testes, conforme combinado — testes ficam para o fim do projeto); próximo passo é Fase 3 (garantir IA sempre via API key em produção)
Resume file: None
