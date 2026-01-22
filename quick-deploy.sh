#!/bin/bash
# Quick Deployment Script for Travel Planner
# This script helps you deploy quickly to various platforms

set -e  # Exit on error

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}╔════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║   Travel Planner - Quick Deployment Tool  ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════╝${NC}"
echo ""

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to generate secret key
generate_secret() {
    if command_exists openssl; then
        openssl rand -hex 32
    elif command_exists python3; then
        python3 -c "import secrets; print(secrets.token_hex(32))"
    else
        echo -e "${RED}Error: Cannot generate secret key. Install openssl or python3${NC}"
        exit 1
    fi
}

# Check prerequisites
echo -e "${YELLOW}Checking prerequisites...${NC}"

if ! command_exists git; then
    echo -e "${RED}Error: git is not installed${NC}"
    exit 1
fi

if ! command_exists node; then
    echo -e "${RED}Error: Node.js is not installed${NC}"
    exit 1
fi

if ! command_exists python3; then
    echo -e "${RED}Error: Python 3 is not installed${NC}"
    exit 1
fi

echo -e "${GREEN}✓ All prerequisites met${NC}"
echo ""

# Ask deployment platform
echo -e "${YELLOW}Select deployment platform:${NC}"
echo "1) Vercel (Frontend) + Railway (Backend)"
echo "2) Render (Full Stack)"
echo "3) Docker (Local/Self-hosted)"
echo "4) Test Build Only (No Deployment)"
read -p "Enter choice [1-4]: " platform_choice

case $platform_choice in
    1)
        PLATFORM="vercel-railway"
        ;;
    2)
        PLATFORM="render"
        ;;
    3)
        PLATFORM="docker"
        ;;
    4)
        PLATFORM="test"
        ;;
    *)
        echo -e "${RED}Invalid choice${NC}"
        exit 1
        ;;
esac

echo ""
echo -e "${BLUE}═══════════════════════════════════════════${NC}"
echo -e "${BLUE}  Step 1: Testing Local Build${NC}"
echo -e "${BLUE}═══════════════════════════════════════════${NC}"

# Test frontend build
echo -e "${YELLOW}Building frontend...${NC}"
cd frontend
npm install
npm run lint
npm run build
echo -e "${GREEN}✓ Frontend build successful${NC}"
cd ..

# Test backend
echo -e "${YELLOW}Testing backend...${NC}"
cd backend
pip install -r requirements.txt > /dev/null 2>&1
python3 -m py_compile main.py
echo -e "${GREEN}✓ Backend syntax check passed${NC}"
cd ..

echo ""

if [ "$PLATFORM" = "test" ]; then
    echo -e "${GREEN}✓ Build test completed successfully!${NC}"
    exit 0
fi

# Generate secrets if needed
if [ ! -f .env ]; then
    echo -e "${YELLOW}No .env file found. Creating from template...${NC}"
    cp .env.example .env
    SECRET_KEY=$(generate_secret)
    sed -i "s/your_secret_key_here/$SECRET_KEY/g" .env
    echo -e "${GREEN}✓ .env file created${NC}"
    echo -e "${YELLOW}⚠ Please edit .env file with your database credentials${NC}"
fi

echo ""
echo -e "${BLUE}═══════════════════════════════════════════${NC}"
echo -e "${BLUE}  Step 2: Platform-Specific Deployment${NC}"
echo -e "${BLUE}═══════════════════════════════════════════${NC}"

case $PLATFORM in
    "vercel-railway")
        echo -e "${YELLOW}Setting up Vercel + Railway deployment...${NC}"

        # Check if Railway CLI is installed
        if ! command_exists railway; then
            echo -e "${YELLOW}Installing Railway CLI...${NC}"
            npm install -g @railway/cli
        fi

        # Check if Vercel CLI is installed
        if ! command_exists vercel; then
            echo -e "${YELLOW}Installing Vercel CLI...${NC}"
            npm install -g vercel
        fi

        echo ""
        echo -e "${GREEN}Next steps:${NC}"
        echo "1. Deploy backend to Railway:"
        echo -e "   ${BLUE}cd backend && railway login && railway init && railway up${NC}"
        echo ""
        echo "2. Copy Railway backend URL and update frontend env:"
        echo -e "   ${BLUE}export VITE_API_URL=https://your-backend.railway.app${NC}"
        echo ""
        echo "3. Deploy frontend to Vercel:"
        echo -e "   ${BLUE}cd frontend && vercel --prod${NC}"
        echo ""
        ;;

    "render")
        echo -e "${YELLOW}Setting up Render deployment...${NC}"

        if [ ! -f render.yaml ]; then
            echo -e "${RED}Error: render.yaml not found${NC}"
            exit 1
        fi

        echo ""
        echo -e "${GREEN}Next steps:${NC}"
        echo "1. Go to https://render.com"
        echo "2. Create New → Blueprint"
        echo "3. Connect your GitHub repository"
        echo "4. Render will auto-deploy from render.yaml"
        echo ""
        echo -e "${YELLOW}Make sure to set SECRET_KEY in Render dashboard${NC}"
        SECRET_KEY=$(generate_secret)
        echo -e "${GREEN}Generated SECRET_KEY:${NC} $SECRET_KEY"
        echo ""
        ;;

    "docker")
        echo -e "${YELLOW}Setting up Docker deployment...${NC}"

        if ! command_exists docker; then
            echo -e "${RED}Error: Docker is not installed${NC}"
            exit 1
        fi

        if ! command_exists docker-compose; then
            echo -e "${RED}Error: Docker Compose is not installed${NC}"
            exit 1
        fi

        echo -e "${YELLOW}Starting services with Docker Compose...${NC}"
        docker-compose up -d

        echo ""
        echo -e "${GREEN}✓ Services started!${NC}"
        echo ""
        echo "Frontend: http://localhost:5173"
        echo "Backend:  http://localhost:8000"
        echo "Backend Docs: http://localhost:8000/docs"
        echo ""
        echo "View logs: docker-compose logs -f"
        echo "Stop services: docker-compose down"
        ;;
esac

echo ""
echo -e "${GREEN}═══════════════════════════════════════════${NC}"
echo -e "${GREEN}  Deployment preparation complete!${NC}"
echo -e "${GREEN}═══════════════════════════════════════════${NC}"
echo ""
echo -e "${YELLOW}📖 For detailed deployment instructions, see:${NC}"
echo "   - DEPLOYMENT_GUIDE.md"
echo "   - PRODUCTION_READINESS.md"
echo "   - SECRETS_SETUP.md"
echo ""
