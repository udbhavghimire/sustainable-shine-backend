# Setting Up SSL for Your Django Backend (FREE)

## Overview

Transform your backend from:
- ❌ `http://170.64.177.253:8000` 
- ✅ `https://api.sustainableshine.com.au`

**Cost: $0** - Everything is free!

---

## Step 1: Add DNS Record (FREE - 5 minutes)

### Where to Add DNS Record:

Go to wherever you manage your domain (sustainableshine.com.au):
- **GoDaddy**: Domains → DNS → Add Record
- **Namecheap**: Domain List → Manage → Advanced DNS
- **Google Domains**: DNS → Manage custom records
- **Cloudflare**: DNS → Add record
- **Other registrar**: Look for "DNS Management" or "DNS Settings"

### DNS Record to Add:

```
Record Type: A
Host/Name: api
Points to/Value: 170.64.177.253
TTL: 3600 (or Auto/Default)
```

**Visual Example:**
```
┌─────────────────────────────────────────────────┐
│ Type │ Name │ Value              │ TTL         │
├──────┼──────┼───────────────────┼─────────────┤
│  A   │ api  │ 170.64.177.253    │ 3600        │
└─────────────────────────────────────────────────┘
```

### Wait for DNS Propagation:

DNS changes take 5-60 minutes to propagate worldwide.

---

## Step 2: Verify DNS is Working

After adding the DNS record, check if it's working:

### Option A: Using dig command (Mac/Linux)
```bash
dig api.sustainableshine.com.au

# Look for this in output:
# api.sustainableshine.com.au. 3600 IN A 170.64.177.253
```

### Option B: Using nslookup (Windows/Mac/Linux)
```bash
nslookup api.sustainableshine.com.au

# Should show:
# Address: 170.64.177.253
```

### Option C: Online DNS Checker
Visit: https://dnschecker.org
Enter: `api.sustainableshine.com.au`
Should show: `170.64.177.253`

---

## Step 3: Install Nginx (Automated Script)

Once DNS is working, run this script to install everything:

### Installation Script:

Save this as `setup-ssl.sh` on your local machine:

```bash
#!/bin/bash

DOMAIN="api.sustainableshine.com.au"
DROPLET_IP="170.64.177.253"
EMAIL="your-email@example.com"  # Change this!

echo "🚀 Installing Nginx and SSL for $DOMAIN..."

ssh root@$DROPLET_IP << 'ENDSSH'

# Update system
apt update

# Install Nginx
apt install -y nginx

# Install Certbot for Let's Encrypt SSL
apt install -y certbot python3-certbot-nginx

# Create Nginx configuration
cat > /etc/nginx/sites-available/django-backend << 'EOF'
server {
    listen 80;
    server_name api.sustainableshine.com.au;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Serve static files
    location /static/ {
        alias /var/www/sustainable-shine-backend/staticfiles/;
    }

    # Serve media files
    location /media/ {
        alias /var/www/sustainable-shine-backend/media/;
    }
}
EOF

# Enable the site
ln -sf /etc/nginx/sites-available/django-backend /etc/nginx/sites-enabled/

# Remove default site
rm -f /etc/nginx/sites-enabled/default

# Test Nginx configuration
nginx -t

# Restart Nginx
systemctl restart nginx

echo "✅ Nginx installed and configured!"

ENDSSH

# Get SSL certificate
echo "🔐 Getting SSL certificate..."
ssh root@$DROPLET_IP "certbot --nginx -d $DOMAIN --non-interactive --agree-tos -m $EMAIL --redirect"

echo "✅ SSL certificate installed!"
echo ""
echo "🎉 Your API is now available at: https://$DOMAIN"
```

### Run the Script:

```bash
chmod +x setup-ssl.sh
./setup-ssl.sh
```

---

## Step 4: Update Django Settings

### Update .env on Droplet:

```bash
ssh root@170.64.177.253

# Edit .env file
nano /var/www/sustainable-shine-backend/.env

# Update ALLOWED_HOSTS to include subdomain:
ALLOWED_HOSTS=api.sustainableshine.com.au,sustainableshine.com.au,www.sustainableshine.com.au,170.64.177.253

# Save and exit (Ctrl+X, Y, Enter)

# Restart Gunicorn
systemctl restart gunicorn
```

---

## Step 5: Update Your Frontend

### Update Next.js Environment Variables:

#### Production (.env.production or Vercel/Netlify):
```env
NEXT_PUBLIC_API_URL=https://api.sustainableshine.com.au
```

#### Local (.env.local):
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Update API Calls:

```javascript
// lib/api.js
const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export const api = {
  blog: {
    getAll: async () => {
      const res = await fetch(`${API_URL}/api/blog/`);
      return res.json();
    },
  },
  bookings: {
    create: async (data) => {
      const res = await fetch(`${API_URL}/api/bookings/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
      });
      return res.json();
    },
  },
};
```

---

## Step 6: Test Everything

### Test API Endpoints:

```bash
# Test blog API
curl https://api.sustainableshine.com.au/api/blog/

# Test bookings API
curl https://api.sustainableshine.com.au/api/bookings/

# Test admin panel
open https://api.sustainableshine.com.au/admin/
```

### Test from Frontend:

```javascript
// Open browser console on sustainableshine.com.au
fetch('https://api.sustainableshine.com.au/api/blog/')
  .then(res => res.json())
  .then(data => console.log('✅ Success:', data))
  .catch(err => console.error('❌ Error:', err))
```

---

## Costs Breakdown

| Item | Cost |
|------|------|
| Subdomain (DNS record) | **FREE** |
| Nginx | **FREE** |
| Let's Encrypt SSL Certificate | **FREE** |
| SSL Auto-renewal | **FREE** |
| **Total** | **$0.00** |

The only cost is your existing Digital Ocean droplet ($4-6/month), which you already have!

---

## Benefits After Setup

| Before | After |
|--------|-------|
| ❌ `http://170.64.177.253:8000` | ✅ `https://api.sustainableshine.com.au` |
| ❌ Mixed content errors | ✅ No errors |
| ❌ Hard to remember IP | ✅ Professional subdomain |
| ❌ No encryption | ✅ SSL encrypted |
| ❌ Not production-ready | ✅ Production-ready |

---

## SSL Certificate Auto-Renewal

Let's Encrypt certificates expire after 90 days, but Certbot automatically renews them.

### Verify auto-renewal is set up:

```bash
ssh root@170.64.177.253 "certbot renew --dry-run"
```

Should show: "Congratulations, all renewals succeeded"

---

## Troubleshooting

### Issue: DNS not resolving
**Solution**: Wait longer (up to 24 hours max), clear DNS cache:
```bash
# Mac
sudo dscacheutil -flushcache

# Windows
ipconfig /flushdns
```

### Issue: Certbot fails with "connection refused"
**Solution**: Ensure Nginx is running and DNS is working:
```bash
systemctl status nginx
dig api.sustainableshine.com.au
```

### Issue: 502 Bad Gateway
**Solution**: Gunicorn might be down, restart it:
```bash
systemctl restart gunicorn
systemctl status gunicorn
```

---

## Quick Commands Reference

```bash
# Check Nginx status
ssh root@170.64.177.253 "systemctl status nginx"

# Check Gunicorn status
ssh root@170.64.177.253 "systemctl status gunicorn"

# View Nginx logs
ssh root@170.64.177.253 "tail -f /var/log/nginx/error.log"

# Restart everything
ssh root@170.64.177.253 "systemctl restart nginx gunicorn"

# Check SSL certificate expiry
ssh root@170.64.177.253 "certbot certificates"
```

---

## Summary Timeline

1. **5 minutes**: Add DNS record
2. **10-30 minutes**: Wait for DNS propagation
3. **5 minutes**: Run SSL setup script
4. **2 minutes**: Update Django settings
5. **2 minutes**: Update frontend environment variables
6. **1 minute**: Deploy frontend

**Total: ~25-45 minutes** (mostly waiting for DNS)

---

## Next Steps

Once DNS is set up, let me know and I'll:
1. Create the automated setup script for you
2. Run it to install Nginx and SSL
3. Test everything is working
4. Update your documentation

**Ready to start?** Just add the DNS record and let me know when it's propagating! 🚀
