# Requirements

## v1

### Setup
- [x] **SET-01**: `pip install -e .[dev]` e `pytest` rodam
- [x] **SET-02**: currículo base em YAML, com exemplo versionado e o real fora do git

### Coleta
- [ ] **COL-01**: OAuth do Gmail (`credentials.json` → `token.json`), escopo só leitura
- [ ] **COL-02**: buscar alertas por remetente (LinkedIn, Indeed, VanHack, Turing)
- [ ] **COL-03**: parser por fonte → `Vaga(titulo, empresa, link, descricao, fonte)` em `data/vagas/*.json`
- [ ] **COL-04**: BeautifulSoup só se a descrição do e-mail vier incompleta; site bloqueado = pula

### IA
- [ ] **IA-01**: Claude recebe currículo base + vaga e devolve currículo adaptado em JSON
- [ ] **IA-02**: validação rejeita cargo, empresa, data, projeto, habilidade ou número fora do base
- [ ] **IA-03**: currículo no idioma da vaga (pt/en)

### PDF
- [ ] **PDF-01**: gera `output/Curriculo_<Nome>_<Empresa>_<Vaga>.pdf` com o template de uma coluna
- [ ] **PDF-02**: texto do PDF extraível em ordem (ATS)

### Submissão
- [ ] **SUB-01**: cover letter com prompt em `prompts/cover_letter.md`
- [ ] **SUB-02**: vaga por e-mail → rascunho no Gmail com PDF anexado
- [ ] **SUB-03**: vaga em plataforma → Playwright preenche campos de texto e pausa
- [ ] **SUB-04**: nada é enviado automaticamente

### Orquestração
- [ ] **ORQ-01**: CLI `python -m curriculos` liga as etapas
- [ ] **ORQ-02**: painel web local com lista de vagas, filtros, status e botões de ação

## Out of Scope
- Envio automático, contorno de anti-bot, invenção de fatos

## Traceability

| Requirement | Phase |
|---|---|
| SET-01..02 | 1 |
| COL-01..04 | 2 |
| IA-01..03 | 3 |
| PDF-01..02 | 4 |
| SUB-01..04 | 5 |
| ORQ-01..02 | 6 |
