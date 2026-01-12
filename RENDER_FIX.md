# 🔧 Fix Render Deployment Error

## Error: "Error loading psycopg2 or psycopg module"

This error occurs when the PostgreSQL driver can't be loaded. Here's how to fix it:

---

## ✅ **Solution 1: Update Files (RECOMMENDED)**

I've already updated these files for you:

### Files Fixed:

1. ✅ `runtime.txt` - Removed extra blank lines
2. ✅ `requirements.txt` - Updated psycopg2-binary version

### Now Push to GitHub:

```bash
cd /Users/udbhavghimire/Desktop/sustainable-shine-backend

# Add the fixed files
git add runtime.txt requirements.txt

# Commit
git commit -m "Fix psycopg2 deployment error"

# Push
git push
```

**Render will automatically redeploy!**

---

## ✅ **Solution 2: If Still Failing**

### Option A: Use Render's Python Version Setting

Instead of `runtime.txt`, set Python version in Render dashboard:

1. Go to your service in Render
2. Click "**Environment**" tab
3. Under "Python Version", select: **3.12**
4. Click "**Save Changes**"
5. Render will redeploy

### Option B: Use Specific Build Command

Update your Build Command in Render to:

```bash
pip install --upgrade pip && pip install -r requirements.txt
```

---

## ✅ **Solution 3: Alternative PostgreSQL Driver**

If psycopg2-binary still fails, use psycopg3 (newer, better):

### Update requirements.txt:

Change from:

```txt
psycopg2-binary==2.9.10
```

To:

```txt
psycopg[binary]==3.1.18
```

### Update production_settings.py:

No changes needed! psycopg3 is a drop-in replacement.

---

## 🚀 **Quick Fix Steps**

### Step 1: Commit and Push

```bash
cd /Users/udbhavghimire/Desktop/sustainable-shine-backend
git add .
git commit -m "Fix Render deployment"
git push
```

### Step 2: Monitor Deployment

1. Go to Render dashboard
2. Watch the logs
3. Wait for "Your service is live!" message

### Step 3: If Still Failing

Check the logs and look for:

- Python version being used
- Which packages are being installed
- Specific error messages

Then try Solution 2 or 3 above.

---

## 🔍 **Verify Environment Variables**

Make sure these are set in Render:

```
SECRET_KEY=<your-secret-key>
DEBUG=False
DJANGO_SETTINGS_MODULE=core.production_settings
DATABASE_URL=<your-postgres-internal-url>
ALLOWED_HOSTS=<your-app-name>.onrender.com
CORS_ALLOWED_ORIGINS=https://sustainableshine.com.au
```

**Missing DATABASE_URL?**

- You need to create a PostgreSQL database in Render first
- Then copy the "Internal Database URL"
- Add it as an environment variable

---

## 📋 **Complete Checklist**

- [ ] PostgreSQL database created in Render
- [ ] `DATABASE_URL` environment variable set (Internal URL)
- [ ] All other environment variables set
- [ ] `runtime.txt` has no extra blank lines
- [ ] `requirements.txt` has psycopg2-binary or psycopg
- [ ] Changes committed and pushed to GitHub
- [ ] Deployment triggered in Render
- [ ] Logs show successful installation
- [ ] Service starts successfully

---

## 💡 **Common Issues**

### Issue: "No module named 'psycopg2'"

**Fix**: Ensure `psycopg2-binary` is in requirements.txt

### Issue: Python version mismatch

**Fix**: Use Python 3.12 (not 3.13) in runtime.txt or Render settings

### Issue: Database connection refused

**Fix**:

- Use **Internal Database URL** (not External)
- Format: `postgresql://user:pass@hostname/dbname`

### Issue: Build timeout

**Fix**: Add to Build Command: `pip install --upgrade pip`

---

## 🎯 **Recommended: Use psycopg3**

For best compatibility with Python 3.12+:

### Update requirements.txt:

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
psycopg[binary]==3.1.18  # ← Use this instead of psycopg2-binary
whitenoise==6.6.0
dj-database-url==2.1.0
python-decouple==3.8
```

Then commit and push!

---

## 📞 **Still Having Issues?**

### Check These:

1. **Render Logs**

   - Go to your service → Logs tab
   - Look for the exact error message

2. **Database Connection**

   ```bash
   # In Render Shell, test:
   python manage.py dbshell
   ```

3. **Environment Variables**

   - Ensure no typos
   - DATABASE_URL must be the Internal URL
   - DJANGO_SETTINGS_MODULE=core.production_settings

4. **Python Version**
   - Render supports: 3.8, 3.9, 3.10, 3.11, 3.12
   - Use 3.12 for best compatibility

---

## ✨ **After Successful Deploy**

Run these commands in Render Shell:

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic --noinput
```

Then test:

```bash
curl https://your-app-name.onrender.com/api/bookings/
```

---

## 🎉 **Success!**

Once deployed, your API will be live at:

- https://your-app-name.onrender.com/api/
- https://your-app-name.onrender.com/admin/

Test it and start using it!

---

Good luck! The fixes I made should resolve the issue. Just push to GitHub! 🚀
