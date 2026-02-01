#!/bin/bash
# Lint script for Travel Planner project
# Runs both backend (Python) and frontend (TypeScript/React) linters

set -e  # Exit on any error

echo "🔍 Running linters for Travel Planner..."
echo ""

# Backend linting
echo "📦 Backend (Python) - Running flake8..."
cd backend
python -m flake8 . --count --max-line-length=100 --show-source --statistics
echo "✅ Backend linting passed!"
echo ""

# Frontend linting
echo "📦 Frontend (TypeScript/React) - Running ESLint..."
cd ../frontend
npm run lint
echo "✅ Frontend linting passed!"
echo ""

echo "🎉 All linting checks passed successfully!"
