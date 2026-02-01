# CLAUDE.md - Travel Planner Codebase Guide

## Project Overview

A full-stack travel planning application built with **FastAPI** (Python backend) and **React + TypeScript** (frontend). Currently in **Phase 1 - Foundation** (~15% complete). The app has project scaffolding, database setup, auth infrastructure, CI/CD pipelines, and deployment configs in place, but most feature endpoints and UI pages are still TODO.

## Repository Structure

```
travel-planner/
├── backend/                  # FastAPI backend (Python 3.11+)
│   ├── main.py              # App entry point, CORS config, health endpoints
│   ├── config.py            # Pydantic settings from environment
│   ├── database.py          # SQLAlchemy engine, session factory, Base
│   ├── user.py              # User model (SQLAlchemy)
│   ├── requirements.txt     # Python dependencies
│   ├── Dockerfile           # Dev Docker image
│   └── Dockerfile.prod      # Production multi-stage Docker image
├── frontend/                 # React 18 + TypeScript + Vite
│   ├── src/
│   │   ├── main.tsx         # React entry point
│   │   ├── App.tsx          # Root component with React Router
│   │   ├── HomePage.tsx     # Landing page with API status check
│   │   ├── api.ts           # Axios client with auth interceptors
│   │   └── *.css            # Stylesheets
│   ├── package.json         # npm dependencies and scripts
│   ├── tsconfig.json        # TypeScript strict config (ES2020)
│   ├── vite.config.ts       # Vite build configuration
│   ├── eslint.config.js     # ESLint flat config
│   ├── Dockerfile           # Nginx-based production image
│   └── nginx.conf           # SPA routing, caching, security headers
├── .github/workflows/        # CI/CD
│   ├── build.yml            # PR checks: lint + build
│   ├── deploy-backend.yml   # Railway auto-deploy
│   ├── deploy-frontend.yml  # Vercel auto-deploy
│   ├── deploy-render.yml    # Full-stack Render deploy
│   └── manual-deploy.yml    # Manual deployment trigger
├── docker-compose.yml        # Local dev: postgres + backend + frontend
├── render.yaml               # Render platform blueprint
├── .flake8                   # Python linter config
├── .env.example              # Dev environment template
└── .env.production.example   # Production environment template
```

## Tech Stack

| Layer | Technology | Version |
|-------|-----------|---------|
| Backend framework | FastAPI | 0.109.0 |
| Backend server | Uvicorn | 0.27.0 |
| Database ORM | SQLAlchemy | 2.0.25 |
| Database | PostgreSQL | 16 |
| Migrations | Alembic | 1.13.1 |
| Auth | python-jose (JWT) + passlib (bcrypt) | 3.3.0 / 1.7.4 |
| Frontend framework | React | 18.2.0 |
| Frontend language | TypeScript (strict) | 5.3.3 |
| Build tool | Vite | 5.0.11 |
| HTTP client | Axios | 1.6.5 |
| Server state | TanStack React Query | 5.17.19 |
| Routing | React Router | 6.21.1 |

## Common Commands

### Local Development (Docker)

```bash
docker-compose up              # Start all services (postgres, backend, frontend)
docker-compose up --build      # Rebuild and start
docker-compose down            # Stop all services
docker-compose logs -f         # Follow logs
```

### Frontend

```bash
cd frontend
npm ci                         # Install deps (use ci, not install)
npm run dev                    # Dev server on http://localhost:5173
npm run build                  # TypeScript check + Vite production build
npm run lint                   # ESLint check
npm run preview                # Preview production build locally
```

### Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload      # Dev server on http://localhost:8000
```

### Code Quality

```bash
# Frontend
cd frontend && npx eslint .

# Backend
cd backend && flake8 .
cd backend && black .          # Auto-format Python code
```

## Code Style & Conventions

### Python (Backend)
- **Formatter**: black
- **Linter**: flake8 (max line length: 79 chars)
- **Config management**: Pydantic `BaseSettings` reading from environment variables
- **Database sessions**: Use `get_db()` dependency injection for SQLAlchemy sessions
- **API versioning**: Routes prefixed with `/api/v1`
- **Auth**: JWT Bearer tokens in Authorization header

### TypeScript (Frontend)
- **Strict mode** enabled (`noUnusedLocals`, `noUnusedParameters`, `noFallthroughCasesInSwitch`)
- **Target**: ES2020
- **Module resolution**: bundler
- **JSX**: react-jsx (new transform — no `import React` needed)
- **Linting**: ESLint with `@typescript-eslint` and `react-hooks` plugins
- **API calls**: Axios instance in `api.ts` with automatic Bearer token injection from localStorage
- **Routing**: React Router v6 with `BrowserRouter`

### General Conventions
- Environment variables for all secrets and configuration (never hardcode)
- `.env.example` documents all required variables
- CORS restricted to explicitly allowed origins
- Health check endpoints: `GET /` and `GET /health` on backend

## CI/CD Pipeline

**On Pull Request** (build.yml):
- Frontend: `npm ci` → `npm run lint` → `npm run build` (Node 18)
- Backend: `pip install` → `python -m compileall` → `flake8` (Python 3.11)

**On Push to main**:
- Backend changes → Railway deploy (deploy-backend.yml)
- Frontend changes → Vercel deploy (deploy-frontend.yml)
- Full-stack → Render deploy (deploy-render.yml)

All PRs must pass lint and build checks before merge.

## Environment Variables

Key variables (see `.env.example` for full list):

| Variable | Purpose |
|----------|---------|
| `DATABASE_URL` | PostgreSQL connection string |
| `SECRET_KEY` | JWT signing key |
| `ALGORITHM` | JWT algorithm (HS256) |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | JWT token TTL (default: 60) |
| `ALLOWED_ORIGINS` | Comma-separated CORS origins |
| `VITE_API_URL` | Backend URL for frontend (default: http://localhost:8000) |
| `ENVIRONMENT` | development / production |
| `DEBUG` | Enable debug mode |
| `DB_POOL_SIZE` | SQLAlchemy pool size (default: 5) |

## Architecture Notes

### Backend
- `main.py` — FastAPI app instance, CORS middleware, root health endpoints
- `config.py` — `Settings` class (Pydantic BaseSettings) loads all config from env
- `database.py` — SQLAlchemy engine with connection pooling, `SessionLocal` factory, `Base` declarative base, `get_db()` dependency
- `user.py` — User model with id, email, username, hashed_password, is_active, created_at, updated_at

### Frontend
- `api.ts` — Axios instance with request interceptor (adds JWT) and response interceptor (redirects to /login on 401). Exports `authAPI` and `tripsAPI` objects.
- `App.tsx` — BrowserRouter with route definitions
- `HomePage.tsx` — Landing page that checks backend connectivity via `/health`

### API Client Pattern
The frontend `api.ts` defines typed API interfaces:
- `authAPI`: register, login, logout, getCurrentUser
- `tripsAPI`: getAll, getById, create, update, delete
These call the backend at `VITE_API_URL` with automatic auth headers.

## What's Implemented vs TODO

**Done**: Project scaffolding, Docker setup, database connection, User model, JWT config, Axios client with auth, CI/CD pipelines, deployment configs, health endpoints.

**Not yet implemented**: Auth endpoints, database migrations, Trip/Activity models, CRUD API routes, frontend pages (Login, Register, Dashboard, TripDetail), component library, test suite, rate limiting, error handling middleware.

## Testing

- **Backend**: pytest + pytest-asyncio + httpx configured in requirements.txt. No tests written yet.
- **Frontend**: No test framework configured yet (Vitest recommended per docs).
- **CI**: Relies on lint + build checks for now. Add tests as features are implemented.

## Deployment

Three deployment paths are configured:

1. **Vercel (frontend) + Railway (backend)** — Separate platform deploys
2. **Render** — Full-stack blueprint via `render.yaml`
3. **Docker** — Self-hosted via `docker-compose.yml` and production Dockerfiles

## Important Files to Know

| File | Why it matters |
|------|---------------|
| `backend/main.py` | All current backend routes live here |
| `backend/config.py` | All backend configuration/settings |
| `backend/database.py` | Database engine and session setup |
| `frontend/src/api.ts` | All API call definitions and auth interceptors |
| `frontend/src/App.tsx` | All frontend route definitions |
| `docker-compose.yml` | Local development orchestration |
| `.github/workflows/build.yml` | PR check pipeline |
