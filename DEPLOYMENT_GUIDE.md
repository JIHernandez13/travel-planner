# Deployment Guide

Complete guide for deploying the Travel Planner application to production.

---

## Table of Contents

1. [Deployment Options](#deployment-options)
2. [Prerequisites](#prerequisites)
3. [Option 1: Vercel + Railway](#option-1-vercel--railway)
4. [Option 2: Full Render Deployment](#option-2-full-render-deployment)
5. [Option 3: Docker Deployment (Self-hosted)](#option-3-docker-deployment-self-hosted)
6. [Environment Variables](#environment-variables)
7. [Post-Deployment](#post-deployment)
8. [Troubleshooting](#troubleshooting)

---

## Deployment Options

| Platform | Frontend | Backend | Database | Cost | Difficulty |
|----------|----------|---------|----------|------|------------|
| **Vercel + Railway** | Vercel | Railway | Railway | $0-$25/mo | Easy ⭐⭐ |
| **Render** | Render | Render | Render | $0-$25/mo | Easy ⭐⭐ |
| **Docker (VPS)** | Nginx | Docker | Docker | $5-20/mo | Medium ⭐⭐⭐⭐ |

**Recommended for beginners**: Vercel + Railway (best developer experience)

---

## Prerequisites

### Required Accounts
- [ ] GitHub account (for code repository)
- [ ] Vercel account (sign up at https://vercel.com)
- [ ] Railway account (sign up at https://railway.app) OR Render account (https://render.com)

### Required Tools (Local Development)
- [ ] Git installed
- [ ] Node.js 18+ installed
- [ ] Python 3.11+ installed
- [ ] Docker and Docker Compose installed (optional, for local testing)

### Before You Deploy
1. Ensure your code is pushed to GitHub
2. All tests are passing (`npm run build` and `pytest`)
3. Environment variables are documented
4. Database schema is finalized (migrations ready)

---

## Option 1: Vercel + Railway

**Best for**: Quick deployment with excellent DX, free tier available

### Step 1: Deploy Backend to Railway

1. **Sign up for Railway**
   - Go to https://railway.app
   - Sign up with GitHub

2. **Create New Project**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your `travel-planner` repository
   - Railway will detect the backend automatically

3. **Add PostgreSQL Database**
   - In your Railway project, click "+ New"
   - Select "Database" → "PostgreSQL"
   - Railway will provision a database and set `DATABASE_URL`

4. **Configure Backend Service**
   - Select the backend service in Railway
   - Go to "Settings" → "Environment"
   - Add environment variables (see [Environment Variables](#environment-variables))
   - Set "Root Directory" to `backend`
   - Confirm "Start Command": `uvicorn main:app --host 0.0.0.0 --port $PORT`

5. **Deploy Backend**
   - Click "Deploy"
   - Wait for build to complete
   - Copy the backend URL (e.g., `https://travel-planner-backend.up.railway.app`)

6. **Verify Backend**
   - Visit `https://your-backend-url.railway.app/health`
   - Should return `{"status": "healthy"}`

### Step 2: Deploy Frontend to Vercel

1. **Sign up for Vercel**
   - Go to https://vercel.com
   - Sign up with GitHub

2. **Import Project**
   - Click "Add New..." → "Project"
   - Import your `travel-planner` repository
   - Vercel will auto-detect Vite

3. **Configure Frontend**
   - **Root Directory**: Set to `frontend`
   - **Framework Preset**: Vite
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`

4. **Add Environment Variable**
   - Under "Environment Variables", add:
     - `VITE_API_URL` = `https://your-backend-url.railway.app`

5. **Deploy Frontend**
   - Click "Deploy"
   - Wait for build to complete
   - Your app will be live at `https://your-app.vercel.app`

6. **Update CORS in Backend**
   - Go to Railway → Backend → Environment Variables
   - Add/Update `CORS_ORIGINS` = `https://your-app.vercel.app`
   - Redeploy backend

### Step 3: Connect Custom Domain (Optional)

**Vercel**:
- Go to Project Settings → Domains
- Add your domain (e.g., `travelplanner.com`)
- Follow DNS configuration instructions

**Railway**:
- Go to Service Settings → Networking
- Add custom domain
- Configure CNAME record

---

## Option 2: Full Render Deployment

**Best for**: All-in-one platform, automatic HTTPS, simple management

### Step 1: Create Render Account

1. Go to https://render.com
2. Sign up with GitHub
3. Connect your repository

### Step 2: Deploy Using Blueprint

1. **Create render.yaml** (already included in repo)
2. **Create New Blueprint**
   - Go to Render Dashboard
   - Click "New" → "Blueprint"
   - Select your `travel-planner` repository
   - Render will detect `render.yaml`

3. **Configure Environment Variables**
   - Render will auto-create services based on `render.yaml`
   - Database will auto-provision
   - Environment variables will auto-populate

4. **Manual Environment Variables**
   - Go to Backend Service → Environment
   - Add `SECRET_KEY` (generate with `openssl rand -hex 32`)
   - Update `VITE_API_URL` in Frontend to match backend URL

5. **Deploy**
   - Click "Create Blueprint"
   - Render will deploy all services
   - Wait 5-10 minutes for completion

### Step 3: Verify Deployment

1. **Backend**: Visit `https://travel-planner-api.onrender.com/health`
2. **Frontend**: Visit `https://travel-planner-frontend.onrender.com`
3. **Database**: Check connection in backend logs

**Note**: Free tier services sleep after 15 minutes of inactivity. First request may take 30-60 seconds.

---

## Option 3: Docker Deployment (Self-hosted)

**Best for**: Full control, self-hosted on VPS (DigitalOcean, AWS, etc.)

### Prerequisites
- VPS with Docker and Docker Compose installed
- Domain name pointing to your VPS
- Basic Linux command line knowledge

### Step 1: Server Setup

```bash
# SSH into your server
ssh user@your-server-ip

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install Docker Compose
sudo apt-get update
sudo apt-get install docker-compose-plugin

# Clone repository
git clone https://github.com/yourusername/travel-planner.git
cd travel-planner
```

### Step 2: Configure Environment

```bash
# Create .env file
cp .env.example .env

# Edit environment variables
nano .env
```

Required variables:
```env
# Database
POSTGRES_USER=traveluser
POSTGRES_PASSWORD=your_secure_password_here
POSTGRES_DB=travelplanner
DATABASE_URL=postgresql://traveluser:your_secure_password_here@db:5432/travelplanner

# Backend
SECRET_KEY=your_secret_key_here
ENVIRONMENT=production
DEBUG=false

# Frontend
VITE_API_URL=https://api.yourdomain.com
```

### Step 3: Deploy with Docker Compose

```bash
# Build and start services
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Step 4: Set Up Nginx Reverse Proxy (Production)

```bash
# Install Nginx
sudo apt-get install nginx

# Create Nginx config
sudo nano /etc/nginx/sites-available/travel-planner
```

Add configuration:
```nginx
# Frontend
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://localhost:5173;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}

# Backend API
server {
    listen 80;
    server_name api.yourdomain.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $host;
    }
}
```

Enable site and restart Nginx:
```bash
sudo ln -s /etc/nginx/sites-available/travel-planner /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### Step 5: Set Up SSL with Let's Encrypt

```bash
# Install Certbot
sudo apt-get install certbot python3-certbot-nginx

# Obtain SSL certificates
sudo certbot --nginx -d yourdomain.com -d api.yourdomain.com

# Auto-renewal is configured automatically
```

---

## Environment Variables

### Backend Environment Variables

| Variable | Description | Example | Required |
|----------|-------------|---------|----------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://user:pass@host:5432/db` | Yes |
| `SECRET_KEY` | JWT secret key | `openssl rand -hex 32` | Yes |
| `ENVIRONMENT` | Environment name | `production` | Yes |
| `DEBUG` | Debug mode | `false` | Yes |
| `ALGORITHM` | JWT algorithm | `HS256` | Yes |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token expiry | `60` | Yes |
| `REFRESH_TOKEN_EXPIRE_DAYS` | Refresh token expiry | `7` | Yes |
| `CORS_ORIGINS` | Allowed origins | `https://yourapp.com` | Yes |

### Frontend Environment Variables

| Variable | Description | Example | Required |
|----------|-------------|---------|----------|
| `VITE_API_URL` | Backend API URL | `https://api.yourapp.com` | Yes |

### Generating Secret Key

```bash
# Python
python -c "import secrets; print(secrets.token_hex(32))"

# OpenSSL
openssl rand -hex 32

# Node.js
node -e "console.log(require('crypto').randomBytes(32).toString('hex'))"
```

---

## Post-Deployment

### 1. Verify Health Checks

```bash
# Backend health
curl https://your-backend-url.com/health

# Expected: {"status": "healthy"}

# Frontend health
curl https://your-frontend-url.com/health

# Expected: healthy
```

### 2. Run Database Migrations

```bash
# Railway/Render (via CLI or web terminal)
alembic upgrade head

# Docker
docker-compose exec backend alembic upgrade head
```

### 3. Create Admin User (if applicable)

```bash
# When auth is implemented
curl -X POST https://your-api.com/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@example.com","password":"secure_password"}'
```

### 4. Set Up Monitoring

**Sentry (Error Tracking)**:
1. Sign up at https://sentry.io
2. Create new project
3. Add DSN to environment variables
4. Deploy with `SENTRY_DSN` set

**Uptime Monitoring**:
- UptimeRobot: https://uptimerobot.com (free)
- Pingdom: https://pingdom.com
- Healthchecks.io: https://healthchecks.io

### 5. Configure Backups

**Railway**:
- Automatic daily backups included
- Manual backup: Project Settings → Database → Backup

**Render**:
- Automatic backups on paid plans
- Snapshot before major changes

**Docker/Self-hosted**:
```bash
# Backup database
docker-compose exec db pg_dump -U traveluser travelplanner > backup.sql

# Restore database
docker-compose exec -T db psql -U traveluser travelplanner < backup.sql
```

---

## Troubleshooting

### Frontend Can't Connect to Backend

**Symptom**: CORS errors, network errors in browser console

**Solutions**:
1. Verify `VITE_API_URL` is correct
2. Check backend `CORS_ORIGINS` includes frontend URL
3. Ensure backend is running: `curl https://backend-url/health`
4. Check browser developer console for exact error

### Database Connection Failed

**Symptom**: Backend won't start, `could not connect to server` errors

**Solutions**:
1. Verify `DATABASE_URL` is correct
2. Check database service is running
3. Ensure database accepts connections from backend
4. Check network/firewall rules

### Build Failures

**Frontend Build Error**:
```bash
# Clear cache and rebuild
rm -rf node_modules dist
npm install
npm run build
```

**Backend Build Error**:
```bash
# Verify requirements.txt
pip install -r requirements.txt

# Check Python version
python --version  # Should be 3.11+
```

### Slow Cold Starts (Free Tier)

**Symptom**: First request takes 30-60 seconds

**Cause**: Free tier services sleep after inactivity

**Solutions**:
1. Upgrade to paid tier (always-on)
2. Use uptime monitor to ping every 5 minutes
3. Accept the limitation for POC/testing

### SSL Certificate Issues

**Symptom**: `NET::ERR_CERT_AUTHORITY_INVALID`

**Solutions**:
1. Ensure domain DNS is properly configured
2. Wait for SSL provisioning (can take 5-10 minutes)
3. Check platform SSL settings
4. Verify HTTPS enforcement is enabled

### Environment Variables Not Loading

**Solutions**:
1. Check variable names match exactly (case-sensitive)
2. Restart service after adding variables
3. Verify variables are in correct service
4. Check for typos in variable values

---

## Deployment Checklist

### Pre-Deployment
- [ ] All tests passing locally
- [ ] Frontend builds successfully (`npm run build`)
- [ ] Backend starts without errors
- [ ] Database migrations ready
- [ ] Environment variables documented
- [ ] Secrets generated (SECRET_KEY, etc.)
- [ ] CORS origins configured

### Deployment
- [ ] Database provisioned
- [ ] Backend deployed and accessible
- [ ] Frontend deployed and accessible
- [ ] Environment variables set correctly
- [ ] Health checks passing
- [ ] Custom domain configured (if applicable)
- [ ] SSL certificate active

### Post-Deployment
- [ ] Run database migrations
- [ ] Test user registration (when implemented)
- [ ] Test API endpoints
- [ ] Check error tracking setup
- [ ] Configure monitoring/alerts
- [ ] Set up automated backups
- [ ] Document deployment process
- [ ] Create rollback plan

---

## Rollback Procedure

### Railway
1. Go to Service → Deployments
2. Find previous working deployment
3. Click "Redeploy"

### Render
1. Go to Service → Events
2. Find previous deployment
3. Click "Rollback to this deployment"

### Vercel
1. Go to Project → Deployments
2. Find previous deployment
3. Click "⋮" → "Promote to Production"

### Docker
```bash
# Restore from backup
docker-compose down
docker-compose exec -T db psql -U traveluser travelplanner < backup.sql
git checkout previous-commit
docker-compose up -d
```

---

## Support Resources

- **Railway Docs**: https://docs.railway.app
- **Vercel Docs**: https://vercel.com/docs
- **Render Docs**: https://render.com/docs
- **FastAPI Docs**: https://fastapi.tiangolo.com
- **Vite Docs**: https://vitejs.dev

---

## Next Steps

After successful deployment:

1. **Implement Authentication**: Follow PRODUCTION_READINESS.md Phase 1A
2. **Add Monitoring**: Set up Sentry and uptime monitoring
3. **Create Staging Environment**: Duplicate setup for testing
4. **Set Up CI/CD**: Automate deployments with GitHub Actions (see `.github/workflows/`)
5. **Plan Feature Development**: Follow roadmap in ROADMAP.md

---

**Need Help?** Open an issue on GitHub or contact the development team.
