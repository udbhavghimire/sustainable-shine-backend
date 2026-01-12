# Quick Command Reference

## Django Management Commands

### Start Development Server
```bash
cd /Users/udbhavghimire/Desktop/sustainable-shine-backend
source venv/bin/activate
python manage.py runserver
```

### Create Superuser
```bash
python manage.py createsuperuser
```

### Database Operations
```bash
# Create migrations after model changes
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Show migrations
python manage.py showmigrations

# Reset database (CAUTION: Deletes all data)
rm db.sqlite3
python manage.py migrate
```

### Django Shell
```bash
# Interactive Python shell with Django environment
python manage.py shell
```

Example shell commands:
```python
# Import models
from leads.models import Booking
from blog.models import BlogPost

# Count bookings
Booking.objects.count()

# Get all bookings
bookings = Booking.objects.all()

# Filter bookings
pending = Booking.objects.filter(status='pending')

# Create a booking
booking = Booking.objects.create(
    first_name='Test',
    last_name='User',
    email='test@example.com',
    # ... other fields
)

# Get all blog posts
posts = BlogPost.objects.all()

# Get published posts
published = BlogPost.objects.filter(status='published')
```

### Static Files
```bash
# Collect static files (for production)
python manage.py collectstatic
```

### Other Useful Commands
```bash
# Check for issues
python manage.py check

# Create admin user programmatically
python manage.py createsuperuser --username admin --email admin@example.com

# Show all URLs
python manage.py show_urls  # (requires django-extensions)
```

---

## Testing API with cURL

### Test Bookings Endpoint (GET)
```bash
curl http://localhost:8000/api/bookings/
```

### Create Booking (POST)
```bash
curl -X POST http://localhost:8000/api/bookings/ \
  -H "Content-Type: application/json" \
  -d '{
    "serviceType": "general",
    "frequency": "once",
    "bedrooms": 3,
    "bathrooms": 2,
    "kitchen": 1,
    "livingDining": 1,
    "laundry": 1,
    "storey": 1,
    "selectedAddOns": {},
    "addOnDetails": {},
    "selectedDate": "2026-01-15",
    "firstName": "John",
    "lastName": "Doe",
    "email": "john@example.com",
    "phone": "0412345678",
    "smsReminders": true,
    "street": "123 Main St",
    "suburb": "Sydney",
    "postcode": "2000",
    "priceDetails": {
      "total": 158
    }
  }'
```

### Test Blog Endpoint (GET)
```bash
curl http://localhost:8000/api/blog/
```

### Get Featured Blog Posts
```bash
curl http://localhost:8000/api/blog/featured/
```

### Get Statistics
```bash
curl http://localhost:8000/api/bookings/statistics/
```

---

## Python Virtual Environment

### Activate
```bash
source venv/bin/activate  # Mac/Linux
# or
venv\Scripts\activate  # Windows
```

### Deactivate
```bash
deactivate
```

### Install Packages
```bash
pip install -r requirements.txt
```

### Update Requirements
```bash
pip freeze > requirements.txt
```

---

## Port Management

### Check what's running on port 8000
```bash
lsof -ti:8000
```

### Kill process on port 8000
```bash
lsof -ti:8000 | xargs kill -9
```

### Run on different port
```bash
python manage.py runserver 8001
```

---

## Git Commands (Optional)

### Initialize Git
```bash
git init
git add .
git commit -m "Initial Django backend setup"
```

### Create .gitignore
Already created! See `.gitignore` file.

---

## Production Deployment Checklist

### Before Deploying:
```bash
# 1. Set environment variables
export SECRET_KEY='your-secret-key'
export DEBUG='False'
export ALLOWED_HOSTS='yourdomain.com,www.yourdomain.com'

# 2. Collect static files
python manage.py collectstatic --noinput

# 3. Run migrations
python manage.py migrate

# 4. Create superuser
python manage.py createsuperuser

# 5. Test the setup
python manage.py check --deploy
```

### Production Settings to Update:
- `SECRET_KEY` - Generate new secure key
- `DEBUG = False`
- `ALLOWED_HOSTS = ['yourdomain.com']`
- `CORS_ALLOWED_ORIGINS = ['https://yourdomain.com']`
- Database → PostgreSQL/MySQL
- Static files → AWS S3 or CDN
- Media files → AWS S3 or cloud storage

---

## Useful API Queries

### Filter bookings by status
```bash
curl "http://localhost:8000/api/bookings/?status=pending"
```

### Search bookings
```bash
curl "http://localhost:8000/api/bookings/?search=john"
```

### Get bookings for specific date
```bash
curl "http://localhost:8000/api/bookings/?selected_date=2026-01-15"
```

### Pagination
```bash
curl "http://localhost:8000/api/bookings/?page=2"
```

### Multiple filters
```bash
curl "http://localhost:8000/api/bookings/?status=pending&service_type=general&ordering=-created_at"
```

### Blog filters
```bash
# Get posts by category
curl "http://localhost:8000/api/blog/?category=Cleaning%20Tips"

# Get featured posts
curl "http://localhost:8000/api/blog/?featured=true"

# Search blog posts
curl "http://localhost:8000/api/blog/?search=eco-friendly"
```

---

## Backup & Restore

### Backup Database (SQLite)
```bash
cp db.sqlite3 db.sqlite3.backup
```

### Backup with timestamp
```bash
cp db.sqlite3 "db.sqlite3.backup.$(date +%Y%m%d_%H%M%S)"
```

### Restore Database
```bash
cp db.sqlite3.backup db.sqlite3
```

### Export Data (JSON)
```bash
# Export all data
python manage.py dumpdata > backup.json

# Export specific app
python manage.py dumpdata leads > leads_backup.json
python manage.py dumpdata blog > blog_backup.json
```

### Import Data
```bash
python manage.py loaddata backup.json
```

---

## Troubleshooting Commands

### Clear all migrations and start fresh
```bash
# WARNING: This deletes all data!
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc"  -delete
rm db.sqlite3
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

### Check Django version
```bash
python -m django --version
```

### Check installed packages
```bash
pip list
```

### Update pip
```bash
pip install --upgrade pip
```

### Run Django tests
```bash
python manage.py test
```

### Validate models
```bash
python manage.py validate  # Django < 1.9
python manage.py check      # Django >= 1.9
```

---

## Development Tips

### Auto-reload when files change
Django dev server auto-reloads by default. Just save your files!

### View SQL queries
```python
# In Django shell
from django.db import connection
print(connection.queries)
```

### Create sample data quickly
```python
# In Django shell
from leads.models import Booking
from datetime import date

for i in range(10):
    Booking.objects.create(
        service_type='general',
        frequency='once',
        bedrooms=3,
        bathrooms=2,
        selected_date=date.today(),
        first_name=f'Test{i}',
        last_name='User',
        email=f'test{i}@example.com',
        phone='0412345678',
        street='123 Main St',
        suburb='Sydney',
        postcode='2000',
    )
```

---

## Quick URLs Reference

- **API Root**: http://localhost:8000/api/
- **Admin Panel**: http://localhost:8000/admin/
- **Bookings API**: http://localhost:8000/api/bookings/
- **Blog API**: http://localhost:8000/api/blog/
- **Statistics**: http://localhost:8000/api/bookings/statistics/
- **Featured Posts**: http://localhost:8000/api/blog/featured/

---

## Support

For detailed documentation, see:
- `API_DOCUMENTATION.md` - Complete API reference
- `FRONTEND_INTEGRATION.md` - Next.js integration guide
- `README.md` - Setup instructions
- `SETUP_COMPLETE.md` - Overview of what was created

