# AI Agent Coding Guide for Travel Planner

Concise, actionable context to help AI agents be productive immediately in this repo.

## Architecture Overview
- Backend: FastAPI app with SQLAlchemy ORM and Pydantic settings. Core files: `backend/app/main.py`, `backend/config.py`, `backend/database.py`, `backend/user.py`.
- Frontend: React + TypeScript via Vite. Core files: `frontend/src/App.tsx`, `frontend/src/HomePage.tsx`, `frontend/src/api.ts`, `frontend/vite.config.ts`.
- Data flow: Frontend calls REST endpoints under `/api/v1/...`; backend exposes `/` and `/health` plus API routes (`auth`, `trips`, `activities`). Routers defined in `backend/app/api/`.
- CORS: Configured in `backend/app/main.py` from `settings.ALLOWED_ORIGINS`.

## Important Conventions
- Configuration via `.env` loaded by `pydantic-settings` in `backend/config.py`. Required keys: `DATABASE_URL`, `SECRET_KEY`.
- `API_V1_PREFIX` is `/api/v1`; frontend `api.ts` assumes auth/trips endpoints under this prefix.
- DB engine/pooling is selected by `settings.DATABASE_URL`; in tests, an in-memory SQLite DB is used.
- Frontend stores JWT in `localStorage` (see `frontend/src/api.ts` interceptors). For production, note comments about httpOnly cookies/CSP.

## Developer Workflows
- Local backend (dev): `uvicorn app.main:app --reload` from `backend/`. Docker Compose uses `uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload`.
- Local frontend (dev): `npm run dev` from `frontend/` (Vite dev server on port 5173).
- Docker (recommended quick start): `docker-compose up` from repo root. Services: `db` (Postgres), `backend`, `frontend`.
- Quick deploy helper: `./quick-deploy.sh` supports Vercel+Railway/Render/Docker; it builds/lints frontend and sanity-checks backend.

## Testing Patterns
- Backend tests in `backend/tests/` use fixtures from `conftest.py` to set environment and an in-memory SQLite via `StaticPool`. Key tests: `test_main.py` (health/root), `test_config.py` (settings), `test_database.py` (sessions), `test_user.py` (model CRUD/constraints).
- Frontend tests via Vitest in `frontend/src/test/`. `api.test.ts` mocks Axios via `vi.mock('axios')`; component tests validate Router/default route and HomePage behaviors.
- Coverage targets configured at ~80% in `frontend/vite.config.ts`; run `pytest --cov` (backend) and `npm run test:coverage` (frontend).

## Building & Running
- Frontend production build: `npm run build` then serve via Nginx (see `frontend/Dockerfile` and `frontend/nginx.conf`).
- Backend dependencies: `pip install -r backend/requirements.txt`. DB URL and secrets must be set via `.env`.
- Compose services expose: Frontend `5173`, Backend `8000`, Postgres `5432`.

## Cross-Component Integration
- Base API URL: `import.meta.env.VITE_API_URL` (defaults to `http://localhost:8000`). Ensure this matches backend when using containers or cloud.
- Endpoint contracts assumed by frontend:
  - `POST /api/v1/auth/register`, `POST /api/v1/auth/login`, `GET /api/v1/auth/me` (see `frontend/src/api.ts`).
  - Trips CRUD under `/api/v1/trips` (stub implementations in `backend/app/api/trips.py`).
- Backend routers in `backend/app/api/` (auth, trips, activities) are included in `backend/app/main.py`.

## Examples & References
- Settings/Env: See `backend/config.py` for required env and CORS origins.
- DB session dependency: `backend/database.py#get_db()` generator pattern used across tests.
- User model schema: `backend/user.py` with uniqueness constraints and timestamps; tested in `backend/tests/test_user.py`.
- Frontend API client: `frontend/src/api.ts` axios instance + interceptors; error handling redirects on 401.
- Health checks: `GET /` and `GET /health` in `backend/app/main.py`; `HomePage.tsx` probes `/` to show connection status.
- API routers: `backend/app/api/auth.py`, `backend/app/api/trips.py`, `backend/app/api/activities.py` (stub implementations with TODOs).

## Gotchas
- Ensure `.env` exists at repo root for Compose (`env_file: .env` used by services).
- Tests import using path injection in `backend/tests/conftest.py`; keep module names stable when refactoring.
- The old `backend/main.py` at repo root is superseded by `backend/app/main.py`; tests now import from `app.main`.

## When Adding Features
- Backend endpoints: define FastAPI routers and include them in `backend/app/main.py`. Match `API_V1_PREFIX` and the paths used by `frontend/src/api.ts`.
- Schemas: add Pydantic models (e.g., `Trip`) and validate inputs/outputs consistently.
- DB models/migrations: add SQLAlchemy models and generate Alembic migrations (see `requirements.txt` includes `alembic`).
- Frontend calls: extend `api.ts` and create pages/components; keep types in sync with backend responses.
