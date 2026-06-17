# InternBase Local Development

## Prerequisites

- Docker Desktop

## Start The Full Stack

From the repository root:

```bash
cp .env.example .env
docker compose up --build
```

## Services

- Frontend (Next.js): `http://localhost:3000`
- Backend (FastAPI): `http://localhost:8000`
- Backend health: `http://localhost:8000/health`
- Postgres: `localhost:5432`

## Stop The Stack

```bash
docker compose down
```
