# Test Coverage Analysis

## Current State: 0% Coverage

The codebase has **zero test files** across both backend and frontend. While `pytest`, `pytest-asyncio`, and `httpx` are listed in `backend/requirements.txt`, no tests, test configuration, or test fixtures exist. The frontend has no testing framework installed at all.

CI/CD (`build.yml`) runs only lint and build checks — no tests are executed.

---

## Backend: What Needs Testing

### Priority 1 — Health Endpoints (`main.py`)

Two live endpoints exist today. These are the lowest-hanging fruit.

| Endpoint | Method | What to test |
|----------|--------|--------------|
| `GET /` | root | Returns `{"message": "Travel Planner API", "version": "1.0.0"}` |
| `GET /health` | health_check | Returns `{"status": "healthy"}` |

**Recommended tests:**
- Response status codes (200)
- Response body structure and values
- CORS headers are present for allowed origins

### Priority 2 — Configuration (`config.py`)

The `Settings` class uses Pydantic `BaseSettings` with 15+ fields and default values. Misconfiguration silently breaks the app at runtime.

**Recommended tests:**
- Default values load correctly when no env vars are set
- `ALLOWED_ORIGINS` comma-separated string is parsed properly
- `DATABASE_URL` construction from components vs. direct URL
- Required vs. optional field behavior
- Invalid values are rejected (e.g., non-integer `DB_POOL_SIZE`)

### Priority 3 — Database Layer (`database.py`)

The session factory and `get_db()` dependency are used by every future endpoint.

**Recommended tests:**
- `get_db()` yields a session and closes it after use
- Engine is created with correct pool size from settings
- Session rollback on exception

### Priority 4 — User Model (`user.py`)

The SQLAlchemy model defines the schema for the users table.

**Recommended tests:**
- Model can be instantiated with valid data
- `created_at` and `updated_at` default to current time
- `is_active` defaults to `True`
- Required fields (email, username, hashed_password) cannot be null

### Priority 5 — Auth Endpoints (not yet implemented)

Once auth routes are built, they will be the most critical code to test:
- Registration with valid/invalid/duplicate data
- Login with correct/incorrect credentials
- JWT token generation, expiration, and validation
- Password hashing (never stored in plaintext)
- Protected route access with/without valid token

---

## Frontend: What Needs Testing

### Priority 1 — API Client (`api.ts`, 120 lines)

This is the highest-complexity frontend file. It contains request/response interceptors with side effects (localStorage reads, writes, and `window.location` redirects).

**Recommended tests:**
- Request interceptor attaches Bearer token from localStorage
- Request interceptor skips token when localStorage is empty
- Response interceptor redirects to `/login` on 401
- `authAPI.login()` stores token in localStorage
- `authAPI.logout()` removes token from localStorage
- `tripsAPI` methods call correct endpoints with correct HTTP methods
- Error responses are propagated correctly

### Priority 2 — HomePage Component (`HomePage.tsx`)

Contains `useState`/`useEffect` with an async fetch call and conditional rendering.

**Recommended tests:**
- Renders loading state initially
- Shows "connected" status when API responds successfully
- Shows error state when API is unreachable
- Fetch is called on mount with correct URL

### Priority 3 — App Component (`App.tsx`)

Routing skeleton — low complexity but important to verify routes render correctly.

**Recommended tests:**
- `/` route renders HomePage
- Unknown route behavior (404 handling when added)

---

## Infrastructure Gaps to Address

### Backend

1. **Create `backend/tests/` directory** with `__init__.py` and `conftest.py`
2. **Add `pytest-cov`** to `requirements.txt` for coverage reporting
3. **Create test fixtures** in `conftest.py`:
   - `TestClient` using httpx `ASGITransport` for async endpoint testing
   - Test database session (SQLite in-memory or test PostgreSQL)
   - Settings override fixture to avoid needing real env vars
4. **Add `pytest.ini` or `[tool.pytest.ini_options]`** section for test discovery config

### Frontend

1. **Install Vitest** (recommended — native Vite integration, faster than Jest):
   ```
   npm install -D vitest @testing-library/react @testing-library/jest-dom @testing-library/user-event jsdom
   ```
2. **Create `vitest.config.ts`** with jsdom environment
3. **Add test script** to `package.json`: `"test": "vitest run"`
4. **Create `src/__tests__/`** directory or colocate `*.test.ts(x)` files

### CI/CD

1. **Update `build.yml`** to run `pytest` in the backend job
2. **Update `build.yml`** to run `npm test` in the frontend job
3. **Add coverage thresholds** to fail the build if coverage drops below a minimum (e.g., 80%)
4. **Add coverage reporting** as PR comments (e.g., via `pytest-cov` + GitHub Actions)

---

## Suggested Implementation Order

| Step | Area | Effort | Impact |
|------|------|--------|--------|
| 1 | Backend test infrastructure (conftest, fixtures) | Low | Unblocks all backend tests |
| 2 | Health endpoint tests (`test_main.py`) | Low | Quick win, validates setup works |
| 3 | Config tests (`test_config.py`) | Low | Catches env var misconfigurations |
| 4 | Frontend test infrastructure (Vitest setup) | Low | Unblocks all frontend tests |
| 5 | API client tests (`api.test.ts`) | Medium | Highest-complexity frontend code |
| 6 | Database layer tests (`test_database.py`) | Medium | Critical for all future features |
| 7 | User model tests (`test_user.py`) | Low | Schema validation |
| 8 | HomePage component tests | Medium | First component test |
| 9 | CI/CD pipeline integration | Low | Enforces test execution on PRs |
| 10 | Auth endpoint tests (when implemented) | High | Most security-critical code path |

---

## Summary

| Metric | Current | Target |
|--------|---------|--------|
| Backend test files | 0 | 4+ |
| Frontend test files | 0 | 3+ |
| Test coverage | 0% | 80%+ |
| CI test execution | No | Yes |
| Coverage reporting | No | Yes |

The most impactful first step is setting up the test infrastructure on both sides (conftest.py + Vitest config), then writing tests for existing code starting with the backend health endpoints and frontend API client.
