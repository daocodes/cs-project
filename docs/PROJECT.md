# InternBase - Project Ground Truth

* **Working Title:** See [Open Decisions](#16-open-decisions). The "home base for CS students in recruiting."
* **Purpose of this Document:** This document is the single source of truth for the project. Every GitHub issue should trace back to something here. If reality diverges from this doc, update the doc in the same PR. GitHub workflow: [GITHUB_CONVENTIONS.md](GITHUB_CONVENTIONS.md) · Tools: [tools/TOOLS.md](../tools/TOOLS.md)

---

## Recent Changes

Last updated: 2026-06-25

### Completed now

- Phase 0 / Issue #1 ("Monorepo + Docker Compose local dev") is implemented and validated.
- Added monorepo local-dev scaffold at repo root with:
  - `docker-compose.yml`
  - `frontend/` (Next.js + TypeScript baseline)
  - `backend/` (FastAPI baseline)
- Docker local stack now starts frontend, backend, and Postgres with one command: `docker compose up --build`.
- Health checks verified:
  - Frontend: `GET /api/health`
  - Backend: `GET /health`
- Added local environment templates and docs:
  - `.env.example`
  - `README.md` one-command startup instructions
- Backend dependencies are now correctly scoped to `backend/requirements.txt` (no root Python requirements file).
- Added `docs/API_CONTRACT.md` with the Phase 1 Tracker API contract (health + applications CRUD + status history).
- Added core SQLAlchemy tracker models and Alembic project wiring for migrations.
- Added GitHub Actions CI workflow at `.github/workflows/ci.yml` for backend (`ruff` + `pytest`) and frontend (`eslint` + `typecheck`) PR checks.
- Added backend smoke test `backend/tests/test_health.py` so CI `pytest` has a real test target.
- Updated frontend CI install step from `npm ci` to `npm install` to avoid lockfile drift failures caused by transitive dependency metadata changes.
- Revalidated frontend CI commands locally: `npm install`, `npm run lint`, and `npm run typecheck` all pass.

### Where to continue next

- Phase 0 is complete (Issues #1-#6 accepted).
- Continue with Phase 1 tracker MVP work (`#7` onward).

---

## 1. One-liner

An IDE-shaped command center for CS students during internship recruiting: track applications, discover tailored internships, close skill gaps with a prep roadmap, and orchestrate it all through a production-style AI agent—built on our own ML models, LangGraph orchestration, RAG, MCP, and AWS Bedrock.

---

## 2. Why this Exists (Goals, in Priority Order)

This ordering decides every trade-off. When two choices conflict, the higher-ranked goal wins.

1. **Learn ML / AWS / Agentic AI Deeply:** Fine-tune our own models (not API-only), build a real agent platform (LangGraph, RAG, MCP, eval harness), and stand up AWS infrastructure including Bedrock. *"There's a library that does this"* is not a reason to skip building it ourselves—for orchestration we use LangGraph/LlamaIndex intentionally (job-relevant); for intelligence the matcher and classifiers are ours.
2. **Strongest Possible Portfolio Piece:** Must defend **two stories** in interviews—**SWE** (FastAPI, Next.js, Postgres, CI/CD, AWS) and **Agentic AI** (planning, tool-use, RAG, MCP, prompt engineering, eval). IDE-lite UI and agent trace panel demonstrate frontend craft and orchestration observability.
3. **Actually Usable for Our Own Recruiting:** Nice-to-have. Rough-but-working beats polished-but-late. We'll use it ourselves this fall, but reliability/polish is not allowed to block goals 1 and 2.

---

## 3. Non-Goals (Explicitly Out of Scope)

* **Not a startup / not a public launch:** No marketing, no scale beyond a handful of test users. (Stays in Gmail OAuth "testing mode" to avoid expensive restricted-scope security review).
* **Not claiming novelty:** This category is crowded (Simplify, Teal, Jobscan, G-Track, etc.). We're rebuilding it to learn and go deeper technically—that's the honest pitch.
* **No multi-tenant scale, billing, or teams in v1:** Single-user-focused. Friends can test lightly; public launch is out of scope.
* **No mobile app or browser extension in v1:** Web app only.
* **No full VS Code clone in v1:** IDE-lite only (theme, sidebar, split panels, Monaco)—no LSP, extensions, or embedded terminal.
* **No LLM-generated roadmaps or project ideation studio in v1:** Lightweight preset roadmaps in v1; full roadmap engine + project studio in v2.

---

## 4. Users

CS students (initially: us) in internship recruiting who currently juggle a spreadsheet, a dozen browser tabs, and an inbox full of "we regret to inform you."

---

## 5. Scope

### v1 — Eight Subsystems (sequenced; each independently complete)

1. **Tracker:** CRUD over applications: status pipeline, dates, notes, linked resume version, deadline reminders, CSV export.
2. **Resume Matcher:** Parse resume + job description, score the match, surface matched vs missing skills (our model).
3. **Resume Tailoring:** Bedrock rewrites bullets guided by matcher output; no fabrication; user approves each edit (Monaco diff UI).
4. **Internship Aggregation:** Scheduled scrapers pull new postings, normalize + dedupe, into a personalized discovery feed.
5. **Email Status Detection:** Read inbox, classify recruiting emails, auto-update matching application (our model + our MCP server).
6. **Lightweight Roadmap:** Preset checklists (LeetCode, courses, skill gaps synced from matcher) per target role.
7. **Agent Platform:** LangGraph orchestration, RAG, MCP, versioned prompts, eval harness—delivered incrementally (one tool per phase).
8. **AI Agent Chat:** Orchestrates all tools through IDE chat + trace panel.

### v2 — Future

* **Project Ideation Studio:** JD-matched project ideas, startup problem finder, creative iteration chat.
* **Full Roadmap Engine:** LLM-generated personalized roadmaps from free-text goals.
* **Multi-agent coordinator** for complex workflows.
* Optional browser extension for autofill.

---

## 6. Agent Architecture

The agent platform is the **technical thesis**; recruiting features are the **domain**.

### Capabilities (mapped to agentic-AI job requirements)

| JD skill | Our implementation |
| :--- | :--- |
| Planning & reasoning | LangGraph state machine: plan → retrieve → act → observe → replan |
| Tool-use | 8 LangGraph tools backed by our APIs and models |
| RAG | LlamaIndex + pgvector over JDs, resumes, roadmap content |
| MCP | Custom Gmail MCP server; agent connects via MCP protocol |
| Prompt engineering | Versioned `prompts/` files; `PromptVersion` tracked per `AgentRun` |
| Testing & evaluation | Golden-set harness (20–30 tasks); metrics in README |
| Orchestration frameworks | LangGraph (not a black-box chatbot wrapper) |

### Agent tools (v1)

| Tool | Backed by |
| :--- | :--- |
| `search_internships` | Aggregation + user preferences |
| `score_resume_match` | Embedding matcher |
| `tailor_resume` | Matcher + Bedrock (HITL approval) |
| `update_application` | Tracker CRUD |
| `get_roadmap_gaps` | Roadmap + matcher |
| `search_knowledge` | RAG over indexed docs |
| `read_email_status` | Gmail MCP + email classifier |
| `get_weekly_plan` | Roadmap + tracker state |

### Memory

* **Short-term:** LangGraph checkpoint / Postgres checkpointer (conversation + plan state).
* **Long-term:** `agent_memory` table (goals, preferred companies, past actions).

### Safety / HITL

* Resume tailoring: user approves every edit.
* Email status: low classifier confidence → `needs_confirmation`.
* Agent cannot delete data without explicit user confirmation.

### Incremental delivery (not big-bang Phase 6)

| Phase | Agent milestone |
| :--- | :--- |
| 1 | Agent shell + `update_application` only |
| 2 | + `score_resume_match`, basic RAG index |
| 2.5 | + `get_roadmap_gaps`, `get_weekly_plan` |
| 3 | + `tailor_resume` with HITL |
| 4 | + `search_internships` |
| 5 | + `read_email_status` via MCP |
| 6 | Full LangGraph wiring + eval harness + trace UI |

---

## 7. UI / UX Philosophy (IDE-Lite)

Not a full VS Code clone—a familiar IDE shell.

```
┌─────────────────────────────────────────────────────────┐
│  Title bar: InternBase    [Cmd+K Search]    [user menu] │
├──────┬──────────────────────────────────────────────────┤
│ Act. │  Tab: Applications | Discovery | Roadmap | Chat │
│ Bar  ├──────────────────────────────────────────────────┤
│ 📋   │           Main content (kanban / feed / etc.)    │
│ 🔍   │                                                  │
│ 📈   ├──────────────────────────────────────────────────┤
│ 💬   │  Bottom panel: Match details | Agent trace | Log │
└──────┴──────────────────────────────────────────────────┘
```

* **Activity bar:** Applications, Discovery, Roadmap, Resume, Agent (chat).
* **Layout:** Dockview or Allotment for resizable split panels; layout persisted in `localStorage`.
* **Monaco Editor:** Resume diff, roadmap notes, agent markdown output.
* **Theme:** VS Code dark tokens + `@vscode/codicons`.
* **Cmd+K:** Command palette (search apps, jump to feed, trigger agent commands).
* **Agent trace panel:** Bottom dock shows plan → RAG retrieve → tool call → result timeline.

---

## 8. Guiding Principle: Real ML, Not a Wrapper

The litmus test for **models**: *if we swapped the LLM for a different one, what of ours is still standing?*

For the **agent layer**, we use LangGraph/LlamaIndex intentionally (framework familiarity for agentic-AI roles). Our moat:

1. Custom fine-tuned models as agent tools.
2. Our own MCP server.
3. Our own eval harness with published benchmark results.
4. Domain-specific multi-step recruiting workflows.

### Models (ours — PyTorch / Hugging Face)

| Model | Job | Approach |
| :--- | :--- | :--- |
| **Skill/keyword extractor** | Pull required skills from a job description | Fine-tuned NER (spaCy baseline first) |
| **Resume JD matcher** | Score semantic match, find missing requirements | Fine-tuned sentence embeddings + pgvector |
| **ATS scorer** | Rate resume's ATS-friendliness | Classifier |
| **Email classifier** | Bucket recruiting emails by type | Text classifier |
| **Project fit scorer** *(v2)* | Rank project idea relevance to JD | Embedding similarity |

> **Note:** Bedrock handles generation + agent reasoning. Strip the LLM out and matcher, classifiers, scrapers, RAG index, and pipeline all remain.

---

## 9. Tech Stack

### SWE core

* **Frontend:** Next.js + TypeScript, Tailwind CSS, shadcn/ui, Dockview or Allotment, Monaco Editor, `@vscode/codicons`.
* **Backend / API:** FastAPI (Python), Pydantic, pytest.
* **Database:** PostgreSQL + SQLAlchemy + Alembic; `pgvector` for embeddings.
* **Auth:** AWS Cognito. *Fallback: Clerk if Cognito eats too much time.*
* **DevOps:** Docker, Docker Compose (local dev), GitHub Actions CI/CD, CloudWatch + Sentry, OpenTelemetry (agent spans), MLflow or S3 model registry.

### Agentic AI layer

* **Orchestration:** LangGraph (plan/tool/observe loops).
* **RAG:** LlamaIndex + pgvector.
* **LLM:** **Amazon Bedrock primary** — Claude on Bedrock via IAM (`boto3` / LangChain Bedrock integration). `LLMProvider` abstraction; direct Anthropic API only as **dev fallback** when `BEDROCK_ENABLED=false`.
* **MCP:** Our own MCP server exposing Gmail (and later Calendar).
* **Prompts:** Versioned YAML in `prompts/`; tracked in `PromptVersion` table.
* **Eval:** `eval/golden_tasks.json` — smoke subset on PR, full suite weekly.

### ML

* PyTorch, Hugging Face Transformers, sentence-transformers, spaCy (baseline). Served as FastAPI inference container on ECS.

### Integrations

* **Scrapers:** `httpx` + BeautifulSoup (static), Playwright (JS-heavy). Targets: Greenhouse/Lever/Ashby + GitHub internship-list repos.
* **Email:** Gmail API + OAuth, Google Cloud Pub/Sub push → backend webhook.

### AWS service map

| Service | Used for |
| :--- | :--- |
| **Bedrock (primary)** | All LLM inference — agent, tailoring, planning |
| ECS Fargate | Backend + ML inference containers |
| RDS PostgreSQL | App DB + pgvector |
| S3 | Resumes, raw scrapes, model artifacts, eval results |
| Lambda + EventBridge | Scheduled scrapers |
| Cognito | Auth |
| Secrets Manager | Gmail OAuth creds (no LLM API keys in prod) |
| CloudWatch | Logs, metrics, agent traces, billing alarms |
| SQS *(later)* | Async email/scrape jobs |

**Skip for v1:** Kubernetes, Kafka, SageMaker, multi-agent coordinator, browser extension.

### Bedrock setup (Phase 0)

* Enable Bedrock model access in AWS console.
* IAM role for ECS: `bedrock:InvokeModel`, `bedrock:InvokeModelWithResponseStream`.
* Default model: Claude Sonnet 4.5 on Bedrock (Claude 3.5 Sonnet was retired); Haiku for routing/planning, Sonnet for tailoring.
* Streaming for agent chat UI.
* Billing alarms on day one.

---

## 10. Cost Model

### Where money goes

| Source | Billing | Notes |
| :--- | :--- | :--- |
| RDS PostgreSQL | Fixed monthly | Largest fixed cost if always on |
| ECS Fargate | Per vCPU-hour | Scales with uptime |
| Amazon Bedrock | Per token | Spikes during agent/tailoring/eval |
| S3, Lambda, CloudWatch | Usage-based | Small at our scale |
| Secrets Manager | ~$0.40/secret/mo | Gmail OAuth |
| Cognito, Gmail API, GitHub Actions | Free tier | Fine for v1 |

**Not a cost:** PyTorch training (local), LangGraph/LlamaIndex (OSS), Docker Compose dev.

### Spending tiers (build phase)

| Tier | Cost | When |
| :--- | :--- | :--- |
| **0 — Free** | $0 | Local Docker only; mock auth/email |
| **1 — Minimal** | ~$5–15/mo | Bedrock from laptop; no always-on deploy |
| **2 — Recommended** | ~$20–40/mo | Deployed ECS + RDS; stop when not demoing |
| **3 — Demo** | ~$40–70/mo | Always-on for portfolio/recruiting season (2–4 weeks) |
| **4 — High** | ~$80–150+ | Not recommended unless funded |

**Default:** Tier 2 during build (student credits cover it); burst to Tier 3 for demo week.

### Student credits ($0 out-of-pocket during build)

* **New AWS account:** Up to **$200** credits for 6 months ($100 signup + $100 from onboarding activities including Bedrock, RDS, Lambda).
* **AWS Educate:** Free labs/training; check current credit offers.
* **Phase 0 action:** Complete all 5 credit activities; set billing alarms immediately.
* **Note:** Bedrock has no permanent free tier—it burns credits or real money.

### Personal use after shipping (solo)

| Mode | Cost | Description |
| :--- | :--- | :--- |
| **A — Local** | $0 (+ optional Bedrock) | Docker Compose on laptop; best for free forever |
| **B — Hibernate** | ~$0–8/mo when idle | Stop RDS + ECS off-season; spin up each recruiting season |
| **C — Free-tier AWS** | $0 for ~12 mo | EC2 t3.micro + RDS db.t3.micro instead of Fargate |
| **D — Always-on** | $30–70/mo | Only if you need 24/7 public URL year-round |

**Recommendation:** Credits during build → **Mode B (hibernate)** for solo personal use after.

### If others use it

| Users | Est. cost |
| :--- | :--- |
| Just you | $0–8/mo (hibernate) or $0 (local) |
| 2–3 friends (light) | +$5–15/mo in Bedrock tokens |
| 5–10 regular users | ~$40–80/mo |
| Public launch | Out of scope (v1) |

*v1.5 guardrails if sharing:* per-user daily Bedrock token budget, queue tailoring jobs, admin cost toggle.

### Cost-control rules

1. Develop locally by default (Docker Compose).
2. Stop ECS tasks and RDS when done for the day.
3. Haiku for plan/route; Sonnet for tailor/generate.
4. Cache embeddings and match scores.
5. Smoke eval on PR; full golden set weekly (not every commit).
6. Billing alarms at $30 and $50 on day one.
7. Bedrock via IAM in prod—no duplicate LLM API keys.

---

## 11. Data Model (Initial)

* **User:** `id`, `email`, `auth_id`, `school`, `grad_year`, `profile_json`
* **UserPreferences:** `user_id`, `target_roles[]`, `target_companies[]`, `locations[]`, `work_auth`, `min_match_score`, `skill_interests[]`
* **Resume:** `id`, `user_id`, `s3_key`, `parsed_text`, `created_at`
* **Resume Version:** `id`, `resume_id`, `application_id`, `tailored_content`, `accepted_edits_json`, `created_at`
* **Company:** `id`, `name`, `domain`
* **JobPosting:** `id`, `company_id`, `title`, `description`, `location`, `source`, `url`, `posted_at`, `scraped_at`, `is_internship`, `season`
* **Application:** `id`, `user_id`, `job_posting_id`, `status`, `current_round`, `applied_at`, `notes`, `deadline_at`
* **StatusEvent:** `id`, `application_id`, `from_status`, `to_status`, `source (manual/email/system)`, `created_at`
* **EmailEvent:** `id`, `user_id`, `gmail_msg_id`, `classified_type`, `confidence`, `matched_application_id`, `needs_confirmation`, `raw_ref`
* **MatchResult:** `id`, `resume_id`, `job_posting_id`, `score`, `matched_skills_json`, `missing_skills_json`, `created_at`
* **Skill:** `id`, `name`, `canonical_name`
* **RoadmapTemplate:** `id`, `role_type`, `content_json`
* **RoadmapItem:** `id`, `user_id`, `template_item_id`, `status`, `completed_at`
* **AgentRun:** `id`, `user_id`, `prompt_version`, `task`, `status`, `trace_json`, `created_at`
* **AgentMemory:** `user_id`, `key`, `value`, `updated_at`
* **PromptVersion:** `id`, `name`, `version`, `content_hash`, `eval_score`
* **EvalResult:** `run_id`, `task_id`, `passed`, `metrics_json`, `created_at`

*v2 placeholders:* `ProjectIdea`, `ProjectSpec`

### Status Enum

`SAVED` → `APPLIED` → `OA` → `PHONE_SCREEN` → `TECHNICAL` → `BEHAVIORAL` → `ONSITE` → `OFFER` / `REJECTED` / `GHOSTED` / `WITHDRAWN`

---

## 12. Build Phases

Each phase is a GitHub milestone. A phase is "done" only when its definition-of-done is met and it's deployed.

* **V1 target:** July 10, 2026 (~29 days, 4 one-week sprints). See [Section 18](#18-sprint-schedule--github-backlog).

### Phase 0 — Setup (~3–4 days)

* Monorepo + Docker Compose local dev (frontend, backend, Postgres).
* GitHub Actions CI (lint + test on PR).
* GitHub Project board, labels, milestones.
* Agree on data model + core API contract.
* **AWS:** Create account, complete 5 credit activities, enable Bedrock, IAM roles, billing alarms.
* **Bedrock:** `LLMProvider` with `BedrockProvider` + dev fallback.
* **Done when:** Both devs run the whole stack locally with one command; Bedrock invoke works from backend.

### Phase 1 — Tracker MVP + IDE Shell

* **(Person A):** IDE-lite shell (activity bar, split layout, VS Code dark theme).
* **(Person A):** Next.js + Cognito auth; kanban CRUD + FastAPI endpoints; CSV export; deadline reminders.
* **(Person A):** Deploy hello-world to AWS (Fargate + RDS).
* **(Person A):** Minimal agent chat shell + `update_application` tool.
* **(Person B):** Collect datasets (JDs + recruiting emails); spaCy baseline skill extractor.
* **Done when:** Track applications end-to-end on deployed app; agent can move a kanban card via chat.

### Phase 2 — Resume Matcher (Our Model)

* **(Person B):** Resume parser (PDF → text), JD parser; embedding matcher on pgvector + ATS scorer.
* **(Person B):** Basic RAG index of uploaded resume; agent `score_resume_match` tool.
* **(Person A):** Upload UI + match-score / gaps view; Monaco resume preview.
* **Done when:** Upload resume + paste JD → see score and missing skills; agent can score a match.

### Phase 2.5 — Lightweight Roadmap (~1 week)

* **(Person B):** Curate 3 preset templates (SWE General, MLE, Agentic AI) in `backend/data/roadmaps/`.
* **(Person B):** Gap sync from matcher; agent `get_roadmap_gaps` + `get_weekly_plan` tools.
* **(Person A):** Roadmap checklist UI with progress tracking.
* **Done when:** Set target role → see checklist with auto-populated skill gaps; agent can suggest weekly plan.

### Phase 3 — Resume Tailoring

* **(Person B):** Bedrock tailoring driven by matcher output; anti-fabrication guardrails; versioned prompts.
* **(Person A):** Per-edit accept/reject Monaco diff UI + PDF export; agent `tailor_resume` tool.
* **Done when:** Generate tailored, downloadable resume with every edit explained and approved.

### Phase 4 — Internship Aggregation

* **(Person B):** Scrapers (Greenhouse/Lever/Ashby + GitHub lists), normalize + dedupe, Lambda + EventBridge.
* **(Person A):** Discovery feed with "For You" ranking (preferences + matcher); one-click add to tracker; agent `search_internships` tool.
* **Done when:** New postings appear automatically; personalized feed works.

### Phase 5 — Email Status Detection (Our Model + MCP)

* **(Person B):** Gmail OAuth + Pub/Sub; email classifier; match-to-application logic; Gmail MCP server.
* **(Person A):** Auto-status UI + confirm-ambiguous flow; agent `read_email_status` tool.
* **Done when:** Rejection/interview email auto-moves the right application (with HITL on low confidence).

### Phase 6 — Agent Integration + Eval

* Wire all tools into LangGraph orchestration.
* Golden-set eval harness in CI (smoke on PR, full weekly).
* Agent trace panel + prompt version viewer.
* Publish eval results in README.
* **Done when:** *"find backend internships and tailor my resume for the top 3"* works end-to-end with visible trace and eval metrics.

### Phase 7 — Polish & Portfolio

* Monitoring (CloudWatch + Sentry), Cmd+K palette, demo video, README write-up.
* **Done when:** Portfolio-ready deploy with documented agent architecture and eval scores.

### Phase 8 — v2 Stub (Future)

* Project Ideation Studio, full roadmap engine, multi-agent coordinator, startup problem finder.

---

## 13. Team & Working Agreements

### Roles

*(Swap/pair occasionally so both learn both halves)*

* **Person A — App + Infra:** Frontend, IDE shell, backend wiring, AWS, deploy, agent UI/trace panel.
* **Person B — ML + Data + Agent:** Models, datasets, scrapers, email pipeline, LangGraph tools, eval harness.
* **Shared:** Data model + API contract (Phase 0), agent integration (Phase 6).

### Agreements

* API contract defined before parallel work.
* Every change → feature branch → PR → partner review.
* Never both edit the same files in the same session.
* 15-minute sync twice a week.

### GitHub Conventions

Full conventions, templates, and repo setup checklist: **[GITHUB_CONVENTIONS.md](GITHUB_CONVENTIONS.md)**.

Summary:

* **Milestones** = phases listed above + `v1.0.0-jul10` release milestone.
* **Types:** `type:feature`, `type:fix`, `type:chore` — match branches `feature/`, `fix/`, `chore/`.
* **Labels:** `area:*`, `type:*`, `priority:P0`–`P3`, `sprint:0`–`sprint:3` — see conventions doc.
* One issue = one shippable task; link to milestone; use GitHub sub-issues under parent epics ([Section 18](#18-sprint-schedule--github-backlog)).
* **Branch workflow:** [BRANCH_WORKFLOW.md](BRANCH_WORKFLOW.md). **Commits:** [COMMIT_CONVENTIONS.md](COMMIT_CONVENTIONS.md).

---

## 14. Risks & Cut Order

If we fall behind, defer in this order (last-listed cut first):

1. **Email Detection (Phase 5):** Most infra-heavy (OAuth + Pub/Sub).
2. **Aggregation (Phase 4):** Scrapers are brittle.
3. **Roadmap (Phase 2.5):** Can ship with one static template later.
4. **Eval harness polish / trace UI:** Reduce golden set; skip dashboard.
5. **NEVER CUT — Tracker + Matcher + Tailoring + Agent core (LangGraph + ≥3 tools + RAG).**

### Other Risks

* **Scraper fragility:** Keep sources modular.
* **Gmail restricted-scope review:** Stay in testing mode.
* **Bedrock costs:** Model tiering + billing alarms + hibernate off-season.
* **Scope creep:** This document is the gate.

---

## 15. Definition of Done (v1)

A deployed web app where a CS student can:

* Track applications on a kanban board (IDE-lite shell).
* Upload a resume and get match scores + tailored version per listing (HITL edits).
* Browse auto-aggregated, preference-ranked internship postings.
* Follow a lightweight roadmap with auto-populated skill gaps.
* Have inbox auto-update application statuses (with confirmation on ambiguity).
* Drive it all through an agent with visible trace panel and published eval metrics.
* All running on AWS (ECS, RDS, S3, Bedrock) with our own matcher, classifiers, and scrapers.

---

## 16. Open Decisions

**Resolved:**

* [x] LLM provider: **Amazon Bedrock primary**; Anthropic direct API as dev-only fallback.
* [x] AWS budget: Credits during build ($0 OOP); solo post-ship = **Mode B hibernate** (~$0–8/mo) or Mode A local ($0).
* [x] UI: **IDE-lite** (not full VS Code clone).
* [x] Scope split: v1 = recruiting + lightweight roadmap + agent platform; v2 = project studio.

**Still open:**

* [ ] Project name (placeholder: InternBase)
* [ ] Partner's name for role assignment
* [ ] Bedrock model tier: Sonnet everywhere vs Haiku routing + Sonnet tailoring
* [ ] Local dev: real Bedrock creds vs `BEDROCK_ENABLED=false` fallback
* [ ] LangGraph checkpoint store: in-memory vs Postgres
* [ ] Eval golden set size (20 vs 30) and CI budget
* [ ] Preset roadmap sources (NeetCode 150 vs Blind 75 vs custom)
* [ ] Dockview vs Allotment for panel layout
* [ ] Browser extension in v2?

---

## 17. What To Do Next (Sprint-Aligned)

**V1 ships July 10, 2026.** Full issue backlog: [Section 18](#18-sprint-schedule--github-backlog). Don't skip Phase 0.

### Sprint 0 — Jun 11–17 (Phase 0–1)

1. **Create AWS account** — 5 credit activities; billing alarms at $30 and $50.
2. **Enable Bedrock** — Claude model access; test invoke from Python.
3. **Monorepo + Docker Compose** — one command runs frontend + backend + Postgres.
4. **GitHub repo** — milestones, labels, project board, issues from Section 18.
5. **Data model + API contract** — finalize Section 11 before parallel work.
6. **IDE shell + tracker kanban** — demoable application board in IDE-lite layout.
7. **Deploy hello-world** — Fargate + RDS; don't wait until Sprint 3.
8. **Minimal agent** — chat shell + `update_application` tool.

### Sprint 1 — Jun 18–24 (Phase 2)

9. **Resume matcher** — parser, embeddings, pgvector, match score + gaps UI.
10. **RAG index + `score_resume_match`** — agent can score a match via chat.

### Sprint 2 — Jun 25–Jul 1 (Phase 2.5–3)

11. **SWE General roadmap only** — one template; gap sync from matcher.
12. **Tailoring HITL** — Bedrock + Monaco diff; every edit approved before export.

### Sprint 3 — Jul 2–10 (Phase 4, 6–7)

13. **Minimal aggregation** — one scraper source + discovery feed (cut to manual URL if behind).
14. **Full agent wiring + trace panel** — LangGraph orchestrates ≥5 tools.
15. **Eval smoke in CI** — 5 golden tasks on PR; publish pass rate in README.
16. **Portfolio polish** — demo video, Cmd+K, hibernate docs.

### Deferred past Jul 10 (unless ahead)

* Phase 5 — Email status detection + Gmail MCP.
* Multi-source scrapers, MLE/Agentic roadmap templates, full eval dashboard.

### What NOT to do yet

* Don't build project ideation studio (v2).
* Don't pursue public launch or multi-tenant billing.
* Don't use Fargate 24/7 during development—stop tasks when done.
* Don't run full eval suite on every PR—smoke 5 tasks only.

### Preset roadmap content (Phase 2.5 — SWE General only for Jul 10)

Store in `backend/data/roadmaps/`:

* **SWE General:** NeetCode 150 by topic, MIT 6.006, CS50, AWS Lambda lab, STAR behavioral template.

*MLE and Agentic AI templates ship post–Jul 10.*

*The app teaches the skills required to build the app—and the app itself is the demo.*

---

## 18. Sprint Schedule & GitHub Backlog

Every issue below traces to this document. Create parent **epics** in GitHub first, then sub-issues. Issue numbers (`#1`, `#2`, …) are placeholders until created—replace with actual GitHub numbers and link sub-issues via GitHub's sub-issue feature.

**How to use:** Copy each issue block into GitHub (or use `gh issue create`). Apply labels and sprint label from the tables. Milestones, assignees, and epics are optional — use the issue templates for day-to-day work.

### Sprint calendar

| Sprint | Dates | Goal | Milestones | Release |
| :--- | :--- | :--- | :--- | :--- |
| **Sprint 0** | Jun 11–17 | Setup + IDE shell + tracker MVP + deploy + agent shell | Phase 0, Phase 1 | — |
| **Sprint 1** | Jun 18–24 | Matcher + RAG index + upload UI | Phase 2 | — |
| **Sprint 2** | Jun 25–Jul 1 | SWE roadmap + tailoring HITL | Phase 2.5, Phase 3 | — |
| **Sprint 3** | Jul 2–10 | Minimal aggregation + agent wiring + eval + polish | Phase 4, Phase 6, Phase 7 | `v1.0.0-jul10` |

**Jul 10 V1 scope (in):** Tracker, Matcher, Tailoring, 1 roadmap template, ≥5 agent tools, LangGraph + trace, smoke eval, AWS deploy.

**Deferred past Jul 10:** Phase 5 (Email/MCP), multi-source scrapers, MLE/Agentic roadmap templates, full eval dashboard.

**If behind at Sprint 2 retro:** Cut Epic E5 to manual job URL paste; reduce eval golden set to 10 tasks.

---

### Epic E0 — Phase 0: Project Setup

**GitHub:** Create as issue titled `[Epic] Phase 0 — Project Setup`  
**Labels:** `type:feature`, `priority:P0`, `sprint:0` | **Milestone:** Phase 0 | **Assignee:** Both

| Sub-issue | Title | Labels | Assignee | Size |
| :--- | :--- | :--- | :--- | :--- |
| #1 | Monorepo + Docker Compose local dev | `area:infra`, `type:feature`, `priority:P0`, `sprint:0` | Person A | M |
| #2 | GitHub repo: milestones, labels, project board | `area:infra`, `type:chore`, `priority:P0`, `sprint:0` | Both | S |
| #3 | AWS account + Bedrock access + billing alarms | `area:infra`, `type:chore`, `priority:P0`, `sprint:0` | Person A | M |
| #4 | `LLMProvider` abstraction + Bedrock invoke | `area:backend`, `type:feature`, `priority:P0`, `sprint:0` | Person A | M |
| #5 | Data model + API contract document | `area:backend`, `type:chore`, `priority:P0`, `sprint:0` | Both | M |
| #6 | GitHub Actions CI: lint + test on PR | `area:infra`, `type:chore`, `priority:P0`, `sprint:0` | Person A | M |

#### #1 — Monorepo + Docker Compose local dev

**Parent epic:** E0 | **PROJECT.md:** [Section 12 — Phase 0](#phase-0--setup-34-days)

**Acceptance criteria:**

- [x] Monorepo layout: `frontend/`, `backend/`, `docker-compose.yml`
- [x] `docker compose up` starts Next.js, FastAPI, and Postgres without manual steps
- [x] Health-check endpoints respond on frontend and backend
- [x] README documents one-command local setup

#### #2 — GitHub repo: milestones, labels, project board

**Parent epic:** E0 | **PROJECT.md:** [Section 13](#13-team--working-agreements), [GITHUB_CONVENTIONS.md](GITHUB_CONVENTIONS.md)

**Acceptance criteria:**

- [x] Milestones `Phase 0`–`Phase 7` and `v1.0.0-jul10` created
- [x] All labels from conventions doc applied
- [x] Project board columns: Backlog → Sprint → In Progress → In Review → Done
- [x] Branch protection on `main` (PR + 1 review required)
- [x] Sub-issues enabled in repo settings

#### #3 — AWS account + Bedrock access + billing alarms

**Parent epic:** E0 | **PROJECT.md:** [Section 9 — Bedrock setup](#bedrock-setup-phase-0), [Section 10](#10-cost-model)

**Acceptance criteria:**

- [x] AWS account created; all 5 credit onboarding activities completed
- [x] Claude model access enabled in Bedrock console
- [x] Billing alarms at $30 and $50 configured
- [x] IAM user/role documented for local dev (no keys in repo)

#### #4 — `LLMProvider` abstraction + Bedrock invoke

**Parent epic:** E0 | **PROJECT.md:** [Section 9 — Agentic AI layer](#agentic-ai-layer)

**Acceptance criteria:**

- [x] `LLMProvider` interface with `BedrockProvider` implementation
- [x] Dev fallback when `BEDROCK_ENABLED=false` (mock or direct API)
- [x] Backend endpoint or script proves successful Bedrock invoke
- [x] Env vars documented in `.env.example`

#### #5 — Data model + API contract document

**Parent epic:** E0 | **PROJECT.md:** [Section 11](#11-data-model-initial)

**Acceptance criteria:**

- [x] SQLAlchemy models match Section 11 entities (core tables)
- [x] Initial Alembic migration runs against Postgres
- [x] `docs/API_CONTRACT.md` lists core REST endpoints for Phase 1
- [x] Both partners sign off before Sprint 0 parallel work splits

#### #6 — GitHub Actions CI: lint + test on PR

**Parent epic:** E0 | **PROJECT.md:** [Section 12 — Phase 0](#phase-0--setup-34-days)

**Acceptance criteria:**

- [x] Workflow runs on pull request to `main`
- [x] Backend: `ruff` + `pytest` (at least smoke test)
- [x] Frontend: `eslint` + `tsc --noEmit` (or equivalent)
- [x] CI status required for merge

---

### Epic E1 — Phase 1: Tracker MVP + IDE Shell

**GitHub:** `[Epic] Phase 1 — Tracker MVP + IDE Shell`  
**Labels:** `type:feature`, `priority:P0`, `sprint:0` | **Milestone:** Phase 1

| Sub-issue | Title | Labels | Assignee | Size |
| :--- | :--- | :--- | :--- | :--- |
| #7 | IDE-lite shell (activity bar, dark theme, split panels) | `area:frontend`, `type:feature`, `priority:P0`, `sprint:0` | Person A | L |
| #8 | Auth: Cognito integration (or mock-auth fallback) | `area:frontend`, `area:backend`, `type:feature`, `priority:P0`, `sprint:0` | Person A | M |
| #9 | Application kanban CRUD API | `area:backend`, `type:feature`, `priority:P0`, `sprint:0` | Person A | M |
| #10 | Kanban UI + CSV export + deadline reminders | `area:frontend`, `type:feature`, `priority:P0`, `sprint:0` | Person A | L |
| #11 | Fargate + RDS hello-world deploy | `area:infra`, `type:feature`, `priority:P0`, `sprint:0` | Person A | L |
| #12 | Agent chat shell + `update_application` tool | `area:agent`, `area:frontend`, `type:feature`, `priority:P0`, `sprint:0` | Person A | L |
| #13 | Collect JD + recruiting email datasets | `area:ml`, `type:chore`, `priority:P1`, `sprint:0` | Person B | M |
| #14 | spaCy skill extractor baseline | `area:ml`, `type:feature`, `priority:P1`, `sprint:0` | Person B | M |

#### #7 — IDE-lite shell

**Parent epic:** E1 | **PROJECT.md:** [Section 7](#7-ui--ux-philosophy-ide-lite)

**Acceptance criteria:**

- [ ] Activity bar with Applications, Discovery, Roadmap, Resume, Agent placeholders
- [ ] VS Code dark theme + `@vscode/codicons`
- [ ] Resizable split panels (Dockview or Allotment); layout persists in `localStorage`
- [ ] Bottom panel placeholder for trace/logs

#### #8 — Auth: Cognito integration (or mock-auth fallback)

**Parent epic:** E1 | **PROJECT.md:** [Section 9 — SWE core](#swe-core)

**Acceptance criteria:**

- [ ] User can sign in and session persists across refresh
- [ ] Protected routes redirect unauthenticated users
- [ ] If Cognito blocked: chore issue documents mock-auth path with follow-up feature issue
- [ ] Auth flow documented in README

#### #9 — Application kanban CRUD API

**Parent epic:** E1 | **PROJECT.md:** [Section 5 — Tracker](#v1--eight-subsystems-sequenced-each-independently-complete), [Section 11](#11-data-model-initial)

**Acceptance criteria:**

- [ ] CRUD endpoints for `Application` with status enum pipeline
- [ ] `StatusEvent` recorded on status changes
- [ ] Pydantic schemas + pytest coverage for happy path
- [ ] API matches `docs/API_CONTRACT.md`

#### #10 — Kanban UI + CSV export + deadline reminders

**Parent epic:** E1 | **PROJECT.md:** [Section 5 — Tracker](#v1--eight-subsystems-sequenced-each-independently-complete)

**Acceptance criteria:**

- [ ] Drag-and-drop kanban columns match status enum
- [ ] Create/edit application with notes, dates, deadline
- [ ] CSV export of all applications
- [ ] Visual indicator for applications with upcoming deadlines

#### #11 — Fargate + RDS hello-world deploy

**Parent epic:** E1 | **PROJECT.md:** [Section 12 — Phase 1](#phase-1--tracker-mvp--ide-shell)

**Acceptance criteria:**

- [ ] Frontend and backend deployed to ECS Fargate
- [ ] RDS Postgres reachable from backend; migrations applied
- [ ] Public URL loads IDE shell (auth may be relaxed for hello-world)
- [ ] Deploy/runbook in `docs/DEPLOY.md` (or README section)

#### #12 — Agent chat shell + `update_application` tool

**Parent epic:** E1 | **PROJECT.md:** [Section 6 — Incremental delivery](#incremental-delivery-not-big-bang-phase-6)

**Acceptance criteria:**

- [ ] Chat panel in IDE shell sends messages to backend agent endpoint
- [ ] `update_application` LangGraph tool moves kanban card by status
- [ ] User can say "move Stripe to phone screen" and see board update
- [ ] Basic agent run logged to `AgentRun` table

#### #13 — Collect JD + recruiting email datasets

**Parent epic:** E1 | **PROJECT.md:** [Section 8 — Models](#models-ours--pytorch--hugging-face)

**Acceptance criteria:**

- [ ] ≥50 job descriptions stored in `backend/data/jds/` (or S3)
- [ ] ≥100 recruiting emails (anonymized) for classifier training
- [ ] Dataset README with source and license notes
- [ ] No PII committed to repo

#### #14 — spaCy skill extractor baseline

**Parent epic:** E1 | **PROJECT.md:** [Section 8 — Skill/keyword extractor](#models-ours--pytorch--hugging-face)

**Acceptance criteria:**

- [ ] spaCy NER or rule baseline extracts skills from sample JDs
- [ ] CLI or endpoint returns skill list for a pasted JD
- [ ] Evaluation on 10 held-out JDs documented
- [ ] Output format ready for matcher pipeline (Phase 2)

---

### Epic E2 — Phase 2: Resume Matcher

**GitHub:** `[Epic] Phase 2 — Resume Matcher`  
**Labels:** `type:feature`, `priority:P0`, `sprint:1` | **Milestone:** Phase 2

| Sub-issue | Title | Labels | Assignee | Size |
| :--- | :--- | :--- | :--- | :--- |
| #15 | Resume parser (PDF → text) | `area:ml`, `type:feature`, `priority:P0`, `sprint:1` | Person B | M |
| #16 | JD parser + skill extraction integration | `area:ml`, `type:feature`, `priority:P0`, `sprint:1` | Person B | M |
| #17 | Embedding matcher + pgvector storage | `area:ml`, `area:backend`, `type:feature`, `priority:P0`, `sprint:1` | Person B | L |
| #18 | ATS scorer classifier | `area:ml`, `type:feature`, `priority:P1`, `sprint:1` | Person B | M |
| #19 | Resume upload UI + match score / gaps view | `area:frontend`, `type:feature`, `priority:P0`, `sprint:1` | Person A | L |
| #20 | Basic RAG index + `score_resume_match` agent tool | `area:agent`, `area:ml`, `type:feature`, `priority:P0`, `sprint:1` | Person B | L |

#### #15 — Resume parser (PDF → text)

**Acceptance criteria:**

- [ ] Upload PDF resume; `parsed_text` stored on `Resume` model
- [ ] Handles common single-column resume formats
- [ ] Parser errors return clear API error messages
- [ ] Unit tests with fixture PDFs

#### #16 — JD parser + skill extraction integration

**Acceptance criteria:**

- [ ] Paste or fetch JD text; skills extracted via #14 pipeline
- [ ] Skills normalized to `Skill` table where applicable
- [ ] Endpoint returns structured JD + skills JSON

#### #17 — Embedding matcher + pgvector storage

**Acceptance criteria:**

- [ ] Sentence embeddings stored in pgvector for resume and JD
- [ ] `MatchResult` with score, matched skills, missing skills
- [ ] Match endpoint: resume ID + job posting ID → score
- [ ] Inference latency acceptable for demo (<3s local)

#### #18 — ATS scorer classifier

**Acceptance criteria:**

- [ ] ATS-friendliness score 0–100 for a resume
- [ ] Score surfaced in match details UI (can be simple badge)
- [ ] Documented limitations in README

#### #19 — Resume upload UI + match score / gaps view

**Acceptance criteria:**

- [ ] Upload flow in Resume activity panel
- [ ] Paste JD or select job posting → see match score
- [ ] Matched vs missing skills displayed clearly
- [ ] Monaco preview of parsed resume text

#### #20 — Basic RAG index + `score_resume_match` agent tool

**Acceptance criteria:**

- [ ] LlamaIndex indexes uploaded resume content in pgvector
- [ ] Agent tool `score_resume_match` returns score + gaps in chat
- [ ] RAG retrieve step visible in agent trace (basic log ok for now)
- [ ] Tool registered in LangGraph agent config

---

### Epic E3 — Phase 2.5: Lightweight Roadmap

**GitHub:** `[Epic] Phase 2.5 — Lightweight Roadmap`  
**Labels:** `type:feature`, `priority:P1`, `sprint:2` | **Milestone:** Phase 2.5

| Sub-issue | Title | Labels | Assignee | Size |
| :--- | :--- | :--- | :--- | :--- |
| #21 | SWE General roadmap template | `area:ml`, `type:feature`, `priority:P1`, `sprint:2` | Person B | M |
| #22 | Gap sync from matcher to roadmap items | `area:backend`, `type:feature`, `priority:P1`, `sprint:2` | Person B | M |
| #23 | Agent tools: `get_roadmap_gaps` + `get_weekly_plan` | `area:agent`, `type:feature`, `priority:P1`, `sprint:2` | Person B | M |
| #24 | Roadmap checklist UI with progress tracking | `area:frontend`, `type:feature`, `priority:P1`, `sprint:2` | Person A | M |

#### #21 — SWE General roadmap template

**Acceptance criteria:**

- [ ] `backend/data/roadmaps/swe_general.json` with NeetCode 150 topics, courses, labs
- [ ] `RoadmapTemplate` seeded via migration or script
- [ ] User can select SWE General as target role

#### #22 — Gap sync from matcher to roadmap items

**Acceptance criteria:**

- [ ] Missing skills from latest `MatchResult` auto-mark relevant checklist items
- [ ] `RoadmapItem` status reflects gap vs complete
- [ ] API endpoint returns merged template + gap state

#### #23 — Agent tools: `get_roadmap_gaps` + `get_weekly_plan`

**Acceptance criteria:**

- [ ] `get_roadmap_gaps` lists prioritized gaps from matcher + template
- [ ] `get_weekly_plan` suggests 5–7 items based on tracker + roadmap state
- [ ] Both tools callable from agent chat

#### #24 — Roadmap checklist UI with progress tracking

**Acceptance criteria:**

- [ ] Roadmap activity panel shows checklist with check/uncheck
- [ ] Gap items visually distinct (e.g. highlighted)
- [ ] Progress percentage or section counts visible

---

### Epic E4 — Phase 3: Resume Tailoring

**GitHub:** `[Epic] Phase 3 — Resume Tailoring`  
**Labels:** `type:feature`, `priority:P0`, `sprint:2` | **Milestone:** Phase 3

| Sub-issue | Title | Labels | Assignee | Size |
| :--- | :--- | :--- | :--- | :--- |
| #25 | Bedrock tailoring service + anti-fabrication guardrails | `area:backend`, `area:agent`, `type:feature`, `priority:P0`, `sprint:2` | Person B | L |
| #26 | Versioned tailoring prompts in `prompts/` | `area:agent`, `type:chore`, `priority:P0`, `sprint:2` | Person B | S |
| #27 | Monaco diff HITL UI + PDF export | `area:frontend`, `type:feature`, `priority:P0`, `sprint:2` | Person A | L |
| #28 | Agent tool: `tailor_resume` with HITL flow | `area:agent`, `type:feature`, `priority:P0`, `sprint:2` | Person B | M |

#### #25 — Bedrock tailoring service + anti-fabrication guardrails

**Acceptance criteria:**

- [ ] Tailoring uses matcher output (missing skills) as input context
- [ ] Proposed edits are bullet-level with explanations
- [ ] Guardrails reject fabricated employers, dates, or degrees
- [ ] `Resume Version` stores tailored content + accepted edits JSON

#### #26 — Versioned tailoring prompts in `prompts/`

**Acceptance criteria:**

- [ ] YAML prompts in `prompts/tailor_resume/v1.yaml` (or similar)
- [ ] `PromptVersion` row created on deploy/migration
- [ ] `AgentRun` records prompt version used

#### #27 — Monaco diff HITL UI + PDF export

**Acceptance criteria:**

- [ ] Side-by-side or inline diff for each proposed edit
- [ ] Accept/reject per edit; no save until user confirms
- [ ] Download tailored resume as PDF
- [ ] Rejected edits never appear in final version

#### #28 — Agent tool: `tailor_resume` with HITL flow

**Acceptance criteria:**

- [ ] Agent initiates tailor flow; UI opens diff panel
- [ ] User completes HITL in UI; agent receives completion status
- [ ] End-to-end: chat request → proposed edits → approved PDF

---

### Epic E5 — Phase 4: Internship Aggregation (minimal)

**GitHub:** `[Epic] Phase 4 — Internship Aggregation (minimal)`  
**Labels:** `type:feature`, `priority:P2`, `sprint:3` | **Milestone:** Phase 4

| Sub-issue | Title | Labels | Assignee | Size |
| :--- | :--- | :--- | :--- | :--- |
| #29 | Single-source internship scraper (Greenhouse or GitHub list) | `area:ml`, `area:backend`, `type:feature`, `priority:P2`, `sprint:3` | Person B | L |
| #30 | Normalize + dedupe job postings pipeline | `area:backend`, `type:feature`, `priority:P2`, `sprint:3` | Person B | M |
| #31 | Discovery feed UI + one-click add to tracker | `area:frontend`, `type:feature`, `priority:P2`, `sprint:3` | Person A | M |
| #32 | Agent tool: `search_internships` | `area:agent`, `type:feature`, `priority:P2`, `sprint:3` | Person B | M |

#### #29 — Single-source internship scraper

**Acceptance criteria:**

- [ ] Scraper pulls internship postings from one source (Greenhouse API or curated GitHub list)
- [ ] Raw scrape stored in S3 or local data dir
- [ ] Runnable manually via CLI; Lambda scheduled job optional for Jul 10
- [ ] Modular adapter pattern for future sources

#### #30 — Normalize + dedupe job postings pipeline

**Acceptance criteria:**

- [ ] Postings normalized to `JobPosting` + `Company` models
- [ ] Dedupe by URL or (company, title, location) hash
- [ ] `is_internship` flag set via heuristic or source filter

#### #31 — Discovery feed UI + one-click add to tracker

**Acceptance criteria:**

- [ ] Discovery activity panel lists postings sorted by preferences + match score
- [ ] "Add to tracker" creates `Application` in `SAVED` status
- [ ] Empty state when no postings scraped yet

#### #32 — Agent tool: `search_internships`

**Acceptance criteria:**

- [ ] Agent searches postings by role, location, or company keywords
- [ ] Results ranked by user preferences and optional match score
- [ ] User can ask agent to add top result to tracker

**Cut alternative (if behind):** Replace #29–#32 with manual "paste job URL" → parse → add to tracker.

---

### Epic E6 — Phase 6: Agent Integration + Eval

**GitHub:** `[Epic] Phase 6 — Agent Integration + Eval`  
**Labels:** `type:feature`, `priority:P0`, `sprint:3` | **Milestone:** Phase 6

| Sub-issue | Title | Labels | Assignee | Size |
| :--- | :--- | :--- | :--- | :--- |
| #33 | Full LangGraph orchestration (all v1 tools) | `area:agent`, `type:feature`, `priority:P0`, `sprint:3` | Both | L |
| #34 | Agent trace panel UI | `area:frontend`, `area:agent`, `type:feature`, `priority:P0`, `sprint:3` | Person A | L |
| #35 | Golden-set eval harness + smoke CI (5 tasks) | `area:agent`, `type:feature`, `priority:P0`, `sprint:3` | Person B | L |
| #36 | Publish eval metrics in README | `area:agent`, `type:chore`, `priority:P1`, `sprint:3` | Person B | S |

#### #33 — Full LangGraph orchestration (all v1 tools)

**Acceptance criteria:**

- [ ] LangGraph state machine: plan → retrieve → act → observe → replan
- [ ] All shipped tools wired: `update_application`, `score_resume_match`, `get_roadmap_gaps`, `get_weekly_plan`, `tailor_resume`, `search_internships`, `search_knowledge`
- [ ] Multi-step task works: "find internships and tailor resume for top match"
- [ ] Checkpoint store configured (Postgres or in-memory per open decision)

#### #34 — Agent trace panel UI

**Acceptance criteria:**

- [ ] Bottom panel shows timeline: plan → RAG retrieve → tool call → result
- [ ] Each step expandable with JSON/detail view
- [ ] Trace loads from `AgentRun.trace_json` for past runs

#### #35 — Golden-set eval harness + smoke CI (5 tasks)

**Acceptance criteria:**

- [ ] `eval/golden_tasks.json` with ≥20 tasks; smoke subset of 5 for PR CI
- [ ] Harness runs agent against tasks; outputs pass/fail + metrics
- [ ] GitHub Actions job runs smoke eval on agent-touched PRs
- [ ] Full suite runnable locally weekly

#### #36 — Publish eval metrics in README

**Acceptance criteria:**

- [ ] README section with eval pass rate, date, and prompt version
- [ ] Instructions to reproduce eval run locally
- [ ] Links to agent architecture diagram or Section 6 summary

---

### Epic E7 — Phase 7: Polish & Portfolio

**GitHub:** `[Epic] Phase 7 — Polish & Portfolio`  
**Labels:** `type:feature`, `priority:P1`, `sprint:3` | **Milestone:** Phase 7

| Sub-issue | Title | Labels | Assignee | Size |
| :--- | :--- | :--- | :--- | :--- |
| #37 | Cmd+K command palette | `area:frontend`, `type:feature`, `priority:P1`, `sprint:3` | Person A | M |
| #38 | Demo video + architecture write-up | `area:infra`, `type:chore`, `priority:P1`, `sprint:3` | Both | M |
| #39 | Hibernate runbook (stop RDS/ECS off-season) | `area:infra`, `type:chore`, `priority:P1`, `sprint:3` | Person A | S |

#### #37 — Cmd+K command palette

**Acceptance criteria:**

- [ ] Cmd+K opens palette: search applications, jump to panels, trigger agent commands
- [ ] Keyboard navigation works
- [ ] At least 5 useful commands registered

#### #38 — Demo video + architecture write-up

**Acceptance criteria:**

- [ ] 3–5 minute demo video (tracker, matcher, tailor, agent trace)
- [ ] README tells SWE story (stack, AWS, CI) and Agentic AI story (RAG, tools, eval, Bedrock)
- [ ] Video linked from README

#### #39 — Hibernate runbook

**Acceptance criteria:**

- [ ] `docs/HIBERNATE.md` documents stop/start for RDS + ECS
- [ ] Estimated monthly cost when hibernating documented
- [ ] Tested once: stop → start → app still works

---

### Epic E8 — Phase 5: Email Status Detection (post–Jul 10 backlog)

**GitHub:** `[Epic] Phase 5 — Email Status Detection`  
**Labels:** `type:feature`, `priority:P3` | **Milestone:** Phase 5 | **Sprint:** Backlog

| Sub-issue | Title | Labels | Assignee | Size |
| :--- | :--- | :--- | :--- | :--- |
| #40 | Gmail OAuth + Pub/Sub webhook | `area:backend`, `area:infra`, `type:feature`, `priority:P3` | Person B | L |
| #41 | Email classifier model | `area:ml`, `type:feature`, `priority:P3` | Person B | L |
| #42 | Auto-status UI + confirm-ambiguous flow | `area:frontend`, `type:feature`, `priority:P3` | Person A | M |
| #43 | Gmail MCP server + `read_email_status` agent tool | `area:agent`, `type:feature`, `priority:P3` | Person B | L |

#### #40 — Gmail OAuth + Pub/Sub webhook

**Acceptance criteria:**

- [ ] OAuth flow in testing mode; tokens in Secrets Manager
- [ ] Pub/Sub push delivers new messages to backend webhook
- [ ] `EmailEvent` rows created for incoming messages

#### #41 — Email classifier model

**Acceptance criteria:**

- [ ] Classifier buckets: rejection, interview invite, OA, offer, other
- [ ] Confidence score returned per classification
- [ ] Low confidence flagged `needs_confirmation`

#### #42 — Auto-status UI + confirm-ambiguous flow

**Acceptance criteria:**

- [ ] UI shows pending email-driven status updates
- [ ] User can confirm or reject ambiguous matches
- [ ] Confirmed updates write `StatusEvent` with `source=email`

#### #43 — Gmail MCP server + `read_email_status` agent tool

**Acceptance criteria:**

- [ ] MCP server exposes read/search email tools per MCP spec
- [ ] Agent `read_email_status` returns classified status for recent recruiting emails
- [ ] Agent trace shows MCP tool invocation

---

### Issue creation checklist

After merging this doc into the repo:

1. Create epics E0–E8 as parent issues (E8 in Backlog, not Sprint 3).
2. Create sub-issues #1–#43; link each to its parent epic.
3. Apply labels and sprint labels from tables above (milestones and assignees optional).
4. Add all Sprint 0 issues to the project board **Sprint** column on Jun 11.
5. Run Sprint 0 planning: confirm WIP ≤2 issues per person.
