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

# Commit message linting
echo "📝 Commit messages - Running gitlint..."
cd ..
if command -v gitlint >/dev/null 2>&1; then
  if git rev-parse --verify --quiet origin/main >/dev/null; then
    gitlint --commits "origin/main..HEAD"
  else
    gitlint
  fi
  echo "✅ Commit message linting passed!"
else
  echo "⏭️  gitlint not installed, skipping (pip install gitlint==0.19.1)"
fi
echo ""

echo "🎉 All linting checks passed successfully!"
