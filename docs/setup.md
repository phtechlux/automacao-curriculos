# Setup — pendências e decisões

## Decisões
- GSD: versão leve. `PROJECT.md`, `REQUIREMENTS.md` e `STATE.md` escritos pelo Claude em `.planning/` (19/10), sem `/gsd-new-project`.
- Executar em paralelo: o usuário configura API do Claude e Gmail enquanto os arquivos do GSD são preparados.
- Preferência de interface: o usuário gosta de coisas **dinâmicas e interativas**. Priorizar um painel visual (ex.: dashboard web local com lista de vagas, filtros, status e botões de ação) em vez de saída só no terminal.

## 1. Chave da API do Claude (.env) — OPCIONAL
Sem chave, o módulo de IA usa o Claude Code instalado (`claude -p`, plano do usuário, sem custo extra). Testado em 19/10: ~45 s por vaga.
Só criar a chave se um dia quiser usar a API paga.

- Link: https://platform.claude.com/settings/keys (o antigo console.anthropic.com redireciona para o mesmo lugar)
- A API é pré-paga: é preciso comprar créditos em Billing (mínimo US$ 5) antes da chave funcionar. Créditos da API são separados da assinatura do claude.ai/Claude Code.
- Criar a chave em "Create Key", dar um nome (ex.: `job-hunter`) e copiar na hora — ela só aparece uma vez.
- Criar o arquivo `.env` na raiz do projeto:

```
ANTHROPIC_API_KEY=sk-ant-COLE_SUA_CHAVE_AQUI
```

- Garantir que `.env` está no `.gitignore`.

## 2. credentials.json do Gmail (Google Cloud Console)
1. Acessar https://console.cloud.google.com e criar um projeto novo (ex.: `job-hunter`).
2. Menu → "APIs e serviços" → "Biblioteca" → buscar **Gmail API** → **Ativar**.
3. Menu → "Google Auth Platform" (ou "Tela de consentimento OAuth"):
   - Tipo de usuário: **Externo**
   - Nome do app, e-mail de suporte e e-mail de contato: o próprio e-mail
   - Em **Público-alvo / Usuários de teste**: adicionar o próprio Gmail
   - Escopo: `https://www.googleapis.com/auth/gmail.readonly` (só leitura basta para coletar vagas)
4. Menu → "Clientes" (ou "Credenciais") → **Criar cliente OAuth** → Tipo: **App para computador (Desktop app)**.
5. Baixar o JSON, renomear para `credentials.json` e colocar na raiz do projeto.
6. Adicionar `credentials.json` e `token.json` ao `.gitignore`.
7. Na primeira execução o navegador abre pedindo login; depois disso é gerado o `token.json`. Aviso de "app não verificado" é normal: clicar em "Avançado" → "Continuar".
- Observação: com o app em modo "Teste", o token expira a cada 7 dias. Se der erro de autenticação, apagar `token.json` e logar de novo.

## 3. Currículo base — STAFFgo (feito em 19/10; falta Pedro confirmar detalhes do login e o banco de dados)
Adicionar ao currículo base, na seção de projetos/experiência (ajustar o que estiver entre colchetes):

**STAFFgo** — aplicativo em desenvolvimento ([ano de início]–atual)
- Desenvolvimento do módulo de cadastro e login de usuários, incluindo [validação de dados / autenticação / recuperação de senha].
- Tecnologias: [linguagem, framework, banco de dados].
- [Uma linha sobre o objetivo do app, ex.: plataforma para conectar profissionais temporários a empresas.]

Tarefa para o Claude Code: inserir esse bloco no currículo base mantendo o formato existente e preencher para o usuario o que está entre colchetes.

## 4.  " Deixei um TODO no arquivo. É só você me dizer o que fez que eu completo."
nao tenho dinheiro para colocar creditos para criar uma api nova, me de apenas formas de fazer isso em gastar dinheiro.
