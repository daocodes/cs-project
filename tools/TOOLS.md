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
| **API contract check** | Backend changes match agreed endpoints | [docs/API_CONTRACT.md](../docs/API_CONTRACT.md) (Phase 0) | Person A | — |
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
| **pytest** | Backend unit and integration tests | `cd backend && pytest` | Person A | — |
| **ruff** | Python lint + format | `cd backend && ruff check . && ruff format --check .` | Person A | — |
| **eslint** | Frontend lint | `cd frontend && npm run lint` | Person A | — |
| **TypeScript** | Frontend type check | `cd frontend && npm run typecheck` or `npx tsc --noEmit` | Person A | — |
| **GitHub Actions CI** | Lint + test on every PR | `.github/workflows/` (Phase 0 #6) | Person A | — |
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
| **Docker Compose** | Local full stack | `docker compose up` (repo root) | Person A | — |
| **AWS CLI** | Deploy, Bedrock test, RDS admin | `aws` + documented profiles | Person A | — |
| **ECS Fargate + RDS** | Production-like deploy | `docs/DEPLOY.md` (Phase 1 #11) | Person A | — |
| **GitHub CLI (`gh`)** | Issues, PRs, releases | `gh issue create`, `gh pr create` | Both | 2026-06-11 |
| **CloudWatch + Sentry** | Logs and error tracking (Phase 7) | AWS console / Sentry project | Person A | — |

---

## Local dev

| Tool | Purpose | Command / path | Owner | Last verified |
| :--- | :--- | :--- | :--- | :--- |
| **Commit template** | Consistent commit messages | `git config commit.template .gitmessage` | Both | 2026-06-11 |
| **`.env.example`** | Document required env vars | Copy to `.env` locally | Both | — |
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
| 2026-06-11 | Initial catalog — code review, testing, ML, agent, infra, local dev |
