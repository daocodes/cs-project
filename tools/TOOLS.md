# Tools Catalog

Living reference for tools used during InternBase development — code review, testing, ML, agent work, infra, and local dev. **Update this file when you add or verify a tool.**

Conventions: [docs/GITHUB_CONVENTIONS.md](../docs/GITHUB_CONVENTIONS.md) · Backlog: [docs/PROJECT.md](../docs/PROJECT.md)

---

## How to use this doc

1. Pick the category that matches your task
2. Run the tool before opening a PR (where applicable)
3. When adding a tool, copy the **Add a tool** template at the bottom
4. Set **Last verified** when you confirm it still works

---

## Code review

| Tool | Purpose | Command / path | Owner | Last verified |
| :--- | :--- | :--- | :--- | :--- |
| **Partner PR review** | Required human review per working agreements | GitHub PR → assign partner reviewer | Both | — |
| **PR template checklist** | Standard review gates | [.github/pull_request_template.md](../.github/pull_request_template.md) | Both | 2026-06-11 |
| **API contract check** | Backend changes match agreed endpoints | [docs/API_CONTRACT.md](../docs/API_CONTRACT.md) (Phase 0) | Person A | 2026-06-18 |
| **Scope gate** | Changes trace to PROJECT.md | [docs/PROJECT.md](../docs/PROJECT.md) | Both | 2026-06-11 |

### Reviewer focus areas

| Area | Look for |
| :--- | :--- |
| `area:frontend` | IDE layout, a11y basics, loading/error states, no secrets in client bundle |
| `area:backend` | Pydantic validation, auth on routes, pytest coverage, migration safety |
| `area:ml` | No PII in datasets, reproducible scripts, inference latency |
| `area:agent` | Tool schemas, HITL paths, prompt version tracked, trace logged |
| `area:infra` | IAM least privilege, no keys in repo, cost impact noted |

---

## Testing

| Tool | Purpose | Command / path | Owner | Last verified |
| :--- | :--- | :--- | :--- | :--- |
| **pytest** | Backend unit and integration tests | `cd backend && source .venv/bin/activate && python -m pytest` | Person A | 2026-06-17 |
| **ruff** | Python lint + format | `cd backend && source .venv/bin/activate && python -m ruff check . && python -m ruff format --check .` | Person A | 2026-06-17 |
| **eslint** | Frontend lint | `cd frontend && npm run lint` | Person A | 2026-06-17 |
| **TypeScript** | Frontend type check | `cd frontend && npm run typecheck` or `npx tsc --noEmit` | Person A | 2026-06-17 |
| **GitHub Actions CI** | Lint + test on every PR | `.github/workflows/` (Phase 0 #6) | Person A | 2026-06-25 |
| **Agent eval smoke** | 5 golden tasks on agent-touched PRs | `cd backend && python -m eval.run --smoke` (Phase 6 #35) | Person B | — |
| **Agent eval full** | Weekly full golden set | `python -m eval.run --full` | Person B | — |

---

## ML

| Tool | Purpose | Command / path | Owner | Last verified |
| :--- | :--- | :--- | :--- | :--- |
| **spaCy** | Skill extractor baseline (Phase 1) | `backend/ml/skill_extractor/` | Person B | — |
| **sentence-transformers** | Embedding matcher (Phase 2) | `backend/ml/matcher/` | Person B | — |
| **PyTorch / Hugging Face** | Model training and export | `backend/ml/` | Person B | — |
| **JD + email datasets** | Training data | `backend/data/jds/`, `backend/data/emails/` | Person B | — |
| **MLflow or S3 registry** | Model artifact tracking (optional v1) | TBD Phase 2+ | Person B | — |

---

## Agent

| Tool | Purpose | Command / path | Owner | Last verified |
| :--- | :--- | :--- | :--- | :--- |
| **LangGraph** | Agent orchestration state machine | `backend/agent/` | Person B | — |
| **LlamaIndex + pgvector** | RAG over resumes and JDs | `backend/agent/rag/` | Person B | — |
| **Amazon Bedrock** | LLM inference (agent + tailoring) | `LLMProvider` / `BedrockProvider` | Person A | — |
| **Versioned prompts** | Prompt engineering artifacts | `prompts/` | Person B | — |
| **Golden task harness** | Eval against agent behaviors | `eval/golden_tasks.json`, `eval/run.py` | Person B | — |
| **Gmail MCP server** | Email tool via MCP (post–Jul 10) | `backend/mcp/gmail/` | Person B | — |

---

## Infra

| Tool | Purpose | Command / path | Owner | Last verified |
| :--- | :--- | :--- | :--- | :--- |
| **Docker Compose** | Local full stack | `docker compose up --build` (repo root) | Person A | 2026-06-17 |
| **AWS CLI** | Deploy, Bedrock test, RDS admin | `aws` + documented profiles | Person A | — |
| **ECS Fargate + RDS** | Production-like deploy | `docs/DEPLOY.md` (Phase 1 #11) | Person A | — |
| **GitHub CLI (`gh`)** | Issues, PRs, releases | `gh issue create`, `gh pr create` | Both | 2026-06-11 |
| **CloudWatch + Sentry** | Logs and error tracking (Phase 7) | AWS console / Sentry project | Person A | — |
| **Alembic** | Database schema migrations and revision history | `cd backend && source .venv/bin/activate && python -m alembic revision --autogenerate -m "msg" && python -m alembic upgrade head` | Person A | 2026-06-18 |

---

## Local dev

| Tool | Purpose | Command / path | Owner | Last verified |
| :--- | :--- | :--- | :--- | :--- |
| **Commit template** | Consistent commit messages | `git config commit.template .gitmessage` | Both | 2026-06-11 |
| **`.env.example`** | Document required env vars | Copy to `.env` locally | Both | 2026-06-17 |
| **Backend dev venv** | Install backend lint/test deps locally | `cd backend && python3 -m venv .venv && source .venv/bin/activate && python -m pip install -r requirements-dev.txt` | Person A | 2026-06-17 |
| **Bedrock dev fallback** | Local dev without AWS | `BEDROCK_ENABLED=false` | Person A | — |
| **Monaco / IDE shell** | Resume diff, agent output | `frontend/` components | Person A | — |

---

## Add a tool

When you adopt a new tool, append a row to the right category:

```markdown
| **Tool name** | One-line purpose | `command` or `path/` | Person A/B | YYYY-MM-DD |
```

Also update **Last verified** on any row you re-tested.

### Changelog

| Date | Change |
| :--- | :--- |
| 2026-06-25 | Updated frontend CI install step in `.github/workflows/ci.yml` from `npm ci` to `npm install` to prevent lockfile sync failures; re-verified frontend checks (`npm run lint`, `npm run typecheck`) |
| 2026-06-18 | Added `docs/API_CONTRACT.md` for Phase 1 endpoint contract, verified API contract review gate, and added Alembic migration command workflow to Infra tools |
| 2026-06-17 | Verified Docker Compose local stack (`frontend` + `backend` + `postgres`), updated Compose command to `docker compose up --build`, verified `.env.example`, and verified frontend/backend pre-PR checks (`typecheck`, `eslint`, `ruff`, `pytest`) |
| 2026-06-11 | Initial catalog — code review, testing, ML, agent, infra, local dev |
