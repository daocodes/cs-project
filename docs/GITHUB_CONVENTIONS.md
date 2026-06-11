# GitHub Conventions

Conventions for the InternBase repo. Ground truth for product scope lives in [PROJECT.md](PROJECT.md). Every issue should trace to a section there.

---

## Repository rules

| Rule | Detail |
| :--- | :--- |
| **Default branch** | `main` — always deployable or clearly marked broken |
| **Protection** | No direct pushes to `main`; PR required; 1 approving review from partner |
| **CI** | All checks must pass before merge |
| **Secrets** | Never commit `.env`, API keys, or AWS credentials |
| **Docs** | If behavior diverges from `docs/PROJECT.md`, update the doc in the same PR |

---

## Milestones

Milestones map to build phases in [PROJECT.md Section 12](PROJECT.md#12-build-phases).

| Milestone | Phase | Target |
| :--- | :--- | :--- |
| `Phase 0` | Setup | Sprint 0 (Jun 11–17) |
| `Phase 1` | Tracker MVP + IDE Shell | Sprint 0 |
| `Phase 2` | Resume Matcher | Sprint 1 |
| `Phase 2.5` | Lightweight Roadmap | Sprint 2 |
| `Phase 3` | Resume Tailoring | Sprint 2 |
| `Phase 4` | Internship Aggregation | Sprint 3 |
| `Phase 5` | Email Status Detection | Post–Jul 10 backlog |
| `Phase 6` | Agent Integration + Eval | Sprint 3 |
| `Phase 7` | Polish & Portfolio | Sprint 3 |
| `v1.0.0-jul10` | V1 release | July 10, 2026 |

Close a milestone only when that phase's definition-of-done is met **and** integrated on the deployed environment (where applicable).

---

## Labels

Create these labels in the GitHub repo. Use exactly one `area:*`, one `type:*`, and one `priority:*` per issue when possible.

### Area

| Label | Use for |
| :--- | :--- |
| `area:frontend` | Next.js, UI, Monaco, IDE shell |
| `area:backend` | FastAPI, SQLAlchemy, APIs |
| `area:ml` | Models, datasets, scrapers, parsers |
| `area:infra` | AWS, Docker, CI/CD, deploy |
| `area:agent` | LangGraph, RAG, MCP, prompts, eval |

### Type

Three types only — matches branch prefixes (`feature/`, `fix/`, `chore/`):

| Label | Use for | Branch |
| :--- | :--- | :--- |
| `type:feature` | New user-facing or agent capability | `feature/<issue#>-<slug>` |
| `type:fix` | Something broken that worked or should work | `fix/<issue#>-<slug>` |
| `type:chore` | Tooling, deps, docs, setup, refactors, time-boxed research | `chore/<issue#>-<slug>` |

### Priority

| Label | Meaning |
| :--- | :--- |
| `priority:P0` | Blocks sprint goal or V1 — do now |
| `priority:P1` | Important for V1 — schedule this sprint |
| `priority:P2` | Nice for V1 — cut if behind |
| `priority:P3` | Post–V1 / backlog |

### Sprint

| Label | Dates |
| :--- | :--- |
| `sprint:0` | Jun 11–17 |
| `sprint:1` | Jun 18–24 |
| `sprint:2` | Jun 25–Jul 1 |
| `sprint:3` | Jul 2–10 |

Remove the previous sprint label when moving an issue to the next sprint.

### Other

| Label | Use for |
| :--- | :--- |
| `good-first-task` | Small, well-scoped, low risk |
| `blocked` | Waiting on external dependency or partner decision |

---

## Issues

### One issue = one shippable task

Each issue should be completable in ≤3 days by one person. If larger, split into sub-issues under a parent epic.

### Required issue fields

1. **Title** — `[area] Imperative summary` (e.g. `[frontend] Kanban drag-and-drop`)
2. **Milestone** — Phase milestone from table above
3. **Labels** — `area:*`, `type:*`, `priority:*`, `sprint:*` (if in active sprint)
4. **Assignee** — Person A, Person B, or both for paired work
5. **PROJECT.md link** — Section reference in issue body
6. **Acceptance criteria** — Checkbox list (3–5 items)

### Epics and sub-issues

- Create **sub-issues** for individual tasks; link via GitHub sub-issues.



### Issue templates

Use the repo templates when creating issues:

- **Feature** — new capability (`type:feature`)
- **Fix** — defect with repro steps (`type:fix`)
- **Chore** — tooling, docs, setup, research (`type:chore`)

Blank issues are disabled; use a template.

---

## Pull requests

### Branch naming

See [BRANCH_WORKFLOW.md](BRANCH_WORKFLOW.md). Pattern: `<type>/<issue#>-<short-slug>`.

Examples: `feature/9-tracker-crud-api`, `fix/10-kanban-dnd`.

### PR title

Match [commit conventions](COMMIT_CONVENTIONS.md): `feat(backend): application kanban CRUD API`

### PR body

Use the [pull request template](../.github/pull_request_template.md). Required:

- Summary (what / why)
- `Closes #N` or `Relates to #N`
- Test plan checklist
- PROJECT.md updated? (if scope changed)

### Review rules

- **Reviewer:** Partner (the person not primarily assigned to the issue)
- **Turnaround:** Review within 24 hours
- **Merge:** Squash merge preferred; delete branch after merge
- **Draft PRs:** Open early in the sprint for visibility

### CI gates

- Lint + test must pass
- Agent smoke eval (5 tasks) when `area:agent` files change (once harness exists)

---


---

## Definition of done

### Per issue

- [ ] Acceptance criteria met
- [ ] PR merged to `main`
- [ ] Partner approved review
- [ ] CI green
- [ ] No secrets committed
- [ ] PROJECT.md / API contract updated if behavior changed

### Per phase

See [PROJECT.md Section 12](PROJECT.md#12-build-phases) — each phase lists **Done when** criteria. Integration phases (1+) require deployed verification unless explicitly local-only.

### V1 (July 10, 2026)

See [PROJECT.md Section 15](PROJECT.md#15-definition-of-done-v1) and [Section 18 sprint scope](PROJECT.md#18-sprint-schedule--github-backlog).

---

## Commit messages

Follow [COMMIT_CONVENTIONS.md](COMMIT_CONVENTIONS.md). Enable the local template:

```bash
git config commit.template .gitmessage
```

---

## One-time repo setup checklist

Run once after creating the GitHub repo:

1. [ ] Create milestones `Phase 0`–`Phase 7` and `v1.0.0-jul10`
2. [ ] Create all labels from this doc
3. [ ] Enable **sub-issues** in repository settings
4. [ ] Create GitHub Project board with columns above
5. [ ] Enable branch protection on `main` (require PR, 1 review, require CI)
6. [ ] Create epics E0–E8 and sub-issues from [PROJECT.md Section 18](PROJECT.md#18-sprint-schedule--github-backlog)
7. [ ] Add both collaborators with write access
8. [ ] Verify issue and PR templates appear on new issue/PR forms

### Bulk issue creation (optional)

```bash
# Example — adjust repo and labels
gh issue create --title "[Epic] Phase 0 — Project Setup" \
  --label "type:feature,priority:P0,sprint:0" \
  --milestone "Phase 0" \
  --body "Parent epic. See docs/PROJECT.md Section 18."
```

---

## Related docs

- [PROJECT.md](PROJECT.md) — product ground truth and full backlog
- [BRANCH_WORKFLOW.md](BRANCH_WORKFLOW.md) — scrum branch workflow
- [COMMIT_CONVENTIONS.md](COMMIT_CONVENTIONS.md) — commit message format
- [tools/TOOLS.md](../tools/TOOLS.md) — code review and dev tools catalog
