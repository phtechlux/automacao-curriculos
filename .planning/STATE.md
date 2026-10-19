---
gsd_state_version: '1.0'
status: planning
progress:
  total_phases: 6
  completed_phases: 1
  total_plans: 1
  completed_plans: 1
  percent: 17
---
<!-- STATE-MD-SCHEMA:END:frontmatter -->

# Project State

## Project Reference

See: .planning/PROJECT.md (updated 2026-10-19)

**Core value:** Um currículo adaptado e verdadeiro por vaga, sem trabalho manual: a IA nunca inventa fatos.
**Current focus:** Phase 2 — Coleta

## Current Position

Phase: 2 of 6 (Coleta)
Plan: 0 of ? in current phase
Status: Ready to plan
Last activity: 2026-10-19 — IA via Claude Code (sem API paga) testada com vaga de exemplo → PDF

Progress: [██░░░░░░░░] 17%

## Accumulated Context

### Decisions

Decisions are logged in PROJECT.md Key Decisions table.

- [Phase 1]: PDF via Playwright; currículo base em YAML; validação anti-invenção em código
- [Phase 1]: `estudando` nunca vira habilidade

### Pending Todos

None yet.

### Blockers/Concerns

- Gmail OK (token.json criado 2026-10-19): 35 alertas Indeed / 169 vagas em 30 dias; nenhum alerta LinkedIn/VanHack/Turing
- Indeed responde HTTP 403 ao script e o e-mail só traz título/empresa/local → sem descrição. Não contornar. Plano: painel com "abrir vaga" + colar descrição; filtro de relevância e dedupe

## Session Continuity

Last session: 2026-10-19
Stopped at: coleta real do Gmail funcionando; decidir como obter a descrição das vagas do Indeed
Resume file: None
