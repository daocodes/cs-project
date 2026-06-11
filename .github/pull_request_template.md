## Summary

<!-- What changed and why (1–3 sentences) -->

## Linked issues

<!-- Closes #123, Relates to #456 -->

- Closes #
- Relates to #

## PROJECT.md

- [ ] No product scope change
- [ ] Updated [docs/PROJECT.md](docs/PROJECT.md) — section: <!-- link or N/A -->

## Type of change

- [ ] Feature — branch `feature/…` (`feat`)
- [ ] Fix — branch `fix/…` (`fix`)
- [ ] Chore — branch `chore/…` (`chore`, `docs`, `ci`, `refactor`)

## Screenshots / agent trace

<!-- UI changes, Monaco diff, agent trace panel — or N/A -->

## Test plan

- [ ] `docker compose up` — stack starts locally
- [ ] Backend: `pytest` passes (or note what was run)
- [ ] Frontend: `lint` / `tsc` passes (or note what was run)
- [ ] Manual verification: <!-- steps -->
- [ ] Agent smoke eval (if `area:agent` or agent paths changed)

## Reviewer checklist

- [ ] Acceptance criteria from linked issue are met
- [ ] API contract respected ([docs/API_CONTRACT.md](docs/API_CONTRACT.md) when it exists)
- [ ] No secrets, `.env`, or credentials in diff
- [ ] DB migrations noted and reversible (if applicable)
- [ ] Error handling reasonable; no silent failures on user paths
- [ ] Matches [commit conventions](docs/COMMIT_CONVENTIONS.md) and [branch workflow](docs/BRANCH_WORKFLOW.md)

## Deploy notes

<!-- Env vars, migrations, AWS/IAM changes — or N/A -->

- Env vars:
- Migrations:
- AWS / infra:
