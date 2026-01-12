# 🚀 Quick Deployment Steps

## Deploy Django Backend to api.sustainableshine.com.au

### ✅ Pre-Deployment Checklist

- [ ] All code committed to GitHub
- [ ] `requirements.txt` updated with production dependencies
- [ ] `Procfile` created
- [ ] `runtime.txt` created
- [ ] `production_settings.py` created
- [ ] `.gitignore` includes `.env` and sensitive files

---

## 📦 Step 1: Deploy to Railway (5 minutes)

### 1.1 Sign Up & Create Project

1. Go to https://railway.app
2. Click "Login" → Sign in with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your `sustainable-shine-backend` repository
5. Click "Deploy Now"

### 1.2 Add PostgreSQL Database

1. In your Railway project, click "+ New"
2. Select "Database" → "Add PostgreSQL"
3. Database will be automatically linked (DATABASE_URL created)

### 1.3 Set Environment Variables

Click on your web service → "Variables" tab → Add these:

```
SECRET_KEY=<generate using command below>
DEBUG=False
DJANGO_SETTINGS_MODULE=core.production_settings
ALLOWED_HOSTS=api.sustainableshine.com.au,your-app-name.up.railway.app
CORS_ALLOWED_ORIGINS=https://sustainableshine.com.au,https://www.sustainableshine.com.au
```

**Generate SECRET_KEY:**

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 1.4 Deploy & Run Migrations

1. Railway will automatically deploy (wait 2-3 minutes)
2. Once deployed, click on your service
3. Click "Deploy Logs" to monitor
4. After successful deployment, open Railway's terminal and run:

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic --noinput
```

---

## 🌐 Step 2: Configure Custom Domain

### 2.1 In Railway

1. Click your web service
2. Go to "Settings" tab
3. Scroll to "Domains" section
4. Click "Custom Domain"
5. Enter: `api.sustainableshine.com.au`
6. Railway will show you a CNAME target (e.g., `randomstring.up.railway.app`)

### 2.2 In Your Domain Provider (GoDaddy, Namecheap, etc.)

1. Login to where you registered `sustainableshine.com.au`
2. Find DNS Management / DNS Settings
3. Add a new CNAME record:
   - **Type**: CNAME
   - **Name**: `api` (this creates api.sustainableshine.com.au)
   - **Points to / Value**: `<the-railway-cname-from-step-2.1>`
   - **TTL**: 3600 or Auto
4. Save

**⏱️ Wait 5-60 minutes for DNS to propagate**

### 2.3 Update ALLOWED_HOSTS

Once DNS is working, update Railway environment variable:

```
ALLOWED_HOSTS=api.sustainableshine.com.au
```

---

## 🎨 Step 3: Update Your Next.js Frontend

### 3.1 Create Environment Variables

**Development (.env.local):**

```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api
```

**Production (.env.production):**

```env
NEXT_PUBLIC_API_URL=https://api.sustainableshine.com.au/api
```

### 3.2 Update All API Calls

**Example - BookingCalculator.jsx:**

```javascript
// Add at the top of the file
const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api';

// Update fetch calls from:
fetch('http://localhost:8000/api/bookings/', ...)

// To:
fetch(`${API_URL}/bookings/`, ...)
```

**Apply this to:**

- ✅ BookingCalculator component
- ✅ Blog list page
- ✅ Blog post page
- ✅ Admin dashboard (if you have one)

### 3.3 Deploy Frontend to Vercel

1. Push changes to GitHub
2. Vercel will auto-deploy
3. Or manually deploy from Vercel dashboard

---

## ✅ Step 4: Test Production

### 4.1 Test API Endpoints

```bash
# Test bookings endpoint
curl https://api.sustainableshine.com.au/api/bookings/

# Test blog endpoint
curl https://api.sustainableshine.com.au/api/blog/
```

### 4.2 Test Admin Panel

Visit: `https://api.sustainableshine.com.au/admin/`
Login with superuser credentials

### 4.3 Test From Frontend

1. Visit your Next.js site
2. Submit a test booking
3. Check if it appears in Django admin

---

## 🐛 Troubleshooting

### Issue: "DisallowedHost at /"

**Fix**: Add your domain to `ALLOWED_HOSTS` in Railway variables

### Issue: CORS error from frontend

**Fix**: Add your frontend URL to `CORS_ALLOWED_ORIGINS`

### Issue: Can't access admin (CSS not loading)

**Fix**: Run `python manage.py collectstatic --noinput` in Railway terminal

### Issue: 502 Bad Gateway

**Fix**: Check Railway logs for errors. Common causes:

- Wrong `DJANGO_SETTINGS_MODULE`
- Database connection issues
- Missing dependencies

### Issue: Database connection error

**Fix**: Ensure PostgreSQL is added and `DATABASE_URL` is set

---

## 📊 Post-Deployment

### Monitor Your App

- **Railway Dashboard**: Check logs, CPU, memory
- **Django Admin**: Monitor incoming bookings
- **Error Tracking**: Consider adding Sentry

### Regular Maintenance

- [ ] Set up automated backups
- [ ] Monitor error logs
- [ ] Update dependencies regularly
- [ ] Review security settings

---

## 🎉 You're Live!

Your production URLs:

- **API Base**: `https://api.sustainableshine.com.au/api/`
- **Admin Panel**: `https://api.sustainableshine.com.au/admin/`
- **Bookings API**: `https://api.sustainableshine.com.au/api/bookings/`
- **Blog API**: `https://api.sustainableshine.com.au/api/blog/`

---

## 💡 Next Steps

1. ✅ Test all functionality
2. ✅ Create some blog posts
3. ✅ Submit test bookings
4. ✅ Set up monitoring/alerts
5. ✅ Configure media file storage (AWS S3 recommended)
6. ✅ Set up automated backups
7. ✅ Add email notifications (optional)

---

## 🔑 Important Notes

- **Never commit `.env` file** to GitHub
- **Keep SECRET_KEY secure**
- **Use environment variables** for all sensitive data
- **Regular backups** are essential
- **Monitor your Railway usage** to avoid unexpected charges

---

## 💰 Estimated Costs

**Railway:**

- Free: $5 credit/month (good for testing)
- Hobby: $5/month (recommended for production)

**Vercel (Frontend):**

- Free tier is perfect for most sites

**Total: ~$5-10/month** for both frontend and backend

---

## 📞 Need Help?

- **Railway Docs**: https://docs.railway.app
- **Django Docs**: https://docs.djangoproject.com
- **Check logs** in Railway dashboard for errors

**Your deployment is ready! 🚀**
