# Roadmap: Automação de Currículos

## Overview

Um módulo por vez, na ordem do fluxo, testado isolado. Revisão curta ao fim de cada fase; revisão completa só na Fase 6.

## Phases

- [x] **Phase 1: Setup** - dependências, currículo base em YAML, testes rodando
- [ ] **Phase 2: Coleta** - ler alertas de vaga do Gmail
- [ ] **Phase 3: IA** - adaptar o currículo à vaga via Claude, sem inventar
- [ ] **Phase 4: PDF** - gerar o PDF ATS-friendly
- [ ] **Phase 5: Submissão** - cover letter, rascunho no Gmail, formulário pausado
- [ ] **Phase 6: Orquestração e painel** - CLI e painel web local que ligam tudo

## Phase Details

### Phase 1: Setup
**Goal**: projeto instalável e testável, com o currículo base real de Pedro
**Requirements**: SET-01, SET-02
**Success Criteria**:
1. `pip install -e .[dev]` e `pytest` rodam (18 testes passando)
2. `curriculo.yaml` real fora do git; só o exemplo versionado

### Phase 2: Coleta
**Goal**: vagas reais do Gmail salvas em `data/vagas/*.json`
**Depends on**: Phase 1
**Requirements**: COL-01, COL-02, COL-03, COL-04
**Success Criteria**:
1. OAuth funciona e gera `token.json`
2. Alertas reais de pelo menos uma fonte viram `Vaga` com título, empresa, link e descrição
3. Testes com e-mails de exemplo, sem rede
**Notes**: código e testes com dados de exemplo já existem; falta rodar com Gmail real.

### Phase 3: IA
**Goal**: currículo adaptado e validado para uma vaga real
**Depends on**: Phase 2
**Requirements**: IA-01, IA-02, IA-03
**Success Criteria**:
1. Uma vaga real gera JSON adaptado que passa na validação
2. Testes com cliente mockado cobrem invenção de experiência, projeto, habilidade e número
**Notes**: código e testes mockados já existem; falta chamada real (precisa de `.env`).

### Phase 4: PDF
**Goal**: PDF por vaga em `output/`
**Depends on**: Phase 3
**Requirements**: PDF-01, PDF-02
**Success Criteria**:
1. PDF gerado a partir do JSON adaptado de uma vaga real
2. `pdftotext` extrai o texto limpo e em ordem
**Notes**: já gera PDF do currículo base.

### Phase 5: Submissão
**Goal**: candidatura pronta para Pedro revisar e enviar
**Depends on**: Phase 4
**Requirements**: SUB-01, SUB-02, SUB-03, SUB-04

### Phase 6: Orquestração e painel
**Goal**: um comando e um painel web local para o fluxo inteiro
**Depends on**: Phase 5
**Requirements**: ORQ-01, ORQ-02

## Decisões (padrão adotado, pode mudar)

- Orquestração: script Python (`python -m curriculos`); n8n depois, se precisar.
- Currículo base: YAML em `data/curriculo_base/curriculo.yaml`.
- PDF: Playwright (`page.pdf()`), evita o GTK que o weasyprint exige no Windows.

## Progress

| Phase | Plans Complete | Status | Completed |
|---|---|---|---|
| 1. Setup | 1/1 | Complete | 2026-10-17 |
| 2. Coleta | 0/? | Not started | - |
| 3. IA | 0/? | Not started | - |
| 4. PDF | 0/? | Not started | - |
| 5. Submissão | 0/? | Not started | - |
| 6. Orquestração e painel | 0/? | Not started | - |
