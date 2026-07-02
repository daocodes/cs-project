# InternBase API Contract (Phase 1)

This document defines the backend REST contract for Tracker MVP work.

## Purpose

- Keep frontend and backend aligned before parallel implementation.
- Define stable request and response shapes for Phase 1.
- Make validation and test expectations explicit.

## Contract status

- Implemented today:
  - `GET /`
  - `GET /health`
- Planned in this contract (Phase 1 target):
  - Tracker endpoints under `/applications` and `/status-events`.

## Base conventions

- Base URL (local): `http://localhost:8000`
- Content type: `application/json`
- Auth: required for `/applications*` routes via backend `get_current_user` dependency.
  - Current local mode: mock auth (`AUTH_MODE=mock`).
  - Planned production mode: Cognito token verification (`AUTH_MODE=cognito`).
  - Client does not send `user_id`; backend derives ownership from current user context.
- Datetime format (future fields): ISO 8601 UTC string.

## Enums

### `ApplicationStatus`

`SAVED` | `APPLIED` | `OA` | `PHONE_SCREEN` | `TECHNICAL` | `BEHAVIORAL` | `ONSITE` | `OFFER` | `REJECTED` | `GHOSTED` | `WITHDRAWN`

## Error format

For contract consistency, endpoints should return:

```json
{
  "detail": "Human-readable error message"
}
```

Common statuses:

- `400` bad request / validation failure
- `401` unauthorized / missing auth context
- `404` resource not found
- `409` conflict (future use)
- `422` schema validation error (FastAPI default)
- `500` unexpected server error

## Health endpoints

### `GET /`

- Purpose: basic service hello route.
- Response `200`:

```json
{
  "details": "Hello from FastAPI"
}
```

### `GET /health`

- Purpose: container and API liveness check.
- Response `200`:

```json
{
  "ok": true
}
```

## Tracker endpoints (Phase 1)

### `GET /applications`

- Purpose: list applications for the authenticated user.
- Query params:
  - `status` (optional, `ApplicationStatus`)
- Response `200`:

```json
[
  {
    "id": 1,
    "user_id": 10,
    "job_posting_id": 25,
    "status": "APPLIED",
    "notes": "Submitted via referral"
  }
]
```

### `POST /applications`

- Purpose: create application row.
- Request body:

```json
{
  "job_posting_id": 25,
  "status": "SAVED",
  "notes": "Draft entry"
}
```

- Response `201`:

```json
{
  "id": 1,
  "user_id": 10,
  "job_posting_id": 25,
  "status": "SAVED",
  "notes": "Draft entry"
}
```

### `GET /applications/{application_id}`

- Purpose: fetch one application by id, scoped to authenticated ownership.
- Response `200`:

```json
{
  "id": 1,
  "user_id": 10,
  "job_posting_id": 25,
  "status": "APPLIED",
  "notes": "Submitted via referral"
}
```

### `PATCH /applications/{application_id}`

- Purpose: partial update for editable fields on an owned application.
- Editable fields:
  - `status`
  - `notes`
- If `status` changes, backend should append a `StatusEvent`.
- Request body example:

```json
{
  "status": "PHONE_SCREEN",
  "notes": "Recruiter call booked for Friday"
}
```

- Response `200`:

```json
{
  "id": 1,
  "user_id": 10,
  "job_posting_id": 25,
  "status": "PHONE_SCREEN",
  "notes": "Recruiter call booked for Friday"
}
```

### `DELETE /applications/{application_id}`

- Purpose: delete an owned application.
- Response `204`: no body.

### `GET /applications/{application_id}/status-events`

- Purpose: read status transition history for one owned application.
- Response `200`:

```json
[
  {
    "id": 1,
    "application_id": 1,
    "from_status": "SAVED",
    "to_status": "APPLIED",
    "source": "manual"
  },
  {
    "id": 2,
    "application_id": 1,
    "from_status": "APPLIED",
    "to_status": "PHONE_SCREEN",
    "source": "manual"
  }
]
```

## Related model notes

- `applications` maps to `Application` model:
  - `id`, `user_id`, `job_posting_id`, `status`, `notes`
- `status_events` maps to `StatusEvent` model:
  - `id`, `application_id`, `from_status`, `to_status`, `source`

## Out of scope for this contract

- Auth token flows (Cognito)
- Resume upload/matcher APIs
- Agent APIs
- Discovery and roadmap APIs

Those are defined in later phase contracts as they are scoped.
