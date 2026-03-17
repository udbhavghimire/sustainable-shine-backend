# Next.js API Proxy Solution for Mixed Content

## Problem

Your frontend is on HTTPS but backend is on HTTP, causing browsers to block requests.

---

## Solution: Next.js API Routes as Proxy

Create proxy routes in your Next.js app that forward requests to your backend.

---

## Implementation

### For Pages Router (pages/api/)

#### 1. Create `pages/api/bookings/index.js`

```javascript
// pages/api/bookings/index.js
const API_URL = process.env.BACKEND_API_URL || 'http://170.64.177.253:8000';

export default async function handler(req, res) {
  const { method, body } = req;

  try {
    const options = {
      method,
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
      },
    };

    // Add body for POST/PUT/PATCH requests
    if (method !== 'GET' && method !== 'HEAD') {
      options.body = JSON.stringify(body);
    }

    const response = await fetch(`${API_URL}/api/bookings/`, options);
    const data = await response.json();

    res.status(response.status).json(data);
  } catch (error) {
    console.error('API Proxy Error:', error);
    res.status(500).json({ error: 'Internal Server Error' });
  }
}
```

#### 2. Create `pages/api/bookings/[id].js` (for single booking)

```javascript
// pages/api/bookings/[id].js
const API_URL = process.env.BACKEND_API_URL || 'http://170.64.177.253:8000';

export default async function handler(req, res) {
  const { method, query, body } = req;
  const { id } = query;

  try {
    const options = {
      method,
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
      },
    };

    if (method !== 'GET' && method !== 'HEAD') {
      options.body = JSON.stringify(body);
    }

    const response = await fetch(`${API_URL}/api/bookings/${id}/`, options);
    const data = await response.json();

    res.status(response.status).json(data);
  } catch (error) {
    console.error('API Proxy Error:', error);
    res.status(500).json({ error: 'Internal Server Error' });
  }
}
```

#### 3. Create `pages/api/blog/index.js`

```javascript
// pages/api/blog/index.js
const API_URL = process.env.BACKEND_API_URL || 'http://170.64.177.253:8000';

export default async function handler(req, res) {
  const { method, query } = req;
  
  // Build query string
  const queryString = new URLSearchParams(query).toString();
  const url = `${API_URL}/api/blog/${queryString ? `?${queryString}` : ''}`;

  try {
    const response = await fetch(url, {
      method,
      headers: {
        'Accept': 'application/json',
      },
    });
    
    const data = await response.json();
    res.status(response.status).json(data);
  } catch (error) {
    console.error('API Proxy Error:', error);
    res.status(500).json({ error: 'Internal Server Error' });
  }
}
```

#### 4. Create `pages/api/blog/[slug].js`

```javascript
// pages/api/blog/[slug].js
const API_URL = process.env.BACKEND_API_URL || 'http://170.64.177.253:8000';

export default async function handler(req, res) {
  const { method, query } = req;
  const { slug } = query;

  try {
    const response = await fetch(`${API_URL}/api/blog/${slug}/`, {
      method,
      headers: {
        'Accept': 'application/json',
      },
    });
    
    const data = await response.json();
    res.status(response.status).json(data);
  } catch (error) {
    console.error('API Proxy Error:', error);
    res.status(500).json({ error: 'Internal Server Error' });
  }
}
```

---

### For App Router (app/api/)

#### 1. Create `app/api/bookings/route.js`

```javascript
// app/api/bookings/route.js
import { NextResponse } from 'next/server';

const API_URL = process.env.BACKEND_API_URL || 'http://170.64.177.253:8000';

export async function GET(request) {
  try {
    const response = await fetch(`${API_URL}/api/bookings/`, {
      headers: {
        'Accept': 'application/json',
      },
    });
    
    const data = await response.json();
    return NextResponse.json(data);
  } catch (error) {
    return NextResponse.json({ error: 'Internal Server Error' }, { status: 500 });
  }
}

export async function POST(request) {
  try {
    const body = await request.json();
    
    const response = await fetch(`${API_URL}/api/bookings/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
      },
      body: JSON.stringify(body),
    });
    
    const data = await response.json();
    return NextResponse.json(data, { status: response.status });
  } catch (error) {
    return NextResponse.json({ error: 'Internal Server Error' }, { status: 500 });
  }
}
```

#### 2. Create `app/api/blog/route.js`

```javascript
// app/api/blog/route.js
import { NextResponse } from 'next/server';

const API_URL = process.env.BACKEND_API_URL || 'http://170.64.177.253:8000';

export async function GET(request) {
  const { searchParams } = new URL(request.url);
  const queryString = searchParams.toString();
  const url = `${API_URL}/api/blog/${queryString ? `?${queryString}` : ''}`;

  try {
    const response = await fetch(url, {
      headers: {
        'Accept': 'application/json',
      },
    });
    
    const data = await response.json();
    return NextResponse.json(data);
  } catch (error) {
    return NextResponse.json({ error: 'Internal Server Error' }, { status: 500 });
  }
}
```

---

## Environment Variables

### Add to `.env.local` (for local development):
```env
BACKEND_API_URL=http://170.64.177.253:8000
```

### Add to Vercel/Netlify (production):
```env
BACKEND_API_URL=http://170.64.177.253:8000
```

---

## Update Your API Client

### Before (Direct API calls):
```javascript
// ❌ This gets blocked in production (mixed content)
const response = await fetch('http://170.64.177.253:8000/api/bookings/');
```

### After (Using Next.js proxy):
```javascript
// ✅ This works in production (same-origin request)
const response = await fetch('/api/bookings/');
```

---

## Updated API Utility File

```javascript
// lib/api.js
const isDevelopment = process.env.NODE_ENV === 'development';

// Use Next.js API routes (proxy) instead of direct backend URL
const API_BASE = ''; // Empty string for relative URLs

export const api = {
  // Blog endpoints
  blog: {
    getAll: async (params = {}) => {
      const queryString = new URLSearchParams(params).toString();
      const url = `/api/blog${queryString ? `?${queryString}` : ''}`;
      const res = await fetch(url);
      return res.json();
    },
    
    getBySlug: async (slug) => {
      const res = await fetch(`/api/blog/${slug}`);
      return res.json();
    },
    
    getFeatured: async () => {
      return api.blog.getAll({ featured: 'true' });
    },
  },

  // Booking endpoints
  bookings: {
    getAll: async () => {
      const res = await fetch('/api/bookings/');
      return res.json();
    },
    
    getById: async (id) => {
      const res = await fetch(`/api/bookings/${id}`);
      return res.json();
    },
    
    create: async (data) => {
      const res = await fetch('/api/bookings/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      });
      return res.json();
    },
  },
};

export default api;
```

---

## Usage Examples

### Server-Side Rendering:
```javascript
// pages/bookings.js
import api from '@/lib/api';

export default function BookingsPage({ bookings }) {
  return (
    <div>
      {bookings.results.map(booking => (
        <div key={booking.id}>{booking.full_name}</div>
      ))}
    </div>
  );
}

export async function getServerSideProps() {
  const bookings = await api.bookings.getAll();
  return { props: { bookings } };
}
```

### Client-Side:
```javascript
// components/BookingForm.js
import { useState } from 'react';
import api from '@/lib/api';

export default function BookingForm() {
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    
    try {
      const result = await api.bookings.create({
        full_name: 'John Doe',
        email: 'john@example.com',
        // ... other fields
      });
      console.log('Booking created:', result);
    } catch (error) {
      console.error('Error:', error);
    } finally {
      setLoading(false);
    }
  };

  return <form onSubmit={handleSubmit}>...</form>;
}
```

---

## Benefits of This Approach

1. ✅ **Fixes Mixed Content**: All requests are now same-origin (HTTPS → HTTPS)
2. ✅ **No Backend Changes**: Your Django backend doesn't need SSL immediately
3. ✅ **Environment Flexibility**: Easy to switch backends via env variables
4. ✅ **Server-Side Requests**: SSR/SSG can still fetch data
5. ✅ **Error Handling**: Centralized error handling in proxy
6. ✅ **Security**: Backend URL not exposed to client
7. ✅ **CORS Not Needed**: Since requests are same-origin

---

## Testing

### Test locally:
```bash
# Start Next.js dev server
npm run dev

# Test endpoints
curl http://localhost:3000/api/bookings/
curl http://localhost:3000/api/blog/
```

### Test in production:
```bash
# After deploying to Vercel/Netlify
curl https://sustainableshine.com.au/api/bookings/
curl https://sustainableshine.com.au/api/blog/
```

---

## Troubleshooting

### Issue: 500 Internal Server Error
**Check:** Backend API URL is correct in environment variables

### Issue: Timeout
**Check:** Backend server is running on Digital Ocean

### Issue: CORS errors still appearing
**Check:** You're using `/api/...` not `http://170.64.177.253:8000/api/...`

---

## Long-term Solution (Recommended)

While this proxy works great, for a professional production setup:

1. Set up a subdomain: `api.sustainableshine.com.au`
2. Point it to your droplet IP
3. Install Nginx as reverse proxy
4. Set up SSL with Let's Encrypt
5. Update frontend to use `https://api.sustainableshine.com.au`

But for now, the Next.js proxy solution will work perfectly! 🎉
