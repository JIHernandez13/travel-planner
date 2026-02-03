# Changelog

All notable changes to the Travel Planner project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

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
