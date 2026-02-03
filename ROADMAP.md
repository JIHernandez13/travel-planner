# Feature Roadmap

> **Last updated**: 2026-02-03
> **Current status**: Phase 1 — Foundation (~85% complete)

## Overview

Travel Planner is a full-stack trip planning application. This roadmap tracks feature development from initial scaffolding through to a mobile app. Each phase builds on the previous one.

**Legend**: ✅ Done | 🔧 In Progress | ⬚ Not Started

---

## Phase 1: Foundation (Weeks 1–2)

The groundwork — project scaffolding, infrastructure, auth, and basic data models.

### Backend Infrastructure ✅
- [x] FastAPI project setup with CORS, health endpoints
- [x] PostgreSQL database connection (SQLAlchemy 2.0, connection pooling)
- [x] Pydantic `BaseSettings` configuration management
- [x] User model (id, email, username, hashed_password, is_active, timestamps)
- [x] Database session factory with `get_db()` dependency injection
- [x] JWT + bcrypt libraries installed and configured

### Frontend Infrastructure ✅
- [x] React 18 + TypeScript (strict) + Vite setup
- [x] React Router v6 with `BrowserRouter`
- [x] Axios HTTP client with JWT interceptors and 401 handling
- [x] API client interfaces defined (`authAPI`, `tripsAPI`)
- [x] TanStack React Query installed
- [x] ESLint with TypeScript and React Hooks plugins
- [x] HomePage with backend connectivity check

### DevOps & CI/CD ✅
- [x] Docker Compose for local dev (PostgreSQL + backend + frontend)
- [x] Production Dockerfiles (multi-stage builds)
- [x] GitHub Actions: PR lint/build checks (`build.yml`)
- [x] GitHub Actions: auto-deploy to Railway, Vercel, Render
- [x] Manual deployment trigger workflow
- [x] Render blueprint (`render.yaml`)
- [x] Environment variable templates (`.env.example`, `.env.production.example`)

### Testing Setup ✅
- [x] pytest + pytest-asyncio + httpx installed
- [x] Health endpoint tests (`test_health.py`)
- [x] pytest integrated into CI pipeline
- [ ] Alembic migrations initialized
- [ ] Database migration for User table

### Authentication ✅
- [x] `POST /api/v1/auth/register` — user registration with validation
- [x] `POST /api/v1/auth/login` — JWT token generation (OAuth2 form)
- [x] `GET /api/v1/auth/me` — get current user profile
- [x] Password hashing with bcrypt via passlib
- [x] `get_current_user` dependency for protected routes
- [x] Auth endpoint tests (9 tests covering register, login, me)

### Auth UI ✅
- [x] Login page (`/login`)
- [x] Registration page (`/register`) with client-side validation
- [x] Protected route wrapper component
- [x] Auth state management (React Context + useAuth hook)
- [x] Token persistence in localStorage
- [x] Dashboard page for authenticated users

---

## Phase 2: Core Features (Weeks 3–4)

Trip CRUD and basic itinerary management — the core product loop.

### Trip Management
- [ ] **Model**: Trip (name, destination, start_date, end_date, budget, description, user_id)
- [ ] **API**: `POST /api/v1/trips` — create trip
- [ ] **API**: `GET /api/v1/trips` — list user's trips (with pagination)
- [ ] **API**: `GET /api/v1/trips/{id}` — trip detail
- [ ] **API**: `PUT /api/v1/trips/{id}` — update trip
- [ ] **API**: `DELETE /api/v1/trips/{id}` — delete trip
- [ ] **API**: Authorization checks (users can only access own trips)
- [ ] **UI**: Trip list page (`/trips`)
- [ ] **UI**: Create/edit trip form
- [ ] **UI**: Trip detail page (`/trips/:id`)

### Itinerary Planning
- [ ] **Model**: Activity (name, time, location, type, cost, notes, trip_id, day_number, order)
- [ ] **API**: CRUD endpoints for activities linked to trips
- [ ] **UI**: Daily itinerary view within trip detail
- [ ] **UI**: Add/edit/delete activities
- [ ] **UI**: Drag-and-drop reordering of activities

### Layout & Navigation
- [ ] Header component with nav links and user menu
- [ ] Sidebar for trip navigation
- [ ] Footer component
- [ ] Responsive layout shell

---

## Phase 3: Enhanced Features (Weeks 5–6)

Map integration, budget tracking, and collaboration to make the app genuinely useful.

### Map Integration
- [ ] Google Maps JavaScript API integration
- [ ] Display trip destination on map
- [ ] Show activity locations as pins
- [ ] Calculate distances and travel time between activities
- [ ] Interactive map with click-to-add-activity

### Budget Tracking
- [ ] **Model**: Expense (amount, currency, category, description, activity_id, trip_id)
- [ ] **API**: Expense CRUD endpoints
- [ ] **UI**: Budget dashboard with planned vs. actual spending
- [ ] **UI**: Expense categorization (food, transport, lodging, activities, etc.)
- [ ] **UI**: Per-trip and per-day budget breakdowns
- [ ] Currency conversion support

### Collaboration
- [ ] **Model**: TripShare (trip_id, user_id, permission_level)
- [ ] Share trips via email invite or link
- [ ] Permission levels: viewer, editor, admin
- [ ] **UI**: Share dialog and collaborator management
- [ ] Comments/notes on activities and trips

---

## Phase 4: Polish & Testing (Weeks 7–8)

Harden the app with tests, error handling, and responsive design.

### Testing
- [ ] Backend unit tests (models, utilities, auth)
- [ ] Backend integration tests (API endpoints with test database)
- [ ] Frontend component tests (Vitest + React Testing Library)
- [ ] API client mock tests
- [ ] E2E tests with Playwright
- [ ] CI pipeline runs full test suite
- [ ] Target: 80%+ code coverage

### UX Polish
- [ ] Mobile-responsive design across all pages
- [ ] Loading skeletons and error states
- [ ] Toast notifications for actions
- [ ] Form validation with clear error messages
- [ ] Empty states for lists (no trips, no activities)
- [ ] Keyboard navigation and accessibility (WCAG 2.1 AA)

### Performance
- [ ] Database indexing for common queries
- [ ] API response caching (Redis or in-memory)
- [ ] Frontend code splitting and lazy loading
- [ ] Image optimization and lazy loading
- [ ] Lighthouse performance audit (target: 90+)

### Error Handling & Observability
- [ ] Structured error responses from API
- [ ] Global error boundary in React
- [ ] Request logging middleware
- [ ] Error tracking integration (Sentry or similar)
- [ ] Rate limiting on auth and write endpoints

---

## Phase 5: External Integrations (Weeks 9–10)

Connect to travel APIs to enrich the planning experience.

### Travel APIs
- [ ] Google Places API — search restaurants, attractions, hotels
- [ ] Weather API — forecast for trip dates and destination
- [ ] Flight search API (Skyscanner/Amadeus) — optional
- [ ] Hotel search API — optional
- [ ] Currency conversion API (exchangerate-api or similar)

### Smart Suggestions
- [ ] Auto-suggest destinations based on input
- [ ] Recommend popular attractions for a destination
- [ ] Travel tips and safety warnings per country
- [ ] Packing list suggestions based on destination and dates

---

## Phase 6: API Hardening & Design System (Weeks 11–12)

Prepare the codebase for mobile by standardizing the API and extracting reusable components.

### API Finalization
- [ ] Audit all endpoints for RESTful consistency
- [ ] Pagination on all list endpoints (cursor-based)
- [ ] Rate limiting across all endpoints
- [ ] API versioning strategy (v1 prefix already in place)
- [ ] OpenAPI/Swagger documentation complete and accurate
- [ ] Optimize response payload sizes

### Frontend Design System
- [ ] Extract reusable component library (buttons, inputs, cards, modals)
- [ ] Design tokens (colors, spacing, typography)
- [ ] Component documentation (Storybook or similar)
- [ ] Prepare shared components for React Native reuse

---

## Phase 7: React Native Mobile App (Week 13+)

Bring the trip planner to mobile with a native experience.

### Setup & Auth
- [ ] Initialize React Native project (Expo or bare)
- [ ] Navigation setup (React Navigation)
- [ ] Port authentication flow (login, register, token management)
- [ ] Shared API client library

### Core Features
- [ ] Trip list and detail screens
- [ ] Activity management
- [ ] Map view with native maps
- [ ] Budget tracking

### Mobile-Specific
- [ ] Offline mode with local storage sync
- [ ] Push notifications (trip reminders, collaborator updates)
- [ ] Camera integration for trip photos
- [ ] GPS location tracking for real-time itinerary

---

## Ongoing / Cross-Cutting

These are maintained continuously, not tied to a specific phase.

### Security
- [ ] Input validation on all endpoints (Pydantic models)
- [ ] SQL injection prevention (parameterized queries via SQLAlchemy)
- [ ] XSS protection (React auto-escaping + CSP headers)
- [ ] CSRF protection
- [ ] Rate limiting on sensitive endpoints
- [ ] Dependency vulnerability scanning in CI

### Documentation
- [x] CLAUDE.md — AI assistant codebase guide
- [x] Deployment guides and production readiness docs
- [ ] API documentation (auto-generated from OpenAPI)
- [ ] User-facing help documentation
- [ ] Contributing guide

### Monitoring
- [ ] Health check monitoring (uptime)
- [ ] Application performance monitoring
- [ ] Error rate alerting
- [ ] Database query performance tracking
- [ ] Privacy-friendly usage analytics
