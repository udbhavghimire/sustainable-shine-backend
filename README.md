# Sustainable Shine Backend

A Django REST API for managing cleaning service bookings and blog posts.

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

### Installation

1. **Clone the repository** (if not already done)
```bash
cd /Users/udbhavghimire/Desktop/sustainable-shine-backend
```

2. **Create and activate virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run migrations**
```bash
python manage.py migrate
```

5. **Create a superuser** (for admin access)
```bash
python manage.py createsuperuser
```
Follow the prompts to set username, email, and password.

6. **Run the development server**
```bash
python manage.py runserver
```

The API will be available at: `http://localhost:8000/api/`

## 📚 API Endpoints

### Bookings/Leads
- `POST /api/bookings/` - Create new booking (public)
- `GET /api/bookings/` - List bookings (requires auth)
- `GET /api/bookings/{id}/` - Get booking details (requires auth)
- `PATCH /api/bookings/{id}/update_status/` - Update booking status (requires auth)
- `GET /api/bookings/statistics/` - Get booking statistics (requires auth)

### Blog Posts
- `GET /api/blog/` - List published blog posts (public)
- `POST /api/blog/` - Create blog post (requires auth)
- `GET /api/blog/{slug}/` - Get blog post details (public)
- `PUT/PATCH /api/blog/{slug}/` - Update blog post (requires auth)
- `DELETE /api/blog/{slug}/` - Delete blog post (requires auth)
- `GET /api/blog/featured/` - Get featured posts (public)
- `GET /api/blog/popular/` - Get popular posts (public)
- `GET /api/blog/recent/` - Get recent posts (public)
- `GET /api/blog/categories/` - Get all categories (public)

## 🎛️ Admin Interface

Access the Django admin panel at: `http://localhost:8000/admin/`

Use the superuser credentials you created to log in.

### Features:
- **Bookings Management**: View, filter, search, and update booking status
- **Blog Management**: Create, edit, publish, and manage blog posts
- **User Management**: Manage admin users and permissions

## 🔧 Configuration

### CORS Settings
The API is configured to accept requests from Next.js frontend running on:
- `http://localhost:3000`
- `http://127.0.0.1:3000`

To add more origins, edit `core/settings.py`:
```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "https://your-production-domain.com",
]
```

### Database
By default, the project uses SQLite. For production, consider using PostgreSQL or MySQL.

## 📁 Project Structure

```
sustainable-shine-backend/
├── core/                   # Project settings
│   ├── settings.py        # Django settings
│   ├── urls.py           # Main URL configuration
│   └── wsgi.py           # WSGI configuration
├── leads/                  # Bookings/Leads app
│   ├── models.py         # Booking model
│   ├── serializers.py    # API serializers
│   ├── views.py          # API views
│   ├── admin.py          # Admin configuration
│   └── urls.py           # App URLs
├── blog/                   # Blog app
│   ├── models.py         # BlogPost model
│   ├── serializers.py    # API serializers
│   ├── views.py          # API views
│   ├── admin.py          # Admin configuration
│   └── urls.py           # App URLs
├── media/                  # Uploaded files (blog images, etc.)
├── staticfiles/           # Static files
├── manage.py              # Django management script
├── requirements.txt       # Python dependencies
├── API_DOCUMENTATION.md   # Detailed API docs
└── README.md             # This file
```

## 🔗 Frontend Integration

### Example: Submit Booking from Next.js

Update your Next.js API route to use the Django backend:

```javascript
// In your BookingCalculator component, update the fetch URL:

const handleSubmit = async () => {
  // ... validation code ...
  
  try {
    const response = await fetch('http://localhost:8000/api/bookings/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(bookingData),
    });

    const result = await response.json();

    if (result.success) {
      setSubmitSuccess(true);
    } else {
      setSubmitError(result.error || 'Failed to submit booking');
    }
  } catch (error) {
    console.error('Submission error:', error);
    setSubmitError('An error occurred while submitting your booking');
  }
};
```

### Example: Fetch Blog Posts

```javascript
// Fetch blog posts for your blog page
const fetchBlogPosts = async () => {
  try {
    const response = await fetch('http://localhost:8000/api/blog/?status=published');
    const data = await response.json();
    
    return data.results;
  } catch (error) {
    console.error('Error fetching blog posts:', error);
    return [];
  }
};
```

## 📊 Database Models

### Booking Model
Stores all booking/lead information including:
- Service details (type, frequency)
- Property details (bedrooms, bathrooms, etc.)
- Customer information (name, email, phone)
- Address details
- Add-ons and pricing
- Status tracking (pending, confirmed, completed, cancelled)

### BlogPost Model
Stores blog content including:
- Title, slug, content
- Author information
- SEO metadata
- Categories and tags
- Publishing status
- View tracking
- Featured flag

## 🛠️ Development

### Run Tests
```bash
python manage.py test
```

### Make Migrations (after model changes)
```bash
python manage.py makemigrations
python manage.py migrate
```

### Create Sample Data
You can create sample bookings and blog posts through the admin interface or Django shell:
```bash
python manage.py shell
```

### Collect Static Files (for production)
```bash
python manage.py collectstatic
```

## 🔐 Security

### Important for Production:
1. Change `SECRET_KEY` in `settings.py`
2. Set `DEBUG = False`
3. Update `ALLOWED_HOSTS` with your domain
4. Use environment variables for sensitive data
5. Use HTTPS
6. Set up proper database backups
7. Configure proper CORS origins

## 📦 Dependencies

- Django 6.0.1
- Django REST Framework 3.16.1
- django-cors-headers 4.9.0
- django-filter 24.3
- Pillow 12.1.0 (for image handling)

See `requirements.txt` for complete list.

## 📝 API Documentation

For detailed API documentation including request/response examples, see [API_DOCUMENTATION.md](./API_DOCUMENTATION.md)

## 🐛 Troubleshooting

### Port already in use
```bash
# Kill the process using port 8000
lsof -ti:8000 | xargs kill -9
```

### Migration issues
```bash
# Reset migrations (development only)
python manage.py migrate --fake leads zero
python manage.py migrate --fake blog zero
python manage.py migrate
```

### CORS errors
Make sure your Next.js frontend URL is listed in `CORS_ALLOWED_ORIGINS` in `settings.py`

## 📧 Support

For issues or questions, please contact your development team.

## 📄 License

[Your License Here]

