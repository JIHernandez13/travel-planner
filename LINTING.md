# Code Quality and Linting Guide

## Overview

This project uses automated linting and formatting tools to maintain consistent code quality across the backend (Python) and frontend (TypeScript/React).

## Linting Tools

### Backend (Python)
- **flake8**: Checks Python code for style guide enforcement (PEP 8)
- **black**: Opinionated code formatter that automatically formats Python code

Configuration files:
- `backend/.flake8` - Flake8 configuration
- `backend/pyproject.toml` - Black configuration

### Frontend (TypeScript/React)
- **ESLint**: Identifies and reports patterns in JavaScript/TypeScript code

Configuration files:
- `frontend/eslint.config.js` - ESLint configuration
- `frontend/package.json` - Contains lint script

### Commit messages
- **gitlint**: Checks git commit messages for style consistency (title length,
  imperative-friendly length limits, trailing punctuation, no `WIP`/`TODO`/`FIXME`
  in the title, body wrapping)

Configuration file:
- `.gitlint` - gitlint rules (repo root)

## Usage

### Quick Commands

Run from the project root directory:

```bash
# Check all code for lint errors
./lint.sh

# Auto-fix lint errors where possible
./lint-fix.sh
```

### Manual Commands

**Backend:**
```bash
cd backend

# Check for lint errors
python -m flake8 . --max-line-length=100

# Auto-format code with Black
python -m black . --line-length=100
```

**Frontend:**
```bash
cd frontend

# Check for lint errors
npm run lint

# Auto-fix lint errors
npm run lint -- --fix
```

**Commit messages:**
```bash
# Install (bundled in backend/requirements.txt)
pip install gitlint==0.19.1

# Lint the most recent commit
gitlint

# Lint every commit on the current branch
gitlint --commits origin/main..HEAD

# Lint a message before committing
git log -1 --format=%B | gitlint

# Optional: install a local commit-msg hook so bad messages are rejected
gitlint install-hook
```

## What Gets Checked

### Backend (flake8)
- PEP 8 style compliance
- Line length (max 100 characters)
- Unused imports
- Whitespace issues
- Import ordering
- Code complexity

### Frontend (ESLint)
- TypeScript type safety
- React best practices
- Hook usage rules
- Import/export standards
- Unused variables
- Code complexity

### Commit messages (gitlint)
- Title length (max 72 chars) and minimum length (8 chars)
- No trailing punctuation or whitespace in the title
- No `WIP` / `TODO` / `FIXME` in the title
- Blank line between title and body
- Body lines wrapped at 100 chars
- Valid author email
- Merge / revert / fixup / squash commits are ignored

## What Gets Auto-Fixed

### Backend (black)
- Line length normalization
- Indentation and spacing
- String quote consistency
- Import ordering
- Expression formatting

### Frontend (ESLint --fix)
- Simple formatting issues
- Semicolon usage
- Quote consistency
- Spacing issues
- Some import ordering

**Note:** Not all lint errors can be auto-fixed. Some require manual intervention, such as:
- Unused variables/imports (must decide if they should be removed or used)
- Type errors (requires proper typing)
- Logic issues (requires code refactoring)

## CI/CD Integration

To add linting to your CI/CD pipeline:

```yaml
# Example for GitHub Actions
- name: Lint Backend
  run: cd backend && python -m flake8 . --max-line-length=100

- name: Lint Frontend
  run: cd frontend && npm run lint

- name: Lint Commit Messages
  run: pip install gitlint==0.19.1 && gitlint --commits origin/main..HEAD
```

The `Build` workflow (`.github/workflows/build.yml`) runs gitlint on every pull
request via the `lint-commits` job, checking all commits between the PR base and
head.

## Best Practices

1. **Run linters before committing**: Catch issues early
2. **Use auto-fix first**: Let tools handle simple formatting
3. **Review auto-fix changes**: Ensure auto-fixes don't break logic
4. **Fix lint errors incrementally**: Don't accumulate technical debt
5. **Configure your IDE**: Many editors can run linters on save

## IDE Integration

### VS Code
- Install extensions:
  - **Python**: Microsoft Python extension (includes flake8)
  - **Black Formatter**: ms-python.black-formatter
  - **ESLint**: dbaeumer.vscode-eslint

### Settings
Add to `.vscode/settings.json`:
```json
{
  "python.linting.flake8Enabled": true,
  "python.formatting.provider": "black",
  "editor.formatOnSave": true,
  "eslint.validate": ["javascript", "javascriptreact", "typescript", "typescriptreact"]
}
```

## Troubleshooting

### Backend Issues

**Problem:** `flake8: command not found`
```bash
cd backend
pip install flake8 black
```

**Problem:** Conflicting flake8 and black rules
- The `.flake8` config already ignores W503 which conflicts with black

### Frontend Issues

**Problem:** `eslint: command not found`
```bash
cd frontend
npm install
```

**Problem:** Some files still have lint errors after auto-fix
- Review the errors manually and fix them
- Some issues like TypeScript type errors require code changes

## Common Lint Errors and Fixes

### Backend

| Error | Description | Fix |
|-------|-------------|-----|
| F401 | Imported but unused | Remove import or use it |
| E501 | Line too long | Break into multiple lines or use black |
| W293 | Blank line with whitespace | Remove whitespace or run black |
| E402 | Module level import not at top | Move imports or add `# noqa: E402` |

### Frontend

| Error | Description | Fix |
|-------|-------------|-----|
| @typescript-eslint/no-explicit-any | Using `any` type | Replace with specific type |
| react-hooks/exhaustive-deps | Missing dependency in hook | Add to dependency array |
| @typescript-eslint/no-unused-vars | Unused variable | Remove or use it |

## Summary of Fixed Issues

The initial linting run found and fixed:
- **Backend**: 33 issues
  - 14 unused imports
  - 14 whitespace issues
  - 4 import ordering issues
  - 1 line length issue
- **Frontend**: 1 issue
  - 1 TypeScript `any` type usage

All issues have been resolved, and the codebase now passes all linting checks.
