# Commit Conventions

We use [Conventional Commits](https://www.conventionalcommits.org/) adapted for InternBase. Consistent messages make history searchable and PR squash titles predictable.

Enable the commit template in this repo:

```bash
git config commit.template .gitmessage
```

---

## Format

```
<type>(<scope>): <imperative summary>

[optional body — wrap at 72 characters]

Refs #123
```

### Subject line rules

- **Imperative mood:** "add tracker API" not "added" or "adds"
- **≤72 characters**
- **No period** at the end
- **Lowercase** after the colon (except proper nouns: Bedrock, LangGraph)

### Body (optional)

- Explain *why*, not just what
- Reference breaking changes if any

### Footer

- `Refs #123` — related issue (feature work)
- `Closes #123` — only in PR description (squash merge closes issue); avoid in individual commits unless one commit = one issue
- `BREAKING CHANGE:` — API or schema breaking change

---

## Types

| Type | When |
| :--- | :--- |
| `feat` | New feature or agent tool |
| `fix` | Bug fix |
| `chore` | Tooling, deps, config — no production behavior change |
| `docs` | Documentation only |
| `test` | Tests only |
| `refactor` | Code change without feature or fix |
| `ci` | GitHub Actions, CI config |
| `ml` | Model training, dataset, inference pipeline |
| `infra` | Docker, AWS, deploy scripts |

---

## Scopes

Use one primary scope per commit:

| Scope | Paths / domain |
| :--- | :--- |
| `frontend` | `frontend/`, Next.js, UI |
| `backend` | `backend/` APIs, services (non-ML) |
| `agent` | LangGraph, tools, prompts, RAG |
| `ml` | Models, parsers, scrapers, datasets |
| `infra` | Docker, AWS, CI, deploy |
| `db` | Migrations, SQLAlchemy models |
| `docs` | `docs/`, README |

Omit scope only for repo-wide chores: `chore: add editorconfig`.

---

## Examples

### Feature

```
feat(backend): add application kanban CRUD endpoints

Implements Application and StatusEvent models per API contract.

Refs #9
```

```
feat(agent): register score_resume_match LangGraph tool

Refs #20
```

```
feat(frontend): kanban drag-and-drop with status updates

Refs #10
```

### Fix

```
fix(frontend): persist kanban column after drag-and-drop

Refs #10
```

```
fix(ml): handle multi-column PDF resumes in parser

Refs #15
```

### ML / agent / infra

```
ml: train embedding matcher baseline on JD dataset

Refs #17
```

```
infra: add Bedrock invoke IAM policy to ECS task role

Refs #3
```

```
ci: run ruff and pytest on pull request

Refs #6
```

### Chore / docs

```
docs: add sprint backlog to PROJECT.md Section 18

Refs #2
```

```
chore(deps): bump fastapi to 0.115.x
```

---

## One logical change per commit

Prefer small commits within a branch:

- ✅ `feat(backend): add Application model` then `feat(backend): add application CRUD routes`
- ❌ One commit mixing kanban UI + scraper + unrelated README edit

The PR squash title should summarize the whole change; individual commits can be smaller.

---

## Squash merge titles

When merging a PR, set the squash commit title to match this format. GitHub uses the PR title by default — name PRs accordingly:

```
feat(backend): application kanban CRUD API (#9)
```

---

## Related docs

- [.gitmessage](../.gitmessage) — local commit template
- [BRANCH_WORKFLOW.md](BRANCH_WORKFLOW.md)
- [GITHUB_CONVENTIONS.md](GITHUB_CONVENTIONS.md)
