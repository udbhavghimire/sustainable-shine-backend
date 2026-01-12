# Sustainable Shine Backend API

Django REST API for cleaning service bookings and blog management.

## Features

- Booking/Lead management API
- Blog post management
- Admin interface
- PostgreSQL database

## Deployment

Configured for Render.com with automatic migrations.

## Environment Variables Required

```
SECRET_KEY=your-secret-key
DEBUG=False
DJANGO_SETTINGS_MODULE=core.production_settings
DATABASE_URL=postgresql://...
ALLOWED_HOSTS=your-domain.com
CORS_ALLOWED_ORIGINS=https://your-frontend.com
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_EMAIL=admin@example.com
DJANGO_SUPERUSER_PASSWORD=secure-password
```

## API Endpoints

- `/api/bookings/` - Booking management
- `/api/blog/` - Blog posts
- `/admin/` - Admin interface
