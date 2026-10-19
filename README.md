# Job Application Automation

> Reads job alerts from Gmail, tailors my resume to each job with Claude and prepares the application — **I review and click send.**

![Python](https://img.shields.io/badge/-Python_3.11-3776AB?style=flat-square&logo=python&logoColor=white)
![Claude](https://img.shields.io/badge/-Claude_API-D97757?style=flat-square&logo=claude&logoColor=white)
![Gmail API](https://img.shields.io/badge/-Gmail_API-EA4335?style=flat-square&logo=gmail&logoColor=white)
![Playwright](https://img.shields.io/badge/-Playwright-2EAD33?style=flat-square&logo=playwright&logoColor=white)
![Status](https://img.shields.io/badge/status-in_progress-yellow?style=flat-square)

Personal project focused on remote and international roles (Visa Sponsorship, Relocation, Remote Worldwide).

## How it works

```
Gmail job alerts ──► Collect ──► Tailor (Claude) ──► PDF ──► Draft / paused form
 LinkedIn, Indeed,    filter +    rewrite summary,    ATS-     I review
 VanHack, Turing      dedupe      reorder bullets     friendly  and send
```

1. **Collect** — reads job alerts via the Gmail API, extracts title, link and description, filters out irrelevant jobs and removes duplicates.
2. **Tailor** — Claude crosses the base resume with the job description: rewrites the summary, highlights the best-matching experience and optimizes for ATS.
3. **PDF** — renders an HTML template and exports `Curriculo_<Name>_<Company>_<Job>.pdf` with Playwright.
4. **Submit** — creates a Gmail **draft** with the PDF attached, or fills a job form in the browser and **pauses** for me.

All of it is driven from a **local web panel**.

## Design rules

- **The AI never invents experience.** It can only reorder, summarize and rewrite what is in the base resume. A validation step in code rejects skills, dates or numbers that are not there.
- **Nothing is sent automatically.** The flow stops at a draft or a paused form.
- **No anti-bot bypassing.** If a site blocks automation (Cloudflare, captcha), the job is skipped.
- **Secrets and personal data stay out of git** — `.env`, Gmail tokens, collected jobs and generated PDFs are ignored.
- Prompts live in [`prompts/`](prompts/), not hardcoded.

## Status

| Module | Status |
|---|---|
| Setup, base resume in YAML, tests | ✅ |
| Collect (Gmail, filter, dedupe) | ✅ working, being refined |
| Local web panel (paste a job → PDF) | ✅ |
| PDF export (Playwright) | ✅ |
| Tailoring with Claude + anti-fabrication validation | 🚧 |
| Gmail draft + cover letter / paused browser form | ⏳ |

## Run locally

```bash
pip install -e .[dev]
playwright install chromium
cp .env.example .env        # optional: ANTHROPIC_API_KEY (without it, uses the local Claude Code CLI)
cp data/curriculo_base/curriculo.exemplo.yaml data/curriculo_base/curriculo.yaml

python -m curriculos painel     # local web panel
python -m curriculos coletar 7  # collect alerts from the last 7 days
pytest
```

Gmail setup (`credentials.json`): see [docs/setup.md](docs/setup.md). Architecture: [docs/arquitetura.md](docs/arquitetura.md).

## Project structure

```
src/curriculos/   coleta (collect) · ia (tailoring) · pdf · submissao (submit) · painel (web panel)
prompts/          prompts sent to Claude
templates/        HTML templates (resume, panel)
tests/            pytest
```

---

Built by [Pedro Henrique](https://github.com/phtechlux) with Claude Code as a development partner.
