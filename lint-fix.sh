#!/bin/bash
# Auto-fix lint errors for Travel Planner project
# Runs formatters and auto-fixers for both backend and frontend

set -e  # Exit on any error

echo "🔧 Auto-fixing lint errors for Travel Planner..."
echo ""

# Backend formatting
echo "📦 Backend (Python) - Running Black formatter..."
cd backend
python -m black . --line-length=100
echo "✅ Backend formatting complete!"
echo ""

# Frontend linting with auto-fix
echo "📦 Frontend (TypeScript/React) - Running ESLint with --fix..."
cd ../frontend
npm run lint -- --fix || echo "⚠️  Some frontend issues require manual intervention"
echo "✅ Frontend auto-fix complete!"
echo ""

echo "🎉 Auto-fix complete! Run ./lint.sh to verify all issues are resolved."
