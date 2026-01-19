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

## Future Plans

- [ ] Mobile app with React Native
- [ ] Integration with travel APIs (Google Places, flight search)
- [ ] Social features (share itineraries)
- [ ] Offline support
