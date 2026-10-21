# Requirements

## v1 — pessoal (Pedro, local)

### Setup
- [x] **SET-01**: `pip install -e .[dev]` e `pytest` rodam
- [x] **SET-02**: currículo base em YAML, com exemplo versionado e o real fora do git

### Coleta (avançado/local — não bloqueia o produto v1, ver ENT-xx)
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
- [x] **ORQ-02**: painel web local com lista de vagas, filtros, status e botões de ação

## v2 — produto multiusuário (Kiwify)

### Entrada manual (substitui Gmail como caminho principal)
- [ ] **ENT-01**: criar vaga direto no painel colando título, empresa e descrição — sem precisar de "coletar" antes
- [ ] **ENT-02**: coleta por Gmail/fontes abertas continua disponível mas opcional, nunca bloqueia o uso

### Contas
- [ ] **CTA-01**: cadastro e login do usuário
- [ ] **CTA-02**: currículo base por conta, via formulário/upload (sem editar YAML à mão)
- [ ] **CTA-03**: vagas, PDFs e histórico isolados por conta

### Créditos e cobrança
- [ ] **COB-01**: webhook da Kiwify (compra aprovada) credita plano/créditos na conta
- [ ] **COB-02**: gerar currículo consome 1 crédito; bloqueia e avisa quando acabar
- [ ] **COB-03**: IA roda sempre via `ANTHROPIC_API_KEY` em produção (nunca `claude -p`), custo medido por geração

### Hospedagem
- [ ] **HOS-01**: painel acessível via HTTPS, não só `127.0.0.1`
- [ ] **HOS-02**: ambiente de produção com Playwright funcionando para gerar PDF

### Lançamento
- [ ] **LAN-01**: produto configurado na Kiwify (planos/créditos, preço, página de vendas)
- [ ] **LAN-02**: política de privacidade e termos de uso publicados
- [ ] **LAN-03**: fluxo pós-compra entrega acesso/login ao comprador

## Out of Scope
- Envio automático, contorno de anti-bot, invenção de fatos
- Coleta automática via Gmail para clientes do produto v1 (fica só local/pessoal)

## Traceability

| Requirement | Phase |
|---|---|
| SET-01..02 | 1 |
| ENT-01..02 | 2 |
| IA-01..03 | 3 |
| PDF-01..02 | 4 |
| CTA-01..03 | 5 |
| COB-01..03 | 6 |
| HOS-01..02 | 7 |
| LAN-01..03 | 8 |
| SUB-01..04 | 9 (futuro, uso pessoal) |
| COL-01..04 | 10 (futuro, avançado/local) |
| ORQ-01..02 | — (ORQ-02 já entregue na Fase 1-2; ORQ-01 fica para depois) |
