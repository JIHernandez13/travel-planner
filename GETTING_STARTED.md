# Quick Start Guide

## Prerequisites Installation

### 1. Install Python (3.11+)
```bash
# Check if Python is installed
python3 --version

# If not installed:
# macOS/Linux: Use package manager (brew, apt, etc.)
# Windows: Download from python.org
```

### 2. Install Node.js (18+)
```bash
# Check if Node is installed
node --version

# If not installed:
# macOS: brew install node
# Linux: Use package manager
# Windows: Download from nodejs.org
```

### 3. Install PostgreSQL
```bash
# macOS
brew install postgresql@16
brew services start postgresql@16

# Linux (Ubuntu/Debian)
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql

# Windows: Download installer from postgresql.org
```

## Option 1: Quick Start with Docker (Recommended)

1. **Install Docker Desktop**
   - Download from docker.com

2. **Start the Application**
   ```bash
   cd travel-planner
   docker-compose up
   ```

3. **Access the Application**
   - Frontend: http://localhost:5173
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

That's it! Everything runs in containers.

## Option 2: Manual Setup

### Backend Setup

1. **Navigate to backend directory**
   ```bash
   cd travel-planner/backend
   ```

2. **Create virtual environment**
   ```bash
   python3 -m venv venv
   ```

3. **Activate virtual environment**
   ```bash
   # macOS/Linux
   source venv/bin/activate
   
   # Windows
   venv\Scripts\activate
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env file with your settings
   ```

6. **Create PostgreSQL database**
   ```bash
   # Connect to PostgreSQL
   psql postgres
   
   # Create database and user
   CREATE DATABASE traveldb;
   CREATE USER traveluser WITH PASSWORD 'travelpass';
   GRANT ALL PRIVILEGES ON DATABASE traveldb TO traveluser;
   \q
   ```

7. **Run the backend**
   ```bash
   uvicorn app.main:app --reload
   ```

   Backend is now running at http://localhost:8000

### Frontend Setup

1. **Open a new terminal and navigate to frontend**
   ```bash
   cd travel-planner/frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Start development server**
   ```bash
   npm run dev
   ```

   Frontend is now running at http://localhost:5173

## Testing the Setup

1. Open http://localhost:5173 in your browser
2. You should see the Travel Planner homepage
3. The status should show "✅ Connected" if the backend is running

## Next Steps

1. **Review the Roadmap**
   - Check `docs/ROADMAP.md` for the development plan

2. **Explore the Code Structure**
   ```
   backend/
   ├── app/
   │   ├── api/        # API endpoints (add routes here)
   │   ├── models/     # Database models
   │   ├── schemas/    # Request/response schemas
   │   └── core/       # Configuration
   
   frontend/
   ├── src/
   │   ├── components/ # Reusable UI components
   │   ├── pages/      # Page components
   │   ├── services/   # API calls
   │   └── types/      # TypeScript types
   ```

3. **Start Building Features**
   - Add authentication endpoints
   - Create trip management features
   - Build the frontend UI

## Common Commands

### Backend
```bash
# Start server
uvicorn app.main:app --reload

# Create database migration
alembic revision --autogenerate -m "description"

# Run migrations
alembic upgrade head

# Run tests
pytest
```

### Frontend
```bash
# Start dev server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Lint code
npm run lint
```

### Docker
```bash
# Start all services
docker-compose up

# Start in background
docker-compose up -d

# Stop services
docker-compose down

# Rebuild containers
docker-compose up --build

# View logs
docker-compose logs -f
```

## Troubleshooting

### Backend won't start
- Check if PostgreSQL is running
- Verify DATABASE_URL in .env
- Make sure virtual environment is activated

### Frontend won't start
- Delete node_modules and run `npm install` again
- Check if port 5173 is available
- Verify Node.js version

### Database connection errors
- Check PostgreSQL is running: `pg_isready`
- Verify credentials in .env match database
- Try connecting manually: `psql -U traveluser -d traveldb`

### Docker issues
- Make sure Docker Desktop is running
- Try `docker-compose down` then `docker-compose up --build`
- Check Docker logs: `docker-compose logs`

## Need Help?

- Check the README.md for more information
- Review the code comments
- Backend API docs: http://localhost:8000/docs
