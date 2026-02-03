# Changelog

All notable changes to the Travel Planner project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Added
- Alembic migrations framework initialized with env.py configured for app settings
- Initial database migration for User table (create_users_table)

## [0.2.0] - 2026-02-03

### Added
- Authentication API endpoints: register, login, get current user
- Pydantic schemas for auth request/response validation
- Password hashing with bcrypt via passlib CryptContext
- JWT access token creation and verification
- OAuth2PasswordBearer dependency for protected routes
- Login supports both username and email as identifier
- Auth test suite (9 tests covering register, login, me endpoints)
- React AuthContext with useAuth hook for auth state management
- Login page with error handling and redirect
- Registration page with client-side validation (email, password match, min length)
- Protected route wrapper component using React Router Outlet
- Dashboard page for authenticated users with user info display
- QueryClientProvider setup with TanStack React Query

### Fixed
- Broken imports in database.py (was referencing non-existent app.core.config)
- Broken imports in user.py (was referencing non-existent app.core.database)
- SQLite compatibility in database.py for test environments
- TypeScript include paths in tsconfig.json (was pointing to non-existent src/ dir)
- Pinned bcrypt==4.0.1 to fix passlib compatibility

## [0.1.0] - 2025-01-01

### Added
- FastAPI backend with health check endpoints (`/` and `/health`)
- SQLAlchemy database setup with PostgreSQL 16 and connection pooling
- User model with authentication fields (email, username, hashed_password)
- Pydantic-based configuration management via environment variables
- JWT authentication infrastructure (python-jose + passlib)
- React 18 + TypeScript frontend with Vite build tooling
- Axios HTTP client with JWT auth interceptors and 401 redirect handling
- React Router v6 routing setup
- TanStack React Query for server state management
- Landing page with backend connectivity check
- Typed API client interfaces for auth and trips endpoints
- Docker Compose local development environment (PostgreSQL, backend, frontend)
- Production Dockerfiles for backend (multi-stage) and frontend (Nginx)
- Nginx configuration with SPA routing, caching, and security headers

### Fixed
- PR build checks for reorganized project structure

### Infrastructure
- GitHub Actions CI pipeline: lint + build checks on pull requests
- Railway auto-deploy workflow for backend
- Vercel auto-deploy workflow for frontend
- Render full-stack deploy workflow with `render.yaml` blueprint
- Manual deployment trigger workflow
- ESLint flat config with TypeScript and React hooks plugins
- Flake8 + Black Python code quality tooling
- CLAUDE.md codebase guide for AI-assisted development
- pytest + httpx test setup with health endpoint tests
- Test coverage analysis with prioritized improvement plan
