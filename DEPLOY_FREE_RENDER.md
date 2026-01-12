# 🆓 Deploy Django Backend to Render.com (100% FREE)

## Complete FREE Deployment Guide

Render.com offers a completely FREE tier perfect for development and low-traffic sites.

---

## ⚠️ Important: Free Tier Limitations

- Web service **spins down after 15 minutes** of inactivity
- Takes ~30 seconds to wake up on first request
- 512 MB RAM
- 100GB bandwidth/month
- PostgreSQL included FREE (1GB storage)
- Perfect for: Development, testing, personal projects, low-traffic sites

---

## 🚀 Step-by-Step Deployment (20 minutes)

### Step 1: Sign Up for Render (2 minutes)

1. Go to https://render.com
2. Click "Get Started"
3. Sign up with GitHub (recommended)
4. Verify your email

---

### Step 2: Create PostgreSQL Database (3 minutes)

1. From Render Dashboard, click "**New +**"
2. Select "**PostgreSQL**"
3. Configure:
   - **Name**: `sustainable-shine-db`
   - **Database**: `sustainableshine` (or leave default)
   - **User**: (auto-generated)
   - **Region**: Choose closest to your users (e.g., Singapore for Australia)
   - **PostgreSQL Version**: 16 (latest)
   - **Plan**: **FREE** ⭐
4. Click "**Create Database**"
5. Wait for database to be created (~2 minutes)
6. **IMPORTANT**: Copy the "**Internal Database URL**" (you'll need this!)
   - It looks like: `postgresql://user:password@host/database`

---

### Step 3: Prepare Your Code (5 minutes)

#### 3.1 Ensure All Files are Present

Check these files exist in your project:

- ✅ `Procfile`
- ✅ `runtime.txt`
- ✅ `requirements.txt`
- ✅ `core/production_settings.py`

#### 3.2 Push to GitHub

```bash
cd /Users/udbhavghimire/Desktop/sustainable-shine-backend

# Initialize git (if not already)
git init

# Add all files
git add .

# Commit
git commit -m "Prepare for Render deployment"

# Create GitHub repo and push
# (Create repo on GitHub first, then:)
git remote add origin https://github.com/yourusername/sustainable-shine-backend.git
git branch -M main
git push -u origin main
```

---

### Step 4: Deploy Web Service (5 minutes)

1. From Render Dashboard, click "**New +**"
2. Select "**Web Service**"
3. Click "**Connect** your GitHub account" (if not already connected)
4. Find and select your `sustainable-shine-backend` repository
5. Click "**Connect**"

#### 4.1 Configure Web Service

Fill in these settings:

**Basic Settings:**

- **Name**: `sustainable-shine-api` (or your choice)
- **Region**: Same as your database (e.g., Singapore)
- **Branch**: `main`
- **Root Directory**: (leave empty)
- **Runtime**: `Python 3`

**Build & Deploy:**

- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn core.wsgi:application`

**Plan:**

- Select **FREE** ⭐

Click "**Advanced**" to add environment variables

---

### Step 5: Add Environment Variables (5 minutes)

Click "**Add Environment Variable**" and add these:

#### Required Variables:

1. **SECRET_KEY**

   - Value: Generate a new one using:

   ```bash
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```

2. **DEBUG**

   - Value: `False`

3. **DJANGO_SETTINGS_MODULE**

   - Value: `core.production_settings`

4. **DATABASE_URL**

   - Value: (Paste the Internal Database URL from Step 2)
   - Example: `postgresql://user:pass@dpg-xxxxx-a.singapore-postgres.render.com/dbname`

5. **ALLOWED_HOSTS**

   - Value: `sustainable-shine-api.onrender.com,api.sustainableshine.com.au`
   - (Replace `sustainable-shine-api` with your actual service name)

6. **CORS_ALLOWED_ORIGINS**
   - Value: `https://sustainableshine.com.au,https://www.sustainableshine.com.au`
   - (Your Next.js frontend URLs)

**Click "Create Web Service"** - Deployment will start automatically!

---

### Step 6: Wait for Deployment (3-5 minutes)

- Watch the logs as your app builds and deploys
- First deployment takes 3-5 minutes
- You'll see logs like:
  ```
  ==> Building...
  ==> Installing dependencies...
  ==> Starting server...
  ==> Your service is live!
  ```

---

### Step 7: Run Database Migrations (2 minutes)

Once deployed:

1. Go to your web service dashboard
2. Click "**Shell**" tab (on the left)
3. A terminal will open
4. Run these commands:

```bash
# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser
# Follow prompts: username, email, password

# Collect static files
python manage.py collectstatic --noinput
```

**Done! Your API is now live!** 🎉

---

### Step 8: Test Your API

Your API is now available at:

- **https://sustainable-shine-api.onrender.com** (replace with your service name)

Test endpoints:

```bash
# Test bookings API
curl https://sustainable-shine-api.onrender.com/api/bookings/

# Test blog API
curl https://sustainable-shine-api.onrender.com/api/blog/

# Access admin
# Visit: https://sustainable-shine-api.onrender.com/admin/
```

---

## 🌐 Step 9: Add Custom Domain (Optional)

### 9.1 In Render Dashboard

1. Go to your web service
2. Click "**Settings**" tab
3. Scroll to "**Custom Domains**"
4. Click "**Add Custom Domain**"
5. Enter: `api.sustainableshine.com.au`
6. Render will provide CNAME record details

### 9.2 In Your Domain Provider

1. Login to where you manage `sustainableshine.com.au`
2. Go to DNS Management
3. Add new CNAME record:
   - **Type**: CNAME
   - **Name**: `api`
   - **Points to**: `sustainable-shine-api.onrender.com` (your Render URL)
   - **TTL**: 3600
4. Save changes

**Wait 5-60 minutes for DNS to propagate**

### 9.3 Update Environment Variables

After DNS is configured, update in Render:

- **ALLOWED_HOSTS**: `api.sustainableshine.com.au,sustainable-shine-api.onrender.com`

---

## 🎨 Step 10: Update Your Next.js Frontend

### 10.1 Environment Variables

**Development (.env.local):**

```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api
```

**Production (.env.production):**

```env
NEXT_PUBLIC_API_URL=https://api.sustainableshine.com.au/api
```

_Or use: `https://sustainable-shine-api.onrender.com/api` if not using custom domain_

### 10.2 Update Code

In your Next.js components, update API calls:

```javascript
// BookingCalculator.jsx
const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api";

// Update fetch calls
const response = await fetch(`${API_URL}/bookings/`, {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
  },
  body: JSON.stringify(bookingData),
});
```

Apply this to all API calls in your frontend.

---

## ⚡ About the Spin-Down Feature

### What Happens:

- After 15 minutes of no requests, Render puts your app to "sleep"
- First request after sleep takes ~30 seconds to wake up
- Subsequent requests are instant
- This saves server resources (why it's free!)

### Solutions:

**Option A: Accept it** (Recommended for free tier)

- Good for: Development, testing, personal projects
- Users might experience a 30-second delay occasionally
- After first load, everything is fast

**Option B: Keep-alive Service** (Free workaround)

- Use a service like UptimeRobot (free) to ping your API every 5 minutes
- Keeps your app awake during business hours
- Setup at: https://uptimerobot.com

**Option C: Upgrade to Paid** ($7/month)

- Always-on, no spin-down
- 512 MB RAM guaranteed
- When you're ready for production

---

## 🔧 Troubleshooting

### Issue: "Application failed to start"

**Check:**

1. Logs for Python errors
2. Ensure `requirements.txt` has all dependencies
3. Verify `Procfile` exists and is correct

### Issue: "DisallowedHost"

**Solution:** Add your domain to `ALLOWED_HOSTS` environment variable

### Issue: Database connection error

**Solution:** Verify `DATABASE_URL` is set correctly (use Internal Database URL)

### Issue: Static files not loading

**Solution:**

1. Check `whitenoise` is in `requirements.txt`
2. Run `python manage.py collectstatic` in Shell

### Issue: CORS errors from frontend

**Solution:** Ensure frontend URL is in `CORS_ALLOWED_ORIGINS`

---

## 📊 Monitor Your App

### In Render Dashboard:

1. **Logs**: Real-time application logs
2. **Metrics**: CPU, memory usage
3. **Events**: Deployment history
4. **Shell**: Run Django commands

### Set Up Monitoring:

Consider adding:

- **Sentry** (free tier) for error tracking
- **UptimeRobot** (free) for uptime monitoring
- **New Relic** (free tier) for performance monitoring

---

## 💡 Tips for Free Tier

### Make the Most of Free Tier:

1. **Add Loading State** in frontend for cold starts

   ```javascript
   if (loading) {
     return <div>Waking up the server... (may take 30 seconds)</div>;
   }
   ```

2. **Use UptimeRobot** to ping API every 5 minutes (keeps it awake)

3. **Optimize Database Queries** (limited to 1GB storage)

4. **Enable Caching** where possible

5. **Monitor Usage** in Render dashboard

---

## 🎓 When to Upgrade

Consider upgrading to paid ($7/month) when:

- ❌ Spin-down delay is annoying users
- ❌ Need more than 512MB RAM
- ❌ Traffic increases significantly
- ❌ Ready for production launch

---

## ✅ Deployment Checklist

- [ ] GitHub repository created and pushed
- [ ] PostgreSQL database created on Render
- [ ] Web service deployed on Render
- [ ] All environment variables set
- [ ] Database migrations run
- [ ] Superuser created
- [ ] Static files collected
- [ ] API endpoints tested
- [ ] Admin panel accessible
- [ ] Custom domain configured (optional)
- [ ] Frontend updated with production API URL
- [ ] Test booking submission from frontend
- [ ] Monitor logs for any errors

---

## 🎉 You're Live! (For FREE!)

**Your Production URLs:**

- API: `https://sustainable-shine-api.onrender.com/api/`
- Admin: `https://sustainable-shine-api.onrender.com/admin/`
- Custom: `https://api.sustainableshine.com.au/api/` (if configured)

**Cost: $0/month** 💰

**Perfect for:**

- ✅ Development
- ✅ Testing
- ✅ MVP/Prototype
- ✅ Low-traffic personal projects
- ✅ Learning

**Upgrade when ready for production traffic!**

---

## 📞 Resources

- **Render Docs**: https://render.com/docs
- **Django Docs**: https://docs.djangoproject.com
- **Support**: Render has great community forum

---

Happy deploying! 🚀 Your backend is now live for FREE!
