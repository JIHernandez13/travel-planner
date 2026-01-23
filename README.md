# Travel Planner App

A modern web application for planning and organizing trips, built with a mobile-first mindset.

## Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **PostgreSQL** - Relational database
- **SQLAlchemy** - ORM for database operations
- **Pydantic** - Data validation

### Frontend
- **React** - UI framework
- **TypeScript** - Type-safe JavaScript
- **Vite** - Build tool
- **React Router** - Navigation
- **Axios** - HTTP client

### DevOps
- **Docker** - Containerization
- **Docker Compose** - Multi-container orchestration

## Project Structure

```
travel-planner/
├── backend/           # FastAPI backend
│   ├── app/
│   │   ├── api/      # API routes
│   │   ├── models/   # Database models
│   │   ├── schemas/  # Pydantic schemas
│   │   └── core/     # Config, dependencies
│   ├── tests/
│   └── requirements.txt
├── frontend/         # React frontend
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   └── types/
│   └── package.json
└── docs/            # Documentation
```

## Getting Started

### Prerequisites
- Python 3.11+
- Node.js 18+
- Docker & Docker Compose (optional but recommended)
- PostgreSQL (or use Docker)

### Environment Setup

1. **Create environment file:**
   ```bash
   cp .env.example .env
   ```

2. **Configure environment variables:**
   Edit `.env` and update the following critical values:
   
   **Security (REQUIRED):**
   - `SECRET_KEY` - Generate a strong secret key:
     ```bash
     openssl rand -hex 32
     ```
   - `POSTGRES_PASSWORD` - Set a strong database password
   
   **Database:**
   - `DATABASE_URL` - Update with your credentials
   - `POSTGRES_USER`, `POSTGRES_DB` - Customize as needed
   
   **Frontend:**
   - `VITE_API_URL` - Set to your backend API URL

### Quick Start

1. **Clone and navigate:**
   ```bash
   cd travel-planner
   ```

2. **Backend Setup:**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   uvicorn app.main:app --reload
   ```

3. **Frontend Setup:**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

4. **Using Docker (Recommended):**
   ```bash
   docker-compose up
   ```

## Development Workflow

- Backend runs on: `http://localhost:8000`
- Frontend runs on: `http://localhost:5173`
- API docs: `http://localhost:8000/docs`

## Testing

This project includes comprehensive unit testing and coverage reporting for both backend and frontend.

**Quick Start:**
```bash
# Backend tests
cd backend && pytest --cov

# Frontend tests
cd frontend && npm run test:coverage
```

For detailed testing instructions, see [TESTING.md](./TESTING.md)

**Test Coverage:**
- Backend: 80% minimum coverage target
- Frontend: 80% minimum coverage target

## Security Best Practices

### Authentication & Authorization
- **Access tokens expire in 60 minutes** by default (configurable via `ACCESS_TOKEN_EXPIRE_MINUTES`)
- Implement refresh tokens for longer sessions using `REFRESH_TOKEN_EXPIRE_MINUTES`
- All passwords must meet complexity requirements:
  - Minimum 8 characters
  - At least one uppercase letter
  - At least one lowercase letter
  - At least one digit
  - At least one special character

### Environment Variables
- **NEVER commit `.env` file** to version control
- Use `.env.example` as a template
- Generate strong random values for production:
  ```bash
  # Generate SECRET_KEY
  openssl rand -hex 32
  
  # Generate strong password
  openssl rand -base64 32
  ```

### Database Security
- Use strong passwords for database credentials
- Database credentials are configured via environment variables
- Connection pooling is optimized for production (configurable via `DB_POOL_SIZE` and `DB_MAX_OVERFLOW`)

### CORS Configuration
- CORS is restricted to specific origins defined in `ALLOWED_ORIGINS`
- Only necessary HTTP methods are allowed: GET, POST, PUT, DELETE, OPTIONS
- Only required headers are permitted: Content-Type, Authorization

### Token Storage
⚠️ **Security Note:** The frontend currently stores JWT tokens in localStorage, which is vulnerable to XSS attacks.

**For production, consider:**
- Using httpOnly cookies for token storage
- Implementing Content Security Policy (CSP) headers
- Adding CSRF protection for cookie-based authentication

### Docker Production Usage
- The Dockerfile is production-ready (no `--reload` flag)
- Development mode is enabled via docker-compose.yml override
- For production deployment:
  ```bash
  docker-compose -f docker-compose.yml -f docker-compose.prod.yml up
  ```

### Password Hashing
- All passwords are hashed using secure algorithms before storage
- Never log or expose plain-text passwords
- Password validation happens at the schema level

## Future Plans

- [ ] Mobile app with React Native
- [ ] Integration with travel APIs (Google Places, flight search)
- [ ] Social features (share itineraries)
- [ ] Offline support
