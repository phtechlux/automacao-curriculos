# Roadmap: Automação de Currículos

## Overview

Um módulo por vez, na ordem do fluxo. A partir de 2026-10-21 o projeto passou a ter dois trilhos:
uso pessoal do Pedro (já com painel funcionando) e **produto pago multiusuário**, lançado na Kiwify.
As fases abaixo priorizam o caminho mais curto até o produto vendável: entrada manual da vaga (sem
Gmail), IA com custo medível, contas, cobrança, hospedagem e lançamento. Gmail automático e submissão
assistida viram fases avançadas/futuras, não bloqueiam o lançamento.

## Phases

- [x] **Phase 1: Setup** - dependências, currículo base em YAML, testes rodando
- [ ] **Phase 2: Entrada manual** - criar vaga colando descrição, sem depender de Gmail
- [ ] **Phase 3: IA** - adaptar o currículo à vaga via Claude, sem inventar, com custo medível
- [ ] **Phase 4: PDF** - gerar o PDF ATS-friendly
- [ ] **Phase 5: Contas** - cadastro/login, currículo base por conta, dados isolados
- [ ] **Phase 6: Créditos e cobrança** - webhook Kiwify, consumo de crédito por geração
- [ ] **Phase 7: Hospedagem** - painel em servidor com HTTPS e Playwright funcionando
- [ ] **Phase 8: Lançamento** - produto na Kiwify, termos, privacidade, página de vendas
- [ ] **Phase 9 (futuro, pessoal): Submissão** - cover letter, rascunho no Gmail, formulário pausado
- [ ] **Phase 10 (futuro, avançado): Coleta automática via Gmail** - opcional, local, fora do produto v1

## Phase Details

### Phase 1: Setup
**Goal**: projeto instalável e testável, com o currículo base real de Pedro
**Requirements**: SET-01, SET-02
**Success Criteria**:
1. `pip install -e .[dev]` e `pytest` rodam (18 testes passando)
2. `curriculo.yaml` real fora do git; só o exemplo versionado
**Status**: Completo (2026-10-17)

### Phase 2: Entrada manual
**Goal**: qualquer usuário cria uma vaga colando título, empresa e descrição, sem precisar de Gmail
**Depends on**: Phase 1
**Requirements**: ENT-01, ENT-02
**Success Criteria**:
1. Painel tem ação "nova vaga" que recebe os campos colados e salva em `data/vagas/*.json`
2. Coleta por Gmail/fontes abertas continua funcionando, mas como opção, nunca obrigatória
3. Testes cobrem a vaga manual sem rede
**Notes**: o painel já aceita colar a *descrição* numa vaga existente (`/api/vagas/<id>/descricao`); falta permitir criar a vaga do zero, sem vir de uma coleta prévia.

### Phase 3: IA
**Goal**: currículo adaptado e validado para uma vaga real, com custo por geração medível
**Depends on**: Phase 2
**Requirements**: IA-01, IA-02, IA-03, COB-03
**Success Criteria**:
1. Uma vaga real gera JSON adaptado que passa na validação
2. Testes com cliente mockado cobrem invenção de experiência, projeto, habilidade e número
3. Em produção, `cliente_padrao()` sempre usa `ANTHROPIC_API_KEY` (nunca o fallback `claude -p`)
**Notes**: `adaptar()` e `validar()` já existem e já suportam API key; falta decidir e medir o custo por geração para precificar os créditos.

### Phase 4: PDF
**Goal**: PDF por vaga em `output/`
**Depends on**: Phase 3
**Requirements**: PDF-01, PDF-02
**Success Criteria**:
1. PDF gerado a partir do JSON adaptado de uma vaga real
2. `pdftotext` extrai o texto limpo e em ordem
**Notes**: já gera PDF do currículo base; falta rodar o pipeline completo com vaga real colada.

### Phase 5: Contas
**Goal**: cada usuário tem login, currículo base próprio e dados isolados
**Depends on**: Phase 4
**Requirements**: CTA-01, CTA-02, CTA-03
**Success Criteria**:
1. Cadastro/login funcionando (pode ser simples: e-mail + senha ou magic link)
2. Currículo base enviado por formulário ou upload, sem editar YAML à mão
3. Vagas, PDFs e histórico de um usuário não aparecem para outro
**Notes**: maior mudança de arquitetura do pivô — hoje tudo é arquivo local único (`data/curriculo_base/curriculo.yaml`, `data/vagas/`, sem conceito de usuário).

### Phase 6: Créditos e cobrança
**Goal**: compra na Kiwify vira créditos na conta; gerar currículo consome crédito
**Depends on**: Phase 5
**Requirements**: COB-01, COB-02
**Success Criteria**:
1. Webhook da Kiwify recebido e validado credita a conta certa
2. Painel bloqueia "gerar" e avisa quando os créditos acabam

### Phase 7: Hospedagem
**Goal**: painel acessível na internet, não só em `127.0.0.1`
**Depends on**: Phase 6
**Requirements**: HOS-01, HOS-02
**Success Criteria**:
1. Painel acessível via HTTPS num domínio
2. Geração de PDF com Playwright funcionando no ambiente de produção

### Phase 8: Lançamento
**Goal**: produto à venda na Kiwify
**Depends on**: Phase 7
**Requirements**: LAN-01, LAN-02, LAN-03
**Success Criteria**:
1. Produto/planos configurados na Kiwify com checkout funcionando
2. Política de privacidade e termos publicados
3. Comprador recebe acesso automaticamente após a compra

### Phase 9: Submissão (futuro, uso pessoal)
**Goal**: candidatura pronta para o usuário revisar e enviar
**Depends on**: Phase 4
**Requirements**: SUB-01, SUB-02, SUB-03, SUB-04
**Notes**: mantido para o uso pessoal do Pedro; não é pré-requisito do lançamento.

### Phase 10: Coleta automática via Gmail (futuro, avançado)
**Goal**: quem quiser configurar localmente continua podendo automatizar a coleta
**Depends on**: Phase 2
**Requirements**: COL-01, COL-02, COL-03, COL-04
**Notes**: código e testes já existem e já foram validados com o Gmail real do Pedro (ver STATE.md); fica fora do produto v1 por causa da verificação do Google para múltiplos usuários.

## Decisões (padrão adotado, pode mudar)

- Orquestração: script Python (`python -m curriculos`); n8n depois, se precisar.
- Currículo base: YAML em `data/curriculo_base/curriculo.yaml` (uso pessoal); no produto vira formulário/upload por conta.
- PDF: Playwright (`page.pdf()`), evita o GTK que o weasyprint exige no Windows.
- Produto v1 sem Gmail: entrada manual da vaga é o caminho principal.
- Lançamento pela Kiwify; IA em produção sempre via `ANTHROPIC_API_KEY`.

## Progress

| Phase | Plans Complete | Status | Completed |
|---|---|---|---|
| 1. Setup | 1/1 | Complete | 2026-10-17 |
| 2. Entrada manual | 0/? | Not started | - |
| 3. IA | 0/? | Not started | - |
| 4. PDF | 0/? | Not started | - |
| 5. Contas | 0/? | Not started | - |
| 6. Créditos e cobrança | 0/? | Not started | - |
| 7. Hospedagem | 0/? | Not started | - |
| 8. Lançamento | 0/? | Not started | - |
| 9. Submissão (futuro) | 0/? | Not started | - |
| 10. Coleta Gmail (futuro) | 0/? | Not started | - |
