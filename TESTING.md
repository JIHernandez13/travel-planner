# Testing Guide

This document provides comprehensive information about running tests and generating coverage reports for the Travel Planner application.

## Overview

The Travel Planner application includes comprehensive unit testing and coverage reporting for both backend (Python/FastAPI) and frontend (React/TypeScript) components.

### Test Coverage Goals

- **Backend**: 80% coverage minimum
- **Frontend**: 80% coverage minimum

## Backend Testing (Python/FastAPI)

### Test Framework

- **pytest**: Main testing framework
- **pytest-asyncio**: For async test support
- **pytest-cov**: For coverage reporting
- **httpx**: For testing FastAPI endpoints

### Running Backend Tests

```bash
cd backend

# Install dependencies (if not already installed)
pip install -r requirements.txt

# Run all tests
pytest

# Run tests with verbose output
pytest -v

# Run tests with coverage report
pytest --cov

# Run specific test file
pytest tests/test_config.py

# Run specific test function
pytest tests/test_config.py::test_settings_default_values
```

### Backend Coverage Reports

```bash
# Generate HTML coverage report
pytest --cov --cov-report=html

# View HTML report (open in browser)
# The report will be in backend/htmlcov/index.html

# Generate terminal coverage report
pytest --cov --cov-report=term-missing

# Generate XML coverage report (for CI/CD)
pytest --cov --cov-report=xml
```

### Backend Test Structure

```
backend/
├── tests/
│   ├── __init__.py
│   ├── conftest.py          # Shared fixtures and configuration
│   ├── test_config.py       # Configuration tests
│   ├── test_database.py     # Database tests
│   ├── test_main.py         # API endpoint tests
│   └── test_user.py         # User model tests
├── pytest.ini               # Pytest configuration
└── .coveragerc             # Coverage configuration
```

### Backend Test Files

1. **test_config.py**: Tests for configuration settings and environment variables
2. **test_database.py**: Tests for database connection, session management, and transactions
3. **test_main.py**: Tests for FastAPI endpoints and middleware
4. **test_user.py**: Tests for User model CRUD operations and validation

## Frontend Testing (React/TypeScript)

### Test Framework

- **Vitest**: Fast unit test framework for Vite
- **@testing-library/react**: React component testing utilities
- **@testing-library/user-event**: User interaction simulation
- **jsdom**: DOM implementation for Node.js

### Running Frontend Tests

```bash
cd frontend

# Install dependencies (if not already installed)
npm install

# Run all tests
npm test

# Run tests in watch mode
npm test -- --watch

# Run tests with UI
npm run test:ui

# Run tests with coverage
npm run test:coverage

# Run specific test file
npm test -- src/test/api.test.ts
```

### Frontend Coverage Reports

```bash
# Generate coverage report
npm run test:coverage

# Coverage reports are generated in multiple formats:
# - Terminal output (text)
# - HTML report: frontend/coverage/index.html
# - JSON report: frontend/coverage/coverage.json
# - LCOV report: frontend/coverage/lcov.info (for CI/CD)
```

### Frontend Test Structure

```
frontend/
├── src/
│   └── test/
│       ├── setup.ts           # Test setup and configuration
│       ├── api.test.ts        # API module tests
│       ├── App.test.tsx       # App component tests
│       └── HomePage.test.tsx  # HomePage component tests
└── vite.config.ts            # Vitest configuration
```

### Frontend Test Files

1. **setup.ts**: Global test setup, mocks for localStorage and window.location
2. **api.test.ts**: Tests for API functions (authAPI, tripsAPI)
3. **App.test.tsx**: Tests for main App component and routing
4. **HomePage.test.tsx**: Tests for HomePage component and API status

## Continuous Integration

### GitHub Actions Example

```yaml
name: Tests

on: [push, pull_request]

jobs:
  backend-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - run: cd backend && pip install -r requirements.txt
      - run: cd backend && pytest --cov --cov-report=xml

  frontend-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '18'
      - run: cd frontend && npm install
      - run: cd frontend && npm run test:coverage
```

## Writing New Tests

### Backend Test Example

```python
# tests/test_example.py
import pytest

def test_example_function(db_session):
    """Test description"""
    # Arrange
    expected = "expected_value"

    # Act
    result = some_function()

    # Assert
    assert result == expected
```

### Frontend Test Example

```typescript
// src/test/example.test.tsx
import { describe, it, expect } from 'vitest'
import { render, screen } from '@testing-library/react'
import ExampleComponent from '../ExampleComponent'

describe('ExampleComponent', () => {
  it('should render correctly', () => {
    render(<ExampleComponent />)
    expect(screen.getByText(/example/i)).toBeInTheDocument()
  })
})
```

## Best Practices

### General

1. Write tests before fixing bugs (TDD approach)
2. Keep tests simple and focused on one thing
3. Use descriptive test names
4. Maintain at least 80% code coverage
5. Mock external dependencies

### Backend

1. Use fixtures for common test data
2. Test both success and error cases
3. Test database transactions and rollbacks
4. Use pytest markers for test categorization
5. Test async functions with pytest-asyncio

### Frontend

1. Test user interactions, not implementation details
2. Use Testing Library queries (getByRole, getByText)
3. Mock API calls and external dependencies
4. Test accessibility (ARIA roles, labels)
5. Use waitFor for async operations

## Coverage Reports Location

### Backend

- HTML: `backend/htmlcov/index.html`
- XML: `backend/coverage.xml`
- Terminal: Run `pytest --cov --cov-report=term-missing`

### Frontend

- HTML: `frontend/coverage/index.html`
- JSON: `frontend/coverage/coverage.json`
- LCOV: `frontend/coverage/lcov.info`

## Troubleshooting

### Backend Issues

**Problem**: Import errors in tests
- **Solution**: Ensure `sys.path` is configured correctly in `conftest.py`

**Problem**: Database errors
- **Solution**: Tests use in-memory SQLite, no external DB needed

**Problem**: Async test warnings
- **Solution**: Add `@pytest.mark.asyncio` decorator or set `asyncio_mode = auto` in pytest.ini

### Frontend Issues

**Problem**: Module not found errors
- **Solution**: Run `npm install` to ensure all dependencies are installed

**Problem**: Component tests failing
- **Solution**: Check that test setup file is configured in vite.config.ts

**Problem**: API mocking issues
- **Solution**: Ensure axios is properly mocked with `vi.mock('axios')`

## Additional Resources

- [pytest Documentation](https://docs.pytest.org/)
- [Vitest Documentation](https://vitest.dev/)
- [Testing Library Documentation](https://testing-library.com/)
- [FastAPI Testing Documentation](https://fastapi.tiangolo.com/tutorial/testing/)

## Running All Tests

To run both backend and frontend tests:

```bash
# From project root

# Backend tests
cd backend && pytest --cov && cd ..

# Frontend tests
cd frontend && npm run test:coverage && cd ..
```
