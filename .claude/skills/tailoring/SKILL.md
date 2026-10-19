---
name: tailoring
description: Adaptar o currículo de Pedro a uma vaga específica (tailoring) neste projeto, ou melhorar o prompt/validação da etapa de IA. Use quando Pedro colar uma vaga e pedir o currículo, pedir análise de aderência/lacunas, quiser descobrir experiências não documentadas para o currículo base, ou preparar entrevista para uma vaga.
---

# Tailoring de currículo

Adaptado da skill "resume-tailoring" (original em `referencia-original.md`, só consultar se precisar de detalhe).

**Princípio:** otimizar sem mentir. Reordenar, resumir, reescrever e usar a terminologia da vaga para algo que JÁ existe em `data/curriculo_base/curriculo.yaml`. Nunca inventar cargo, empresa, data, habilidade, projeto ou número.

## Regras do projeto (vencem a skill original)
- Cargo, empresa e datas: **exatamente** como no base. Sem "reframing" de título.
- `estudando` nunca vira habilidade; no máximo "em estudo" no resumo.
- Saída é o PDF do pipeline (`templates/curriculo.html`), não DOCX.
- Pesquisa web da empresa: no máximo 1–2 buscas, só se a vaga for vaga demais. Sem varrer perfis do LinkedIn.
- Nada é enviado automaticamente.

## Fluxo

### 1. Ler a vaga → perfil de sucesso
Extrair: requisitos obrigatórios, diferenciais, palavras-chave (escritas como a vaga escreve), senioridade, idioma, sinais de cultura, alertas (ex.: exige experiência que Pedro não tem).

### 2. Casar com o currículo base (nota por item)
Para cada requisito, procurar o melhor fato no base e classificar:
- **DIRETO (90–100%)**: mesma tecnologia/atividade.
- **TRANSFERÍVEL (75–89%)**: mesma capacidade, outro contexto (ex.: atendimento ao público → suporte a usuários).
- **ADJACENTE (60–74%)**: ferramenta ou área vizinha.
- **LACUNA (<60%)**: não existe no base. Não forçar.

Peso sugerido: direto 40%, transferível 30%, adjacente 20%, tipo de impacto 10%. Cobertura da vaga = média dos requisitos obrigatórios.

### 3. Reescrever com verdade
Estratégias permitidas: alinhar termos (mesmo significado, palavra da vaga), mudar a ênfase (mesmos fatos), ajustar o nível técnico, destacar o aspecto relevante. Para cada reescrita relevante, saber dizer por que é verdadeira.

### 4. Lacunas
Para cada LACUNA em requisito obrigatório, escolher: omitir, mencionar "em estudo" (só se estiver em `estudando`), citar na cover letter, ou rodar a descoberta (passo 5).

### 5. Descoberta de experiências (opcional, conversa com Pedro)
Só quando houver lacunas importantes. Perguntas curtas e ramificadas:
- "Você já usou {skill}?" → SIM: onde, quando, escala, resultado, foi em produção? → INDIRETO: qual era seu papel? → NÃO: algo parecido?
- Pedir números só se ele souber; nunca estimar por ele.
- O que Pedro confirmar entra no `curriculo.yaml` (fonte da verdade). Não colocar nada que ele não confirmou.

### 6. Relatório (curto)
Cobertura %, quantos itens diretos/transferíveis/adjacentes, lacunas, reescritas principais, 2–3 histórias para preparar na entrevista.

## Onde isso vive no código
- Etapa automática: `prompts/adaptar_curriculo.md` (o prompt pede `analise` com cobertura, lacunas e preparação) + `src/curriculos/ia/__init__.py` (`validar` barra invenção).
- O painel (`python -m curriculos`) mostra a análise depois de gerar.
- Ao mudar o prompt, rodar `pytest` e gerar uma vaga real para conferir.
