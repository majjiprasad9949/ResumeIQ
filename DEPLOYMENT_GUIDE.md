# Deployment Guide - ResumeIQ MVP

This guide covers deploying the ResumeIQ MVP to production using:
- **Frontend**: Vercel
- **Backend**: Render or Railway
- **Database**: PostgreSQL (managed)

---

## Prerequisites

- GitHub account with repository access
- Vercel account (free tier available)
- Render or Railway account (free tier available)
- PostgreSQL database (managed service)
- Domain name (optional, can use provided subdomains)

---

## Part 1: Frontend Deployment (Vercel)

### Step 1: Prepare Frontend for Deployment

1. **Create `vercel.json` in frontend root**:
```json
{
  "buildCommand": "npm run build",
  "outputDirectory": "dist",
  "env": {
    "VITE_API_URL": "@vite_api_url"
  },
  "rewrites": [
    {
      "source": "/(.*)",
      "destination": "/index.html"
    }
  ]
}
```

2. **Create `.env.production` in frontend root**:
```
VITE_API_URL=https://your-backend-url.com
```

3. **Update `vite.config.js`**:
```javascript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  build: {
    outDir: 'dist',
    sourcemap: false,
  }
})
```

### Step 2: Deploy to Vercel

1. **Push code to GitHub**:
```bash
git add .
git commit -m "Prepare frontend for deployment"
git push origin main
```

2. **Connect to Vercel**:
   - Go to https://vercel.com
   - Click "New Project"
   - Select your GitHub repository
   - Click "Import"

3. **Configure Environment Variables**:
   - In Vercel dashboard, go to Settings → Environment Variables
   - Add `VITE_API_URL` with your backend URL
   - Click "Save"

4. **Deploy**:
   - Click "Deploy"
   - Wait for deployment to complete
   - Your frontend is now live at `https://your-project.vercel.app`

### Step 3: Configure Custom Domain (Optional)

1. In Vercel dashboard, go to Settings → Domains
2. Add your custom domain
3. Update DNS records as instructed
4. Wait for DNS propagation (up to 48 hours)

---

## Part 2: Backend Deployment (Render)

### Step 1: Prepare Backend for Deployment

1. **Create `render.yaml` in backend root**:
```yaml
services:
  - type: web
    name: ai-resume-optimizer-api
    env: python
    plan: free
    buildCommand: pip install -r requirements.txt && python manage.py migrate
    startCommand: gunicorn config.wsgi:application
    envVars:
      - key: DEBUG
        value: false
      - key: PYTHON_VERSION
        value: 3.11
      - key: DATABASE_URL
        fromDatabase:
          name: postgres
          property: connectionString
      - key: SECRET_KEY
        generateValue: true
      - key: ALLOWED_HOSTS
        value: your-backend-url.com
      - key: CORS_ALLOWED_ORIGINS
        value: https://your-frontend-url.com

databases:
  - name: postgres
    plan: free
```

2. **Update `requirements.txt`**:
```
Django==4.2.0
djangorestframework==3.14.0
django-cors-headers==4.0.0
psycopg2-binary==2.9.6
python-decouple==3.8
PyJWT==2.8.0
gunicorn==20.1.0
spacy==3.5.0
sentence-transformers==2.2.2
```

3. **Update `backend/config/settings.py`**:
```python
import os
from decouple import config

# Production settings
DEBUG = config('DEBUG', default=False, cast=bool)
SECRET_KEY = config('SECRET_KEY')
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost').split(',')

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DATABASE_NAME', default='postgres'),
        'USER': config('DATABASE_USER', default='postgres'),
        'PASSWORD': config('DATABASE_PASSWORD', default=''),
        'HOST': config('DATABASE_HOST', default='localhost'),
        'PORT': config('DATABASE_PORT', default='5432'),
    }
}

# CORS
CORS_ALLOWED_ORIGINS = config('CORS_ALLOWED_ORIGINS', default='http://localhost:3000').split(',')

# JWT
JWT_SECRET = config('JWT_SECRET', default=SECRET_KEY)
```

4. **Create `Procfile` in backend root**:
```
web: gunicorn config.wsgi:application
```

### Step 2: Deploy to Render

1. **Push code to GitHub**:
```bash
git add .
git commit -m "Prepare backend for deployment"
git push origin main
```

2. **Connect to Render**:
   - Go to https://render.com
   - Click "New +"
   - Select "Web Service"
   - Connect your GitHub repository
   - Select the backend directory

3. **Configure Settings**:
   - **Name**: `ai-resume-optimizer-api`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt && python manage.py migrate`
   - **Start Command**: `gunicorn config.wsgi:application`

4. **Add Environment Variables**:
   - Click "Advanced"
   - Add environment variables:
     - `DEBUG`: `false`
     - `SECRET_KEY`: Generate a secure key
     - `ALLOWED_HOSTS`: Your backend domain
     - `CORS_ALLOWED_ORIGINS`: Your frontend URL
     - `DATABASE_URL`: From PostgreSQL service

5. **Create PostgreSQL Database**:
   - In Render dashboard, click "New +"
   - Select "PostgreSQL"
   - Configure database
   - Copy connection string to `DATABASE_URL`

6. **Deploy**:
   - Click "Create Web Service"
   - Wait for deployment to complete
   - Your backend is now live at `https://your-backend-url.onrender.com`

---

## Part 3: Backend Deployment (Railway Alternative)

### Step 1: Prepare Backend for Railway

1. **Create `railway.json` in backend root**:
```json
{
  "build": {
    "builder": "dockerfile"
  },
  "deploy": {
    "startCommand": "gunicorn config.wsgi:application"
  }
}
```

2. **Create `Dockerfile` in backend root**:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
```

### Step 2: Deploy to Railway

1. **Push code to GitHub**:
```bash
git add .
git commit -m "Prepare backend for Railway deployment"
git push origin main
```

2. **Connect to Railway**:
   - Go to https://railway.app
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Select your repository

3. **Configure Environment Variables**:
   - In Railway dashboard, go to Variables
   - Add all required environment variables
   - Add PostgreSQL plugin

4. **Deploy**:
   - Railway automatically deploys on push
   - Your backend is now live at the provided Railway URL

---

## Part 4: Database Setup

### PostgreSQL on Render

1. **Create Database**:
   - In Render dashboard, click "New +"
   - Select "PostgreSQL"
   - Configure:
     - **Name**: `ai-resume-optimizer-db`
     - **Database**: `postgres`
     - **User**: `postgres`
     - **Region**: Same as backend
   - Click "Create Database"

2. **Get Connection String**:
   - Copy the connection string
   - Add to backend environment variables as `DATABASE_URL`

3. **Run Migrations**:
```bash
# After deployment
python manage.py migrate
```

### PostgreSQL on Railway

1. **Add PostgreSQL Plugin**:
   - In Railway project, click "Add"
   - Select "PostgreSQL"
   - Railway automatically configures connection

2. **Run Migrations**:
```bash
# After deployment
python manage.py migrate
```

---

## Part 5: Environment Variables Summary

### Frontend (Vercel)
```
VITE_API_URL=https://your-backend-url.com
```

### Backend (Render/Railway)
```
DEBUG=false
SECRET_KEY=<generate-secure-key>
ALLOWED_HOSTS=your-backend-url.com
CORS_ALLOWED_ORIGINS=https://your-frontend-url.com
DATABASE_URL=postgresql://user:password@host:port/database
JWT_SECRET=<generate-secure-key>
```

---

## Part 6: Post-Deployment Verification

### Frontend Verification

1. **Check Frontend URL**:
   - Visit `https://your-frontend-url.com`
   - Should load login page

2. **Test API Connection**:
   - Open browser console
   - Check for CORS errors
   - Verify API calls are reaching backend

### Backend Verification

1. **Check Backend Health**:
   - Visit `https://your-backend-url.com/api/health` (if endpoint exists)
   - Should return 200 OK

2. **Check Database Connection**:
   - Backend should connect to PostgreSQL
   - Migrations should be applied

3. **Test API Endpoints**:
```bash
# Test registration
curl -X POST https://your-backend-url.com/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"test123","full_name":"Test User"}'

# Test login
curl -X POST https://your-backend-url.com/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"test123"}'
```

---

## Part 7: Monitoring and Maintenance

### Vercel Monitoring

1. **Check Deployment Status**:
   - Go to Vercel dashboard
   - View deployment history
   - Check build logs

2. **Monitor Performance**:
   - Use Vercel Analytics
   - Monitor Core Web Vitals
   - Check error rates

### Render/Railway Monitoring

1. **Check Service Status**:
   - Go to Render/Railway dashboard
   - View service logs
   - Check resource usage

2. **Monitor Database**:
   - Check database connections
   - Monitor disk usage
   - Review slow queries

### Logging

1. **Frontend Logs**:
   - Check browser console
   - Use Vercel Analytics

2. **Backend Logs**:
   - Check Render/Railway logs
   - Use Django logging
   - Monitor error rates

---

## Part 8: Troubleshooting

### Frontend Issues

**Issue**: CORS errors
- **Solution**: Update `CORS_ALLOWED_ORIGINS` in backend settings

**Issue**: API calls failing
- **Solution**: Check `VITE_API_URL` environment variable

**Issue**: Blank page
- **Solution**: Check browser console for errors, verify build succeeded

### Backend Issues

**Issue**: Database connection error
- **Solution**: Verify `DATABASE_URL` is correct, check PostgreSQL service

**Issue**: 500 errors
- **Solution**: Check backend logs, verify migrations ran successfully

**Issue**: CORS errors from frontend
- **Solution**: Update `CORS_ALLOWED_ORIGINS` to include frontend URL

### Database Issues

**Issue**: Migrations failed
- **Solution**: Check database connection, verify PostgreSQL is running

**Issue**: Connection pool exhausted
- **Solution**: Increase connection pool size in settings

---

## Part 9: Scaling and Optimization

### Frontend Optimization

1. **Enable Caching**:
   - Vercel automatically caches static assets
   - Configure cache headers in `vercel.json`

2. **Optimize Images**:
   - Use Next.js Image component (if using Next.js)
   - Compress images before upload

3. **Monitor Performance**:
   - Use Vercel Analytics
   - Monitor Core Web Vitals

### Backend Optimization

1. **Database Optimization**:
   - Add indexes on frequently queried fields
   - Use connection pooling
   - Monitor slow queries

2. **API Optimization**:
   - Implement pagination
   - Use caching headers
   - Optimize database queries

3. **Scaling**:
   - Upgrade Render/Railway plan if needed
   - Add more database connections
   - Consider CDN for static files

---

## Part 10: Security Checklist

- [ ] `DEBUG` is set to `false` in production
- [ ] `SECRET_KEY` is a strong, random string
- [ ] `ALLOWED_HOSTS` is configured correctly
- [ ] `CORS_ALLOWED_ORIGINS` is restricted to frontend URL
- [ ] HTTPS is enforced
- [ ] Database password is strong
- [ ] Environment variables are not committed to Git
- [ ] JWT tokens are signed with secure key
- [ ] CSRF protection is enabled
- [ ] SQL injection prevention is in place
- [ ] XSS protection is enabled
- [ ] Rate limiting is configured (optional)

---

## Deployment Checklist

- [ ] Frontend code is ready
- [ ] Backend code is ready
- [ ] Environment variables are configured
- [ ] Database is created and migrations are applied
- [ ] Frontend is deployed to Vercel
- [ ] Backend is deployed to Render/Railway
- [ ] Frontend can connect to backend API
- [ ] All API endpoints are working
- [ ] User registration works
- [ ] User login works
- [ ] Resume upload works
- [ ] ATS scoring works
- [ ] Results page displays correctly
- [ ] Error handling works
- [ ] Monitoring is configured
- [ ] Backups are configured

---

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review service documentation (Vercel, Render/Railway, PostgreSQL)
3. Check application logs
4. Contact support for your hosting provider

