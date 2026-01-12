# 🚀 Production Deployment Guide

## Deploying Django Backend to Production with Custom Subdomain

This guide will help you deploy your Django backend to `api.sustainableshine.com.au` using Railway (recommended) or other platforms.

---

## 📋 Architecture Overview

**Recommended Setup:**

- **Frontend (Next.js)**: Deploy to **Vercel** → `sustainableshine.com.au`
- **Backend (Django)**: Deploy to **Railway** → `api.sustainableshine.com.au`

---

## 🎯 Option 1: Railway.app (RECOMMENDED - Easiest!)

Railway is perfect for Django with excellent free tier and simple setup.

### **Step 1: Prepare Your Django Project**

#### 1.1 Install Production Dependencies

Add to `requirements.txt`:

```txt
asgiref==3.11.0
Django==6.0.1
django-cors-headers==4.9.0
djangorestframework==3.16.1
django-filter==24.3
Pillow==12.1.0
sqlparse==0.5.5

# Production dependencies
gunicorn==21.2.0
psycopg2-binary==2.9.9
whitenoise==6.6.0
dj-database-url==2.1.0
python-decouple==3.8
```

#### 1.2 Create Production Settings File

Create `core/production_settings.py`:

```python
from .settings import *
import os
import dj_database_url
from decouple import config

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=False, cast=bool)

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# Allowed hosts
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='').split(',')

# Database
DATABASES = {
    'default': dj_database_url.config(
        default=config('DATABASE_URL'),
        conn_max_age=600,
        conn_health_checks=True,
    )
}

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# WhiteNoise configuration
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Add WhiteNoise middleware
MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# CORS for production
CORS_ALLOWED_ORIGINS = config('CORS_ALLOWED_ORIGINS', default='').split(',')
CORS_ALLOW_CREDENTIALS = True

# Security settings
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# HSTS
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
```

#### 1.3 Create Environment Variables Template

Create `.env.example`:

```env
# Django Settings
SECRET_KEY=your-secret-key-here-change-this
DEBUG=False
ALLOWED_HOSTS=api.sustainableshine.com.au,your-railway-domain.up.railway.app

# Database (Railway will provide this automatically)
DATABASE_URL=postgresql://user:password@host:port/database

# CORS Origins (your frontend URLs)
CORS_ALLOWED_ORIGINS=https://sustainableshine.com.au,https://www.sustainableshine.com.au

# Email Settings (optional - for later)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

#### 1.4 Create Procfile

Create `Procfile` in root directory:

```
web: gunicorn core.wsgi --log-file -
```

#### 1.5 Create runtime.txt

Create `runtime.txt`:

```
python-3.12.4
```

#### 1.6 Update .gitignore

Ensure `.gitignore` includes:

```
.env
*.pyc
__pycache__/
db.sqlite3
staticfiles/
media/
venv/
```

---

### **Step 2: Deploy to Railway**

#### 2.1 Sign Up & Create Project

1. Go to [railway.app](https://railway.app)
2. Sign up with GitHub
3. Click "New Project"
4. Select "Deploy from GitHub repo"
5. Choose your Django repository

#### 2.2 Add PostgreSQL Database

1. In your Railway project, click "New"
2. Select "Database" → "PostgreSQL"
3. Railway will automatically create `DATABASE_URL` environment variable

#### 2.3 Configure Environment Variables

In Railway project settings, add these environment variables:

```env
SECRET_KEY=generate-a-new-secure-secret-key
DEBUG=False
ALLOWED_HOSTS=api.sustainableshine.com.au,your-project.up.railway.app
CORS_ALLOWED_ORIGINS=https://sustainableshine.com.au,https://www.sustainableshine.com.au
DJANGO_SETTINGS_MODULE=core.production_settings
```

**Generate SECRET_KEY:**

```python
# Run this in Python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

#### 2.4 Deploy

1. Railway will automatically deploy when you push to GitHub
2. Or click "Deploy" in Railway dashboard
3. Wait for build to complete (~3-5 minutes)

#### 2.5 Run Migrations

In Railway terminal:

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic --noinput
```

---

### **Step 3: Configure Custom Domain (api.sustainableshine.com.au)**

#### 3.1 In Railway

1. Go to your Railway project
2. Click "Settings" → "Domains"
3. Click "Custom Domain"
4. Enter: `api.sustainableshine.com.au`
5. Railway will provide you with a CNAME record

#### 3.2 In Your Domain Provider (e.g., GoDaddy, Namecheap, etc.)

1. Log into your domain registrar where `sustainableshine.com.au` is registered
2. Go to DNS Management
3. Add a new CNAME record:
   - **Type**: CNAME
   - **Name/Host**: `api`
   - **Value/Points to**: `your-project.up.railway.app` (provided by Railway)
   - **TTL**: 3600 (or automatic)
4. Save changes

**DNS propagation takes 5-60 minutes**

#### 3.3 Update Django Settings

Once DNS is configured, update Railway environment variables:

```env
ALLOWED_HOSTS=api.sustainableshine.com.au
CORS_ALLOWED_ORIGINS=https://sustainableshine.com.au,https://www.sustainableshine.com.au
```

---

### **Step 4: Update Frontend (Next.js) to Use Production API**

#### 4.1 Create Environment Variables in Next.js

Create `.env.local` (development):

```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api
```

Create `.env.production` (production):

```env
NEXT_PUBLIC_API_URL=https://api.sustainableshine.com.au/api
```

#### 4.2 Update API Calls in Next.js

**BookingCalculator.jsx:**

```javascript
// At the top of your file
const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api";

// In handleSubmit function
const response = await fetch(`${API_URL}/bookings/`, {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
  },
  body: JSON.stringify(bookingData),
});
```

**Blog pages:**

```javascript
// In your blog list page
const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api";

const response = await fetch(`${API_URL}/blog/?status=published`);
```

---

## 🎯 Option 2: Render.com (Alternative)

### Deploy to Render

1. Go to [render.com](https://render.com)
2. Sign up with GitHub
3. Click "New +" → "Web Service"
4. Connect your Django repository
5. Configure:
   - **Name**: sustainable-shine-api
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn core.wsgi:application`
6. Add PostgreSQL database
7. Set environment variables (same as Railway)
8. Deploy

**Custom Domain**: Same process as Railway in their settings

---

## 🎯 Option 3: DigitalOcean App Platform

### Deploy to DigitalOcean

1. Go to [DigitalOcean App Platform](https://cloud.digitalocean.com/apps)
2. Create new app from GitHub
3. Select Django repository
4. Configure:
   - **Type**: Web Service
   - **Build Command**: `pip install -r requirements.txt`
   - **Run Command**: `gunicorn core.wsgi`
5. Add managed PostgreSQL database
6. Set environment variables
7. Deploy

**Custom Domain**: Configure in app settings

---

## 🔒 Production Checklist

Before going live, ensure:

- [ ] `DEBUG = False` in production
- [ ] New `SECRET_KEY` generated
- [ ] PostgreSQL database configured
- [ ] Environment variables set correctly
- [ ] `ALLOWED_HOSTS` includes your domain
- [ ] `CORS_ALLOWED_ORIGINS` includes frontend URLs
- [ ] SSL/HTTPS enabled (Railway does this automatically)
- [ ] Migrations run on production database
- [ ] Superuser created for admin access
- [ ] Static files collected
- [ ] Media file storage configured (consider AWS S3 for production)

---

## 📁 Media Files in Production

### Issue

Railway/Render have ephemeral filesystems - uploaded media files will be deleted on redeploy.

### Solution: Use AWS S3 or Cloudinary

#### Option A: AWS S3 (Recommended for production)

Install dependencies:

```bash
pip install django-storages boto3
```

Add to settings:

```python
# AWS S3 Configuration
AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME')
AWS_S3_REGION_NAME = 'ap-southeast-2'  # Sydney
AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'

# Media files
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/media/'
```

#### Option B: Cloudinary (Easier setup)

Install:

```bash
pip install cloudinary
```

Configure in settings.

---

## 🧪 Testing Production Deployment

After deployment:

1. **Test API endpoints:**

```bash
curl https://api.sustainableshine.com.au/api/bookings/
curl https://api.sustainableshine.com.au/api/blog/
```

2. **Test admin access:**
   Visit: `https://api.sustainableshine.com.au/admin/`

3. **Test booking submission:**
   From your frontend, submit a test booking

4. **Check CORS:**
   Ensure frontend can communicate with backend

---

## 🔧 Troubleshooting

### Issue: "DisallowedHost" Error

**Solution**: Add domain to `ALLOWED_HOSTS` in environment variables

### Issue: CORS Error from Frontend

**Solution**: Ensure frontend URL is in `CORS_ALLOWED_ORIGINS`

### Issue: Static files not loading

**Solution**: Run `python manage.py collectstatic` and ensure WhiteNoise is configured

### Issue: Database connection error

**Solution**: Check `DATABASE_URL` environment variable is set correctly

### Issue: 502 Bad Gateway

**Solution**: Check Railway logs for Python errors, ensure gunicorn is running

---

## 📊 Monitoring

After deployment:

1. **Railway Dashboard**: Monitor logs, CPU, memory usage
2. **Django Admin**: Check incoming bookings at `/admin/`
3. **Error Tracking**: Consider adding Sentry for error monitoring

---

## 💰 Costs

### Railway (Recommended)

- **Free Tier**: $5 credit/month (sufficient for testing)
- **Hobby**: $5/month for both web service + PostgreSQL
- **Pro**: $20/month (when you need more resources)

### Render

- **Free Tier**: Available (spins down after inactivity)
- **Starter**: $7/month

### DigitalOcean

- **Basic**: $5/month (app + database = $10/month)

---

## 🎉 Final Steps

Once deployed:

1. ✅ Test all API endpoints
2. ✅ Submit test booking from frontend
3. ✅ Create blog post via admin
4. ✅ Verify frontend can fetch blog posts
5. ✅ Set up monitoring
6. ✅ Create regular backups
7. ✅ Document your production URLs

---

## 📞 Quick Reference

**Production URLs:**

- Backend API: `https://api.sustainableshine.com.au/api/`
- Admin Panel: `https://api.sustainableshine.com.au/admin/`
- Frontend: `https://sustainableshine.com.au`

**Key Files:**

- `core/production_settings.py` - Production Django settings
- `Procfile` - Tells Railway how to run your app
- `runtime.txt` - Specifies Python version
- `.env` - Environment variables (NEVER commit this!)

**Support:**

- Railway Docs: https://docs.railway.app
- Render Docs: https://render.com/docs
- DigitalOcean Docs: https://docs.digitalocean.com

---

Good luck with your deployment! 🚀
