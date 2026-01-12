# Sustainable Shine Backend API Documentation

## Overview
This Django REST API provides endpoints for managing cleaning service bookings (leads) and blog posts.

## Base URL
- **Development**: `http://localhost:8000/api/`

---

## 🔑 Authentication
Most endpoints are public for reading. Admin operations require authentication via Django session authentication.

---

## 📋 Bookings/Leads API

### Create Booking (POST)
**Endpoint**: `POST /api/bookings/`

**Access**: Public (no authentication required)

**Request Body**:
```json
{
  "serviceType": "general",
  "frequency": "weekly",
  "bedrooms": 3,
  "bathrooms": 2,
  "kitchen": 1,
  "livingDining": 1,
  "laundry": 1,
  "storey": 2,
  "selectedAddOns": {
    "carpetSteam": true,
    "insideFridge": true
  },
  "addOnDetails": {
    "carpetSteam": {
      "name": "Carpet Steam Clean",
      "price": 60,
      "quantity": 2,
      "totalPrice": 120
    }
  },
  "selectedDate": "2026-01-15",
  "firstName": "John",
  "lastName": "Doe",
  "email": "john@example.com",
  "phone": "0412345678",
  "smsReminders": true,
  "unitNumber": "5",
  "street": "123 Main Street",
  "suburb": "Sydney",
  "postcode": "2000",
  "hasPet": "yes",
  "hearAboutUs": "google",
  "specialNotes": "Please call before arriving",
  "cleanlinessLevel": "2",
  "parking": "driveway",
  "flexibleDateTime": "yes",
  "access": "home",
  "priceDetails": {
    "base": 158,
    "addOns": 25,
    "addOnsExtra": 120,
    "subtotal": 275.45,
    "gst": 27.55,
    "total": 303
  }
}
```

**Response** (201 Created):
```json
{
  "success": true,
  "message": "Booking request received successfully!",
  "data": {
    "id": 1,
    "service_type": "general",
    "frequency": "weekly",
    "full_name": "John Doe",
    "email": "john@example.com",
    ...
  }
}
```

---

### List All Bookings (GET)
**Endpoint**: `GET /api/bookings/`

**Access**: Requires authentication (admin only)

**Query Parameters**:
- `service_type` - Filter by service type (general, deep, endOfLease, moveIn)
- `frequency` - Filter by frequency (once, weekly, fortnightly, monthly)
- `status` - Filter by status (pending, confirmed, completed, cancelled)
- `selected_date` - Filter by date
- `search` - Search in name, email, phone, suburb, postcode
- `ordering` - Order by fields (created_at, selected_date, status)
- `page` - Page number for pagination

**Example**:
```
GET /api/bookings/?status=pending&search=john&ordering=-created_at&page=1
```

**Response** (200 OK):
```json
{
  "count": 25,
  "next": "http://localhost:8000/api/bookings/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "full_name": "John Doe",
      "email": "john@example.com",
      "phone": "0412345678",
      "service_type": "general",
      "frequency": "weekly",
      "selected_date": "2026-01-15",
      "status": "pending",
      "total_price": 303,
      "full_address": "5, 123 Main Street, Sydney, 2000",
      "created_at": "2026-01-11T10:30:00Z"
    }
  ]
}
```

---

### Get Single Booking (GET)
**Endpoint**: `GET /api/bookings/{id}/`

**Access**: Requires authentication

**Response** (200 OK):
```json
{
  "id": 1,
  "service_type": "general",
  "frequency": "weekly",
  "bedrooms": 3,
  "bathrooms": 2,
  "full_name": "John Doe",
  "full_address": "5, 123 Main Street, Sydney, 2000",
  "total_price": 303,
  ...
}
```

---

### Update Booking Status (PATCH)
**Endpoint**: `PATCH /api/bookings/{id}/update_status/`

**Access**: Requires authentication

**Request Body**:
```json
{
  "status": "confirmed"
}
```

**Response** (200 OK):
```json
{
  "success": true,
  "message": "Booking status updated to confirmed",
  "data": { ... }
}
```

---

### Get Booking Statistics (GET)
**Endpoint**: `GET /api/bookings/statistics/`

**Access**: Requires authentication

**Response** (200 OK):
```json
{
  "total_bookings": 150,
  "status_breakdown": {
    "pending": 45,
    "confirmed": 60,
    "completed": 40,
    "cancelled": 5
  },
  "service_breakdown": {
    "general": 80,
    "deep": 40,
    "endOfLease": 20,
    "moveIn": 10
  },
  "recent_bookings_30_days": 35
}
```

---

## 📝 Blog API

### List Published Blog Posts (GET)
**Endpoint**: `GET /api/blog/`

**Access**: Public

**Query Parameters**:
- `status` - Filter by status (draft, published, archived) [authenticated only]
- `category` - Filter by category
- `featured` - Filter featured posts (true/false)
- `search` - Search in title, excerpt, content, tags
- `ordering` - Order by fields (published_date, created_at, views, title)
- `page` - Page number for pagination

**Example**:
```
GET /api/blog/?featured=true&category=Cleaning%20Tips&ordering=-views
```

**Response** (200 OK):
```json
{
  "count": 10,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "title": "10 Eco-Friendly Cleaning Tips",
      "slug": "10-eco-friendly-cleaning-tips",
      "author_name": "Jane Smith",
      "excerpt": "Learn how to clean your home sustainably...",
      "featured_image": "/media/blog/images/cleaning-tips.jpg",
      "category": "Cleaning Tips",
      "tags_list": ["eco-friendly", "tips", "sustainable"],
      "status": "published",
      "published_date": "2026-01-10T09:00:00Z",
      "views": 245,
      "featured": true,
      "reading_time": 5,
      "created_at": "2026-01-09T15:30:00Z"
    }
  ]
}
```

---

### Get Single Blog Post (GET)
**Endpoint**: `GET /api/blog/{slug}/`

**Access**: Public (for published posts)

**Response** (200 OK):
```json
{
  "id": 1,
  "title": "10 Eco-Friendly Cleaning Tips",
  "slug": "10-eco-friendly-cleaning-tips",
  "author": 1,
  "author_name": "Jane Smith",
  "excerpt": "Learn how to clean your home sustainably...",
  "content": "<p>Full blog post content here...</p>",
  "featured_image": "/media/blog/images/cleaning-tips.jpg",
  "meta_description": "Discover 10 eco-friendly cleaning tips...",
  "meta_keywords": "eco-friendly, cleaning, sustainable, tips",
  "category": "Cleaning Tips",
  "tags": "eco-friendly, tips, sustainable",
  "tags_list": ["eco-friendly", "tips", "sustainable"],
  "status": "published",
  "published_date": "2026-01-10T09:00:00Z",
  "views": 246,
  "featured": true,
  "reading_time": 5,
  "created_at": "2026-01-09T15:30:00Z",
  "updated_at": "2026-01-11T08:00:00Z"
}
```

Note: Views are automatically incremented when a published post is retrieved.

---

### Create Blog Post (POST)
**Endpoint**: `POST /api/blog/`

**Access**: Requires authentication

**Request Body**:
```json
{
  "title": "New Cleaning Guide",
  "excerpt": "A comprehensive guide to...",
  "content": "<p>Full content here...</p>",
  "category": "Guides",
  "tags": "guide, cleaning, tips",
  "meta_description": "Learn about...",
  "meta_keywords": "cleaning, guide",
  "status": "draft",
  "featured": false
}
```

Note: `author` is automatically set to the authenticated user. `slug` is auto-generated from the title.

**Response** (201 Created):
```json
{
  "success": true,
  "message": "Blog post created successfully!",
  "data": { ... }
}
```

---

### Update Blog Post (PUT/PATCH)
**Endpoint**: `PUT /api/blog/{slug}/` or `PATCH /api/blog/{slug}/`

**Access**: Requires authentication

**Request Body**: Same as create, but all fields optional for PATCH

---

### Delete Blog Post (DELETE)
**Endpoint**: `DELETE /api/blog/{slug}/`

**Access**: Requires authentication

**Response** (204 No Content)

---

### Get Featured Posts (GET)
**Endpoint**: `GET /api/blog/featured/`

**Access**: Public

**Response**: Returns up to 5 featured blog posts (published only)

---

### Get Popular Posts (GET)
**Endpoint**: `GET /api/blog/popular/`

**Access**: Public

**Response**: Returns top 10 most viewed posts

---

### Get Recent Posts (GET)
**Endpoint**: `GET /api/blog/recent/`

**Access**: Public

**Response**: Returns 10 most recently published posts

---

### Get Categories (GET)
**Endpoint**: `GET /api/blog/categories/`

**Access**: Public

**Response** (200 OK):
```json
[
  {
    "category": "Cleaning Tips",
    "count": 15
  },
  {
    "category": "Eco-Friendly",
    "count": 10
  }
]
```

---

### Publish Blog Post (PATCH)
**Endpoint**: `PATCH /api/blog/{slug}/publish/`

**Access**: Requires authentication

**Response** (200 OK):
```json
{
  "success": true,
  "message": "Blog post published successfully!",
  "data": { ... }
}
```

---

### Unpublish Blog Post (PATCH)
**Endpoint**: `PATCH /api/blog/{slug}/unpublish/`

**Access**: Requires authentication

**Response** (200 OK):
```json
{
  "success": true,
  "message": "Blog post unpublished successfully!",
  "data": { ... }
}
```

---

## 🔧 Setup Instructions

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. Create Superuser (for admin access)
```bash
python manage.py createsuperuser
```

### 4. Run Development Server
```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000/api/`

### 5. Access Django Admin
Visit `http://localhost:8000/admin/` to manage bookings and blog posts via the admin interface.

---

## 🌐 Frontend Integration

### Example: Submit Booking from Next.js

```javascript
const handleSubmit = async () => {
  try {
    const response = await fetch('http://localhost:8000/api/bookings/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        serviceType: serviceType,
        frequency: frequency,
        bedrooms: bedrooms,
        bathrooms: bathrooms,
        kitchen: kitchen,
        livingDining: livingDining,
        laundry: laundry,
        storey: storey,
        selectedAddOns: selectedAddOns,
        addOnDetails: addOnDetails,
        selectedDate: selectedDate,
        firstName: firstName,
        lastName: lastName,
        email: email,
        phone: phone,
        smsReminders: smsReminders,
        unitNumber: unitNumber,
        street: street,
        suburb: suburb,
        postcode: postcode,
        hasPet: hasPet,
        hearAboutUs: hearAboutUs,
        specialNotes: specialNotes,
        cleanlinessLevel: cleanlinessLevel,
        parking: parking,
        flexibleDateTime: flexibleDateTime,
        access: access,
        priceDetails: priceDetails,
      }),
    });

    const result = await response.json();
    
    if (result.success) {
      console.log('Booking submitted successfully!');
    }
  } catch (error) {
    console.error('Error submitting booking:', error);
  }
};
```

### Example: Fetch Blog Posts

```javascript
const fetchBlogPosts = async () => {
  try {
    const response = await fetch('http://localhost:8000/api/blog/?status=published');
    const data = await response.json();
    
    console.log('Blog posts:', data.results);
  } catch (error) {
    console.error('Error fetching blog posts:', error);
  }
};
```

---

## 📊 Admin Interface Features

### Bookings Admin
- View all bookings with filtering and search
- Update booking status (pending → confirmed → completed)
- View full customer and property details
- Export booking data
- Bulk actions for status updates

### Blog Admin
- Create, edit, and delete blog posts
- Rich text content editing
- Image upload for featured images
- SEO fields (meta description, keywords)
- Publish/unpublish posts
- Mark posts as featured
- Auto-generate slugs from titles
- View analytics (views, reading time)

---

## 🔒 Security Notes

1. **CORS**: Update `CORS_ALLOWED_ORIGINS` in `settings.py` to include your production frontend URL
2. **Secret Key**: Change the `SECRET_KEY` in production
3. **Debug**: Set `DEBUG = False` in production
4. **Allowed Hosts**: Update `ALLOWED_HOSTS` for production
5. **Database**: Use PostgreSQL or MySQL in production instead of SQLite

---

## 📝 Environment Variables (Production)

Create a `.env` file:

```env
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
CORS_ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com

# Database
DB_ENGINE=django.db.backends.postgresql
DB_NAME=sustainable_shine
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=5432
```

---

## 🚀 Deployment Checklist

- [ ] Update `ALLOWED_HOSTS` in settings
- [ ] Update `CORS_ALLOWED_ORIGINS` in settings
- [ ] Set `DEBUG = False`
- [ ] Use a production database (PostgreSQL/MySQL)
- [ ] Set up static file serving
- [ ] Set up media file serving (S3, etc.)
- [ ] Configure HTTPS
- [ ] Set up environment variables
- [ ] Run `python manage.py collectstatic`
- [ ] Set up database backups
- [ ] Configure logging

---

## 📧 Support

For issues or questions, please contact your development team.

