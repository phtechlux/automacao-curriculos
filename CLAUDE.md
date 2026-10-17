# Automação de Currículos

Projeto pessoal. Sistema semi-automatizado que lê alertas de vagas do Gmail, usa a API do Claude para adaptar um currículo base a cada vaga, gera o PDF e deixa a candidatura pronta para eu revisar e enviar.

Foco: vagas remotas e no exterior (Visa Sponsorship, Relocation, Remote Worldwide).

Arquitetura completa: [docs/arquitetura.md](docs/arquitetura.md)

## Fluxo

1. **Coleta** (`src/curriculos/coleta/`): ler alertas de vaga no Gmail (LinkedIn, Indeed, VanHack, Turing) e extrair link, título e descrição. Usar BeautifulSoup só quando o texto do e-mail não bastar.
2. **IA** (`src/curriculos/ia/`): cruzar o currículo base com a vaga via API do Claude, reescrever o resumo profissional, destacar as experiências com mais "match" e otimizar para ATS.
3. **PDF** (`src/curriculos/pdf/`): converter o resultado em `Curriculo_<Nome>_<Empresa>_<Vaga>.pdf` usando os templates em `templates/`.
4. **Submissão** (`src/curriculos/submissao/`):
   - Vaga por e-mail: gerar cover letter e criar um **rascunho** no Gmail com o PDF anexado.
   - Vaga em plataforma: abrir o navegador com Playwright, preencher os campos de texto e **pausar** para eu enviar o PDF manualmente.

## Regras

- **Nunca inventar experiência.** A IA só pode reordenar, resumir e reescrever o que existe no currículo base. Nada de habilidades, cargos, datas ou números que não estejam lá.
- **Nada é enviado automaticamente.** O sistema para em rascunho ou em formulário pausado; quem clica em enviar sou eu.
- **Sem burlar anti-bot.** Não contornar Cloudflare, captcha ou limites das plataformas. Se um site bloquear, pular a vaga.
- **Segredos fora do git.** Chave da API e tokens do Gmail ficam em `.env`, `credentials.json` e `token.json`, todos no `.gitignore`. Use `.env.example` como modelo.
- **Dados pessoais fora do git.** Vagas coletadas (`data/vagas/`) e PDFs gerados (`output/`) não são versionados.
- Prompts ficam em arquivos dentro de `prompts/`, não escritos direto no código.

## Estrutura

```
data/curriculo_base/   currículo base (fonte da verdade)
data/vagas/            vagas coletadas (não versionado)
docs/                  arquitetura e decisões
output/                PDFs e cover letters gerados (não versionado)
prompts/               prompts enviados ao Claude
templates/             templates HTML do currículo e da cover letter
src/curriculos/        código: coleta, ia, pdf, submissao
tests/                 testes
.planning/             planejamento do GSD (PROJECT, ROADMAP, fases)
```

## Stack

- Python 3.11+ (Windows 10)
- Gmail API
- API do Claude (Anthropic SDK)
- BeautifulSoup para scraping
- Playwright para o navegador
- Markdown/HTML → PDF (biblioteca a definir)

## Decisões em aberto

- Orquestração: script Python ou n8n.
- Formato do currículo base: JSON, YAML ou Markdown.
- Geração de PDF: weasyprint, pdfkit ou o próprio Playwright.

## Como trabalhamos

O projeto é conduzido com GSD Core. Fases e planos ficam em `.planning/`. Construir um módulo por vez, na ordem do fluxo acima, e testar cada módulo isolado antes de ligar ao próximo.
