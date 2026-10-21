# Automação de Currículos

## What This Is

Nasceu como sistema pessoal de Pedro: lê alertas de vaga do Gmail, adapta o currículo base a cada vaga via API do Claude, gera o PDF ATS-friendly e deixa a candidatura pronta para ele revisar e enviar.

Desde 2026-10-21, em paralelo ao uso pessoal, o projeto está sendo transformado em **produto pago multiusuário**: qualquer pessoa cola seu currículo base e a descrição da vaga, recebe o PDF adaptado, pagando por crédito/plano. Lançamento inicial na Kiwify.

## Core Value

Um currículo adaptado e verdadeiro por vaga, sem trabalho manual: a IA nunca inventa fatos.

## Produto (venda)

- **Fluxo v1 de venda**: sem Gmail. Usuário cola o currículo base (formulário/upload) e cola a descrição da vaga; recebe o currículo adaptado em PDF. Evita depender de OAuth do Gmail de terceiros (ver Key Decisions).
- **Canal de lançamento**: Kiwify (checkout BR, afiliados, lançamento rápido). Reavaliar Gumroad/LemonSqueezy/Stripe direto se o volume crescer ou mirar mercado internacional.
- **Modelo de cobrança**: créditos (1 crédito = 1 currículo gerado) ou plano com limite mensal — decidir ao planejar a Fase de Créditos.
- **Gmail como recurso avançado, não bloqueador**: a coleta automática por Gmail exige que cada usuário autorize acesso à própria caixa de entrada; para múltiplos usuários isso provavelmente exige verificação do app pelo Google (processo caro/lento para escopos sensíveis). Fica como funcionalidade local/avançada, fora do produto v1.

## Requirements

### Validated
- Currículo base em YAML como fonte da verdade (Fase 1)
- Template HTML de uma coluna, texto extraível por ATS (Fase 1)

### Active
- Ver REQUIREMENTS.md

### Out of Scope
- Envio automático de candidaturas: quem clica em enviar é o usuário
- Contornar anti-bot, captcha ou limites de plataforma: site bloqueado = pula a vaga
- Inventar experiência, habilidade, data ou número
- Coleta automática via Gmail para outros usuários no produto v1 (exige verificação do Google); continua disponível como recurso local/pessoal

## Context

- Currículo HTML antigo de duas colunas (sidebar 30/70) parseava mal em ATS; o modelo de uma coluna (ATS v8 e o do primo, aprovado na Gupy) é a referência.
- Pedro: estudante de ADS (Senac, 3º semestre), dev web júnior (React, Vite, Node.js), Brasília.
- Prefere interface interativa: painel web local em vez de só terminal.

## Constraints

- Python 3.11+ no Windows 10 (dev); produção precisa de hospedagem com Playwright funcionando
- Segredos (`.env`, `credentials.json`, `token.json`) e dados pessoais (`data/curriculo_base/*`, `data/vagas/`, `output/`) fora do git
- Prompts em `prompts/`, nunca no código
- Dados pessoais de clientes pagantes (currículo, contato) exigem política de privacidade e cuidado com LGPD antes do lançamento

## Key Decisions

| Decisão | Motivo | Resultado |
|---|---|---|
| Orquestração em script Python (n8n depois, se precisar) | Menos peças, testável | Adotado |
| Currículo base em YAML | Estruturado e fácil de editar à mão | Adotado |
| PDF via Playwright `page.pdf()` | Já é dependência; weasyprint exige GTK no Windows | Adotado, testado |
| Validação anti-invenção em código (experiências, projetos, habilidades, números) | Regra "nunca inventar" não pode depender só do prompt | Adotado, testado |
| Seção `estudando` separada das habilidades | Plano de estudo não é experiência | Adotado |
| IA via Claude Code (`claude -p`) quando não há `ANTHROPIC_API_KEY` | Pedro não tem créditos de API; usa o plano que já paga | Adotado, testado 2026-10-19 |
| GSD versão leve (sem `/gsd-new-project`) | Economia de tokens | Adotado em 2026-10-19 |
| Produto v1 sem Gmail: fluxo "colar vaga" como entrada principal | Verificação do Google para OAuth do Gmail em múltiplos usuários é cara/lenta; o painel já tinha esse fallback (Indeed bloqueava scraping) | Adotado 2026-10-21 |
| Lançamento pela Kiwify | Checkout BR rápido, afiliados prontos, menor fricção pra primeiros clientes | Adotado 2026-10-21 |
| IA em produção sempre via `ANTHROPIC_API_KEY` (nunca `claude -p`) | `claude -p` depende do plano pessoal de Pedro; multiusuário precisa de custo medível por geração | Adotado 2026-10-21 |

---
*Last updated: 2026-10-21*
