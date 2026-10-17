# Projeto: Automação de Submissão de Currículos (IA + Web Automation)

## Objetivo
Criar um sistema semi-automatizado que coleta vagas recebidas por e-mail, utiliza IA para reescrever um currículo base de acordo com os requisitos da vaga, gera um PDF e prepara a submissão (via e-mail ou preenchimento parcial no navegador). Foco principal em vagas remotas e oportunidades no exterior (Visa Sponsorship / Relocation).

## Arquitetura e Tecnologias Sugeridas

### 1. Coleta de Vagas e Gatilho (Trigger)
*   **Ação:** Monitorar a caixa de entrada do Gmail por alertas de vagas (LinkedIn, Indeed, VanHack, Turing).
*   **Ferramentas:**
    *   `n8n` (Nó do Gmail + IMAP) para orquestração visual rápida, OU
    *   `Python` (Gmail API) integrado em um script contínuo.
*   **Saída Esperada:** Link da vaga, título e texto descritivo extraído (usando `BeautifulSoup` para raspar a página do link, se necessário).

### 2. O Cérebro: Análise e Adaptação (Claude API)
*   **Ação:** Cruzar o currículo base com os requisitos da vaga capturada.
*   **Ferramenta:** API do Claude (Anthropic).
*   **Prompt System:**
    *   *Input A:* Currículo Pai (JSON ou Markdown).
    *   *Input B:* Descrição da vaga.
    *   *Comando:* "Reescreva o Resumo Profissional e destaque as experiências do Currículo Pai que possuem maior "match" com a Vaga B. Otimize para ATS (Applicant Tracking Systems). Retorne exclusivamente em Markdown."

### 3. Geração do Documento (PDF)
*   **Ação:** Converter a resposta gerada pela IA em um documento pronto para envio.
*   **Ferramentas:**
    *   `Python` com bibliotecas `markdown2` (para converter MD para HTML) e `pdfkit` ou `weasyprint` (HTML para PDF).
*   **Saída Esperada:** Arquivo `Curriculo_SeuNome_Empresa_Vaga.pdf`.

### 4. Preparo de Submissão (Ação Final)
Para evitar bloqueios de sistemas anti-bot (Cloudflare) e banimentos nas plataformas:
*   **Cenário A (Vagas por E-mail):** 
    *   Gerar "Cover Letter" com IA.
    *   Criar um rascunho no Gmail com o PDF anexado, pronto para envio manual.
*   **Cenário B (Plataformas Web):**
    *   Ferramenta: `Python` + `Playwright` ou `Selenium`.
    *   Ação: O script abre o navegador no perfil logado, navega até a URL da vaga, preenche os campos de texto suportados e pausa a execução para o upload manual do PDF gerado.

## Workflow de Desenvolvimento Recomendado (com Claude Code e GSD)
Utilize a metodologia do framework **GSD Core** (`open-gsd/gsd-core`) para conduzir a construção junto com a IA:
1.  **Fase de Especificação (`/gsd-new-project`):** Defina todo esse Markdown lá dentro para o Claude criar a "Spec" inicial.
2.  **Fase de Pesquisa:** Peça ao Claude para investigar a API do Gmail e criar provas de conceito (PoC) para o web scraping das vagas.
3.  **Fase de Execução:** Divida o trabalho em módulos (Módulo 1: Leitor de Email. Módulo 2: Prompt e API. Módulo 3: Gerador de PDF. Módulo 4: Playwright).

## Dicas para Vagas Internacionais
*   Configure os filtros de pesquisa dos alertas de emprego para termos específicos: `Visa Sponsorship`, `Relocation Assistance`, `Remote (Worldwide)`.
*   Priorize desenvolver o script de automação web para sites focados em tech internacional, que costumam ter formulários mais amigáveis e diretos que o LinkedIn (ex: VanHack, Turing, Wellfound).