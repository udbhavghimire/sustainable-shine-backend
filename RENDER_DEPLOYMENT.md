# 🚀 Deploy to Render - Quick Guide

## Your Cloudinary Credentials

```
CLOUDINARY_CLOUD_NAME=dmbeugy6d
CLOUDINARY_API_KEY=755859763682432
CLOUDINARY_API_SECRET=UrdgqvG5G0hMxkjSg-xgjTBUbT8
```

---

## Step 1: Push Your Code to GitHub

```bash
git add .
git commit -m "Add Cloudinary integration"
git push origin main
```

---

## Step 2: Create PostgreSQL Database

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click **"New +"** → **"PostgreSQL"**
3. Settings:
   - **Name**: `sustainable-shine-db`
   - **Plan**: Free
4. Click **"Create Database"**
5. **Copy the "Internal Database URL"** (you'll need this)

---

## Step 3: Create Web Service

1. Click **"New +"** → **"Web Service"**
2. Connect your GitHub repository
3. Settings:
   - **Name**: `sustainable-shine-backend`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn core.wsgi:application`

---

## Step 4: Add Environment Variables

Click **"Advanced"** → Add these environment variables:

### Required Variables:

```
SECRET_KEY=<generate-at-https://djecrety.ir/>
DEBUG=False
ALLOWED_HOSTS=sustainable-shine-backend.onrender.com
DATABASE_URL=<paste-internal-database-url-from-step-2>
CLOUDINARY_CLOUD_NAME=dmbeugy6d
CLOUDINARY_API_KEY=755859763682432
CLOUDINARY_API_SECRET=UrdgqvG5G0hMxkjSg-xgjTBUbT8
```

### Optional (for your frontend):

```
CORS_ALLOWED_ORIGINS=https://your-frontend-domain.com
```

**Note**: 
- Replace `sustainable-shine-backend` in ALLOWED_HOSTS with YOUR actual Render app name
- For CORS_ALLOWED_ORIGINS, add your actual frontend URL (e.g., Vercel, Netlify)

---

## Step 5: Deploy

1. Click **"Create Web Service"**
2. Wait 3-5 minutes for deployment
3. Watch the logs for any errors

---

## Step 6: Run Migrations

After deployment completes:

1. In Render dashboard, click your web service
2. Go to **"Shell"** tab
3. Run these commands:

```bash
python manage.py migrate
python manage.py createsuperuser
```

---

## Step 7: Test Everything

### Test 1: API
Visit: `https://sustainable-shine-backend.onrender.com/api/blog/`

Should see JSON response ✅

### Test 2: Admin
Visit: `https://sustainable-shine-backend.onrender.com/admin/`

Login with superuser credentials ✅

### Test 3: Upload Image
1. In admin, create a new blog post
2. Upload an image
3. Save
4. Check Cloudinary dashboard - image should appear!
5. API should return Cloudinary URL like: `https://res.cloudinary.com/dmbeugy6d/...`

---

## ✅ Done!

Your backend is now live with persistent image storage!

### Update Your Frontend:

Change your API URL to:
```javascript
const API_BASE_URL = "https://sustainable-shine-backend.onrender.com/api";
```

### Important:
- Replace `sustainable-shine-backend` with YOUR actual Render app name
- Images will now persist forever on Cloudinary
- No more broken image links!

---

## 🆘 Troubleshooting

**Images not showing?**
- Check Cloudinary env vars are set correctly
- No typos in credentials
- Check Render logs for errors

**Can't connect to database?**
- Verify DATABASE_URL is set
- Make sure you used the "Internal Database URL"

**CORS errors?**
- Add your frontend URL to CORS_ALLOWED_ORIGINS
- Include `https://` in the URL

---

**Need Help?** Check Render logs first, they usually show the exact error.
