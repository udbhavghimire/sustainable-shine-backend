# Digital Ocean Droplet Deployment Guide

## Quick Deployment (Using the Script)

### 1. Configure the deployment script

Edit `deploy.sh` and update these values:

```bash
DROPLET_USER="root"  # Your SSH user (root, ubuntu, etc.)
DROPLET_IP="YOUR_DROPLET_IP"  # Your droplet's IP address
APP_DIR="/var/www/sustainable-shine-backend"  # Path to your app on the droplet
```

### 2. Run the deployment script

```bash
./deploy.sh
```

The script will:
- Pull latest code from GitHub
- Install dependencies
- Run migrations
- Collect static files
- Restart Gunicorn and Nginx

---

## Manual Deployment (Step by Step)

If you prefer to deploy manually or the script doesn't work:

### 1. Push your local changes to GitHub

```bash
git add .
git commit -m "Your change description"
git push origin main
```

### 2. SSH into your Digital Ocean Droplet

```bash
ssh root@YOUR_DROPLET_IP
# or
ssh YOUR_USER@YOUR_DROPLET_IP
```

### 3. Navigate to your app directory

```bash
cd /var/www/sustainable-shine-backend
# or wherever your app is located
```

### 4. Pull the latest changes

```bash
git pull origin main
```

### 5. Activate virtual environment

```bash
source venv/bin/activate
```

### 6. Install any new dependencies

```bash
pip install -r requirements.txt
```

### 7. Run migrations (if database changed)

```bash
python manage.py migrate
```

### 8. Collect static files

```bash
python manage.py collectstatic --noinput
```

### 9. Restart Gunicorn service

```bash
sudo systemctl restart gunicorn
# or
sudo supervisorctl restart gunicorn  # if using supervisor
```

### 10. Reload Nginx

```bash
sudo systemctl reload nginx
```

### 11. Check service status

```bash
sudo systemctl status gunicorn
sudo systemctl status nginx
```

---

## Common Issues and Solutions

### Issue: "Permission denied (publickey)"

**Solution**: Your SSH key isn't configured
```bash
# Generate SSH key if you don't have one
ssh-keygen -t ed25519 -C "your_email@example.com"

# Copy public key to droplet
ssh-copy-id root@YOUR_DROPLET_IP
```

### Issue: "git pull" requires password

**Solution**: Set up SSH key for GitHub
```bash
# On your droplet, generate SSH key
ssh-keygen -t ed25519 -C "your_email@example.com"

# View public key
cat ~/.ssh/id_ed25519.pub

# Add this key to GitHub: Settings → SSH and GPG keys → New SSH key
```

### Issue: Gunicorn service not found

**Solution**: Check your service name
```bash
# List all services with 'gunicorn' in name
sudo systemctl list-units --all | grep gunicorn

# Or check supervisor
sudo supervisorctl status
```

### Issue: Changes not appearing

**Solution**: Clear browser cache or:
```bash
# Hard reload static files
python manage.py collectstatic --clear --noinput

# Restart services
sudo systemctl restart gunicorn nginx
```

---

## Deployment Checklist

Before deploying:
- [ ] Test changes locally
- [ ] Commit all changes
- [ ] Push to GitHub
- [ ] Backup production database (optional but recommended)

After deploying:
- [ ] Check website loads
- [ ] Test API endpoints
- [ ] Check admin panel
- [ ] Review error logs if issues occur

---

## Checking Logs

If something goes wrong:

```bash
# Gunicorn logs
sudo journalctl -u gunicorn -n 50

# Nginx error logs
sudo tail -n 50 /var/log/nginx/error.log

# Application logs
tail -n 50 /var/www/sustainable-shine-backend/logs/django.log
```

---

## Environment Variables

Make sure your `.env` file on the droplet is configured for production:

```bash
# On the droplet
cd /var/www/sustainable-shine-backend
nano .env
```

Key settings:
```
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
SECRET_KEY=<production-secret-key>
```

---

## Need Help?

Common commands:
- Check app directory: `ls -la /var/www/`
- Find gunicorn service: `sudo systemctl list-units | grep gunicorn`
- Test nginx config: `sudo nginx -t`
- Restart everything: `sudo systemctl restart gunicorn nginx`
