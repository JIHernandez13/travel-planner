# GitHub Secrets Setup Guide

This guide explains how to set up secrets for automated deployments via GitHub Actions.

---

## Required Secrets by Platform

### Option 1: Vercel + Railway

#### Vercel Secrets (Frontend)
| Secret Name | Description | How to Get |
|-------------|-------------|------------|
| `VERCEL_TOKEN` | Vercel authentication token | Account Settings → Tokens → Create |
| `VERCEL_ORG_ID` | Your Vercel organization ID | Project Settings → General |
| `VERCEL_PROJECT_ID` | Your Vercel project ID | Project Settings → General |
| `VITE_API_URL` | Backend API URL | Your Railway backend URL |

#### Railway Secrets (Backend)
| Secret Name | Description | How to Get |
|-------------|-------------|------------|
| `RAILWAY_TOKEN` | Railway API token | Account Settings → Tokens → Create |
| `BACKEND_URL` | Your backend URL | Railway backend service URL |

---

### Option 2: Render

#### Render Secrets
| Secret Name | Description | How to Get |
|-------------|-------------|------------|
| `RENDER_API_KEY` | Render API key | Account Settings → API Keys → Create |
| `RENDER_BACKEND_SERVICE_ID` | Backend service ID | Dashboard → Service → Settings |
| `RENDER_FRONTEND_SERVICE_ID` | Frontend service ID | Dashboard → Service → Settings |
| `RENDER_BACKEND_URL` | Backend URL | Service URL from Render dashboard |
| `RENDER_FRONTEND_URL` | Frontend URL | Service URL from Render dashboard |

---

## Step-by-Step Setup

### 1. Generate Secret Key for JWT

Run one of these commands locally:

```bash
# Option 1: Python
python -c "import secrets; print(secrets.token_hex(32))"

# Option 2: OpenSSL
openssl rand -hex 32

# Option 3: Node.js
node -e "console.log(require('crypto').randomBytes(32).toString('hex'))"
```

Copy the output - you'll need it for `SECRET_KEY`.

---

### 2. Set Up Vercel

#### Get Vercel Token
1. Go to https://vercel.com
2. Click your profile → Settings
3. Go to "Tokens"
4. Click "Create" → Name it "GitHub Actions"
5. Copy the token (**save it securely**)

#### Get Vercel Org ID and Project ID
1. Go to your project on Vercel
2. Click Settings → General
3. Scroll down to find:
   - **Project ID**: `prj_xxxxxxxxxxxxx`
   - **Organization ID**: `team_xxxxxxxxxxxxx`
4. Copy both IDs

#### Add to GitHub Secrets
1. Go to your GitHub repository
2. Settings → Secrets and variables → Actions
3. Click "New repository secret"
4. Add each secret:
   - Name: `VERCEL_TOKEN` → Value: (paste token)
   - Name: `VERCEL_ORG_ID` → Value: (paste org ID)
   - Name: `VERCEL_PROJECT_ID` → Value: (paste project ID)
   - Name: `VITE_API_URL` → Value: (your Railway backend URL)

---

### 3. Set Up Railway

#### Get Railway Token
1. Go to https://railway.app
2. Click your profile → Account Settings
3. Go to "Tokens"
4. Click "Create Token" → Name it "GitHub Actions"
5. Copy the token (**save it securely**)

#### Add to GitHub Secrets
1. Go to your GitHub repository
2. Settings → Secrets and variables → Actions
3. Click "New repository secret"
4. Add secrets:
   - Name: `RAILWAY_TOKEN` → Value: (paste token)
   - Name: `BACKEND_URL` → Value: `https://your-app.up.railway.app`

---

### 4. Set Up Render

#### Get Render API Key
1. Go to https://render.com
2. Click your profile → Account Settings
3. Go to "API Keys"
4. Click "Create API Key" → Name it "GitHub Actions"
5. Copy the key (**save it securely**)

#### Get Service IDs
1. Go to Render Dashboard
2. Click on your Backend service
3. Go to Settings → General
4. Copy the Service ID (e.g., `srv-xxxxxxxxxxxxx`)
5. Repeat for Frontend service

#### Add to GitHub Secrets
1. Go to your GitHub repository
2. Settings → Secrets and variables → Actions
3. Add secrets:
   - Name: `RENDER_API_KEY` → Value: (paste API key)
   - Name: `RENDER_BACKEND_SERVICE_ID` → Value: (backend service ID)
   - Name: `RENDER_FRONTEND_SERVICE_ID` → Value: (frontend service ID)
   - Name: `RENDER_BACKEND_URL` → Value: `https://your-backend.onrender.com`
   - Name: `RENDER_FRONTEND_URL` → Value: `https://your-frontend.onrender.com`

---

## Environment Variables for Each Platform

### Railway Environment Variables

Add these in Railway Dashboard → Service → Variables:

```env
# Backend Service
DATABASE_URL=<auto-populated from database>
SECRET_KEY=<your-generated-secret-key>
ENVIRONMENT=production
DEBUG=false
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
REFRESH_TOKEN_EXPIRE_DAYS=7
CORS_ORIGINS=https://your-vercel-app.vercel.app
PORT=8000
```

### Vercel Environment Variables

Add these in Vercel Dashboard → Project → Settings → Environment Variables:

```env
# Frontend
VITE_API_URL=https://your-backend.up.railway.app
```

### Render Environment Variables

These are auto-populated from `render.yaml`, but you may need to add:

```env
# Backend Service
SECRET_KEY=<your-generated-secret-key>

# Frontend Service (if not in render.yaml)
VITE_API_URL=https://your-backend.onrender.com
```

---

## Testing Your Secrets

### Test Locally First

```bash
# Test backend locally
cd backend
export SECRET_KEY="your-test-key"
export DATABASE_URL="postgresql://localhost/testdb"
python -c "from config import settings; print('Config loaded:', settings.SECRET_KEY[:10] + '...')"

# Test frontend locally
cd frontend
export VITE_API_URL="http://localhost:8000"
npm run build
```

### Test GitHub Actions

1. Push a small change to trigger workflow
2. Go to Actions tab in GitHub
3. Watch the workflow run
4. Check for any secret-related errors

---

## Security Best Practices

### ✅ DO
- Rotate tokens every 6 months
- Use different tokens for staging and production
- Store tokens in password manager
- Use environment-specific secrets
- Enable 2FA on all platform accounts

### ❌ DON'T
- Commit secrets to Git
- Share tokens in Slack/Discord
- Use the same token across multiple projects
- Screenshot tokens
- Store tokens in plain text files

---

## Troubleshooting

### "Invalid token" errors

**Solution**:
1. Verify token is copied correctly (no extra spaces)
2. Check token hasn't expired
3. Regenerate token if needed
4. Update GitHub secret with new token

### Deployment succeeds but app doesn't work

**Solution**:
1. Check environment variables are set correctly
2. Verify `VITE_API_URL` matches backend URL exactly
3. Check CORS origins include frontend URL
4. Look at deployment logs for errors

### "Secret not found" in GitHub Actions

**Solution**:
1. Verify secret name matches exactly (case-sensitive)
2. Check secret is in correct repository
3. Wait a few minutes after adding secret (can take time to propagate)
4. Re-run workflow

---

## Secrets Checklist

Before deploying, ensure you have:

### For Vercel + Railway:
- [ ] `VERCEL_TOKEN` added to GitHub
- [ ] `VERCEL_ORG_ID` added to GitHub
- [ ] `VERCEL_PROJECT_ID` added to GitHub
- [ ] `RAILWAY_TOKEN` added to GitHub
- [ ] `VITE_API_URL` added to Vercel
- [ ] `SECRET_KEY` added to Railway
- [ ] `CORS_ORIGINS` added to Railway
- [ ] Backend `DATABASE_URL` configured

### For Render:
- [ ] `RENDER_API_KEY` added to GitHub
- [ ] `RENDER_BACKEND_SERVICE_ID` added to GitHub
- [ ] `RENDER_FRONTEND_SERVICE_ID` added to GitHub
- [ ] `SECRET_KEY` added to Render backend
- [ ] All environment variables in `render.yaml` verified

---

## Quick Reference Commands

### Generate JWT Secret
```bash
openssl rand -hex 32
```

### View GitHub Secrets (you can't - they're hidden)
```bash
# You can only add/update, not view
# Keep your secrets in a password manager
```

### Test Railway Connection
```bash
# Install Railway CLI
npm i -g @railway/cli

# Login
railway login

# Link project
railway link

# Test environment variables
railway run env
```

### Test Vercel Connection
```bash
# Install Vercel CLI
npm i -g vercel

# Login
vercel login

# Pull environment variables
vercel env pull
```

---

**Need Help?**
- Railway: https://docs.railway.app
- Vercel: https://vercel.com/docs/security
- Render: https://render.com/docs/environment-variables
