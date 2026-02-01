# Sustainable Shine Backend API

Django REST API for cleaning service bookings and blog management.

## Features

- Booking/Lead management API
- Blog post management with image uploads
- Admin interface
- PostgreSQL database support
- Cloudinary integration for persistent media storage

## 🚀 Quick Start (Local Development)

```bash
# Clone and setup
git clone <repository-url>
cd sustainable-shine-backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run server
python manage.py runserver
```

**Access:**
- API: http://localhost:8000/api/
- Admin: http://localhost:8000/admin/

## 📦 Deployment to Render

### Step 1: Get Cloudinary Credentials

1. Sign up at [Cloudinary](https://cloudinary.com/users/register/free)
2. Get your credentials from the dashboard:
   - Cloud Name
   - API Key
   - API Secret

### Step 2: Create PostgreSQL Database in Render

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click "New +" → "PostgreSQL"
3. Name: `sustainable-shine-db`
4. Click "Create Database"
5. Copy the "Internal Database URL"

### Step 3: Deploy Web Service

1. Click "New +" → "Web Service"
2. Connect your Git repository
3. Configure:
   - **Name**: `sustainable-shine-backend`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn core.wsgi:application`

4. **Add Environment Variables:**

```
SECRET_KEY=<generate-at-djecrety.ir>
DEBUG=False
ALLOWED_HOSTS=your-app-name.onrender.com
DATABASE_URL=<paste-from-step-2>
CORS_ALLOWED_ORIGINS=https://your-frontend-domain.com
CLOUDINARY_CLOUD_NAME=<your-cloud-name>
CLOUDINARY_API_KEY=<your-api-key>
CLOUDINARY_API_SECRET=<your-api-secret>
```

5. Click "Create Web Service"

### Step 4: Run Migrations

After deployment completes:
1. Go to your web service → "Shell" tab
2. Run: `python manage.py migrate`
3. Run: `python manage.py createsuperuser`

### Step 5: Test

- API: `https://your-app.onrender.com/api/blog/`
- Admin: `https://your-app.onrender.com/admin/`

## 🖼️ Why Cloudinary?

Render uses ephemeral storage - uploaded files are deleted when your app restarts. Cloudinary provides persistent cloud storage so your images are never lost.

**Before**: Images → Local storage → Deleted on restart ❌
**After**: Images → Cloudinary cloud → Persists forever ✅

## 🔗 API Endpoints

**Blog**: `/api/blog/` - List, create, update, delete blog posts
**Bookings**: `/api/bookings/` - Manage booking/lead submissions
**Admin**: `/admin/` - Django admin dashboard

## 🛠️ Tech Stack

Django 6.0 • Django REST Framework • PostgreSQL • Cloudinary • Pillow

## 📚 Resources

- See `CLOUDINARY_SETUP.md` for detailed Cloudinary setup instructions
- [Django Docs](https://docs.djangoproject.com/)
- [Render Docs](https://render.com/docs)
