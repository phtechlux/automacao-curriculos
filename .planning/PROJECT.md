# Automação de Currículos

## What This Is

Sistema pessoal semi-automatizado: lê alertas de vaga do Gmail, adapta o currículo base de Pedro a cada vaga via API do Claude, gera o PDF ATS-friendly e deixa a candidatura pronta (rascunho no Gmail ou formulário pausado) para ele revisar e enviar. Foco em vagas remotas e no exterior.

## Core Value

Um currículo adaptado e verdadeiro por vaga, sem trabalho manual: a IA nunca inventa fatos.

## Requirements

### Validated
- Currículo base em YAML como fonte da verdade (Fase 1)
- Template HTML de uma coluna, texto extraível por ATS (Fase 1)

### Active
- Ver REQUIREMENTS.md

### Out of Scope
- Envio automático de candidaturas: quem clica em enviar é Pedro
- Contornar anti-bot, captcha ou limites de plataforma: site bloqueado = pula a vaga
- Inventar experiência, habilidade, data ou número

## Context

- Currículo HTML antigo de duas colunas (sidebar 30/70) parseava mal em ATS; o modelo de uma coluna (ATS v8 e o do primo, aprovado na Gupy) é a referência.
- Pedro: estudante de ADS (Senac, 3º semestre), dev web júnior (React, Vite, Node.js), Brasília.
- Prefere interface interativa: painel web local em vez de só terminal.

## Constraints

- Python 3.11+ no Windows 10
- Segredos (`.env`, `credentials.json`, `token.json`) e dados pessoais (`data/curriculo_base/*`, `data/vagas/`, `output/`) fora do git
- Prompts em `prompts/`, nunca no código

## Key Decisions

| Decisão | Motivo | Resultado |
|---|---|---|
| Orquestração em script Python (n8n depois, se precisar) | Menos peças, testável | Adotado |
| Currículo base em YAML | Estruturado e fácil de editar à mão | Adotado |
| PDF via Playwright `page.pdf()` | Já é dependência; weasyprint exige GTK no Windows | Adotado, testado |
| Validação anti-invenção em código (experiências, projetos, habilidades, números) | Regra "nunca inventar" não pode depender só do prompt | Adotado, testado |
| Seção `estudando` separada das habilidades | Plano de estudo não é experiência | Adotado |
| GSD versão leve (sem `/gsd-new-project`) | Economia de tokens | Adotado em 2026-10-19 |

---
*Last updated: 2026-10-19*
