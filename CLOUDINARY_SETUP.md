# Cloudinary Setup Guide

## Why Cloudinary?

Render's filesystem is **ephemeral** - uploaded files are deleted when your app restarts. Cloudinary provides persistent cloud storage.

## Setup Steps

### 1. Create Cloudinary Account

1. Sign up: [https://cloudinary.com/users/register/free](https://cloudinary.com/users/register/free)
2. Free tier: 25GB storage + 25GB bandwidth/month

### 2. Get Credentials

From your Cloudinary dashboard, copy:
- Cloud Name
- API Key
- API Secret

### 3. Add to Render

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Select your web service → "Environment" tab
3. Add these variables:

```
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret
```

4. Click "Save Changes"
5. Render will automatically redeploy

### 4. Verify

1. Go to `https://your-app.onrender.com/admin/`
2. Upload a blog post with an image
3. Check Cloudinary dashboard → Media Library
4. Image should appear there
5. Images persist even after app restarts!

## How It Works

**Before**: `/media/blog/photo.jpg` → Deleted on restart ❌
**After**: `https://res.cloudinary.com/.../photo.jpg` → Persists forever ✅

## Local Development

Create a `.env` file:

```env
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret
```

## Free Tier

- 25GB storage
- 25GB bandwidth/month
- More than enough for most websites!

## Resources

- [Cloudinary Docs](https://cloudinary.com/documentation)
- [Django Cloudinary Storage](https://github.com/klis87/django-cloudinary-storage)
