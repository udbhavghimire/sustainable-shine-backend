# Next.js Frontend Integration Guide

## 🔗 Connecting Your Frontend to the Live API

Your backend API is now configured to accept requests from **sustainableshine.com.au**

---

## 📋 Backend Configuration (Already Done ✅)

The following has been configured on your Digital Ocean droplet:

```env
ALLOWED_HOSTS=sustainableshine.com.au,www.sustainableshine.com.au,170.64.177.253
CORS_ALLOWED_ORIGINS=https://sustainableshine.com.au,https://www.sustainableshine.com.au,http://localhost:3000
```

This allows your frontend to make API requests from:
- ✅ https://sustainableshine.com.au
- ✅ https://www.sustainableshine.com.au  
- ✅ http://localhost:3000 (for local development)

---

## 🚀 Next.js Integration

### Option 1: Environment Variables (Recommended)

#### 1. Create/Update `.env.local` in your Next.js project:

```env
# Production API
NEXT_PUBLIC_API_URL=http://170.64.177.253:8000

# API Endpoints
NEXT_PUBLIC_BLOG_API=${NEXT_PUBLIC_API_URL}/api/blog/
NEXT_PUBLIC_BOOKINGS_API=${NEXT_PUBLIC_API_URL}/api/bookings/
```

#### 2. Create an API utility file: `lib/api.js` or `utils/api.js`

```javascript
// lib/api.js
const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export const api = {
  // Base fetch wrapper
  async fetch(endpoint, options = {}) {
    const url = `${API_URL}${endpoint}`;
    
    const config = {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    };

    try {
      const response = await fetch(url, config);
      
      if (!response.ok) {
        throw new Error(`API Error: ${response.status}`);
      }
      
      return await response.json();
    } catch (error) {
      console.error('API fetch error:', error);
      throw error;
    }
  },

  // Blog endpoints
  blog: {
    // Get all blog posts
    getAll: () => api.fetch('/api/blog/'),
    
    // Get single blog post by slug
    getBySlug: (slug) => api.fetch(`/api/blog/${slug}/`),
    
    // Get featured posts
    getFeatured: () => api.fetch('/api/blog/?featured=true'),
    
    // Get posts by category
    getByCategory: (category) => api.fetch(`/api/blog/?category=${category}`),
    
    // Search posts
    search: (query) => api.fetch(`/api/blog/?search=${query}`),
  },

  // Booking/Lead endpoints
  bookings: {
    // Create a booking
    create: (data) => 
      api.fetch('/api/bookings/', {
        method: 'POST',
        body: JSON.stringify(data),
      }),
    
    // Get all bookings (if needed)
    getAll: () => api.fetch('/api/bookings/'),
  },
};

export default api;
```

#### 3. Usage Examples:

**A. Server-Side Rendering (SSR) - Recommended for SEO**

```javascript
// pages/blog/index.js
import api from '@/lib/api';

export default function BlogPage({ posts }) {
  return (
    <div>
      <h1>Blog Posts</h1>
      {posts.results.map(post => (
        <article key={post.id}>
          <h2>{post.title}</h2>
          <p>{post.excerpt}</p>
          <img src={post.featured_image} alt={post.title} />
        </article>
      ))}
    </div>
  );
}

// Fetch data on the server
export async function getServerSideProps() {
  try {
    const posts = await api.blog.getAll();
    
    return {
      props: {
        posts,
      },
    };
  } catch (error) {
    console.error('Failed to fetch posts:', error);
    return {
      props: {
        posts: { results: [] },
      },
    };
  }
}
```

**B. Static Site Generation (SSG) - Best Performance**

```javascript
// pages/blog/[slug].js
import api from '@/lib/api';

export default function BlogPost({ post }) {
  return (
    <article>
      <h1>{post.title}</h1>
      <img src={post.featured_image} alt={post.title} />
      <div dangerouslySetInnerHTML={{ __html: post.content }} />
    </article>
  );
}

// Generate static paths
export async function getStaticPaths() {
  const posts = await api.blog.getAll();
  
  const paths = posts.results.map(post => ({
    params: { slug: post.slug },
  }));

  return {
    paths,
    fallback: 'blocking', // or false
  };
}

// Generate static props
export async function getStaticProps({ params }) {
  try {
    const post = await api.blog.getBySlug(params.slug);
    
    return {
      props: {
        post,
      },
      revalidate: 60, // Revalidate every 60 seconds
    };
  } catch (error) {
    return {
      notFound: true,
    };
  }
}
```

**C. Client-Side Fetching (CSR)**

```javascript
// components/BlogList.js
import { useState, useEffect } from 'react';
import api from '@/lib/api';

export default function BlogList() {
  const [posts, setPosts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    async function fetchPosts() {
      try {
        setLoading(true);
        const data = await api.blog.getAll();
        setPosts(data.results);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    }

    fetchPosts();
  }, []);

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;

  return (
    <div>
      {posts.map(post => (
        <article key={post.id}>
          <h2>{post.title}</h2>
          <p>{post.excerpt}</p>
        </article>
      ))}
    </div>
  );
}
```

**D. Contact/Booking Form**

```javascript
// components/BookingForm.js
import { useState } from 'react';
import api from '@/lib/api';

export default function BookingForm() {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    phone: '',
    message: '',
  });
  const [status, setStatus] = useState('idle'); // idle, loading, success, error

  const handleSubmit = async (e) => {
    e.preventDefault();
    setStatus('loading');

    try {
      await api.bookings.create(formData);
      setStatus('success');
      setFormData({ name: '', email: '', phone: '', message: '' });
    } catch (error) {
      setStatus('error');
      console.error('Booking submission failed:', error);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="text"
        placeholder="Name"
        value={formData.name}
        onChange={(e) => setFormData({ ...formData, name: e.target.value })}
        required
      />
      <input
        type="email"
        placeholder="Email"
        value={formData.email}
        onChange={(e) => setFormData({ ...formData, email: e.target.value })}
        required
      />
      <input
        type="tel"
        placeholder="Phone"
        value={formData.phone}
        onChange={(e) => setFormData({ ...formData, phone: e.target.value })}
      />
      <textarea
        placeholder="Message"
        value={formData.message}
        onChange={(e) => setFormData({ ...formData, message: e.target.value })}
        required
      />
      <button type="submit" disabled={status === 'loading'}>
        {status === 'loading' ? 'Submitting...' : 'Submit'}
      </button>
      
      {status === 'success' && <p>Thank you! We'll contact you soon.</p>}
      {status === 'error' && <p>Something went wrong. Please try again.</p>}
    </form>
  );
}
```

---

## 🔧 Alternative: Using Axios

If you prefer Axios:

```bash
npm install axios
```

```javascript
// lib/api.js
import axios from 'axios';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

const axiosInstance = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const api = {
  blog: {
    getAll: () => axiosInstance.get('/api/blog/').then(res => res.data),
    getBySlug: (slug) => axiosInstance.get(`/api/blog/${slug}/`).then(res => res.data),
    getFeatured: () => axiosInstance.get('/api/blog/?featured=true').then(res => res.data),
  },
  bookings: {
    create: (data) => axiosInstance.post('/api/bookings/', data).then(res => res.data),
  },
};

export default api;
```

---

## 📍 API Endpoints Available

### Blog Posts

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/blog/` | GET | Get all blog posts (paginated) |
| `/api/blog/{slug}/` | GET | Get single post by slug |
| `/api/blog/?featured=true` | GET | Get featured posts |
| `/api/blog/?category={category}` | GET | Filter by category |
| `/api/blog/?search={query}` | GET | Search posts |

### Bookings/Leads

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/bookings/` | POST | Create new booking |
| `/api/bookings/` | GET | Get all bookings |

---

## 🌐 Testing the Integration

### 1. Test API from Browser Console:

```javascript
// Open sustainableshine.com.au in browser
// Open Developer Console (F12)
// Run this:

fetch('http://170.64.177.253:8000/api/blog/')
  .then(res => res.json())
  .then(data => console.log(data))
  .catch(err => console.error(err));
```

### 2. Test API from Terminal:

```bash
curl -X GET "http://170.64.177.253:8000/api/blog/" \
  -H "Origin: https://sustainableshine.com.au"
```

---

## ⚠️ Important Notes

### 1. **Use HTTPS for Production** (Recommended Next Step)

Currently your API is on `http://170.64.177.253:8000`. For production, you should:

- Set up a subdomain like `api.sustainableshine.com.au`
- Point it to your droplet IP (170.64.177.253)
- Set up Nginx as reverse proxy
- Enable SSL with Let's Encrypt

Then your API URL would be: `https://api.sustainableshine.com.au`

### 2. **Mixed Content Warning**

If your frontend is on HTTPS (https://sustainableshine.com.au) but API is on HTTP, browsers may block requests. Solutions:

**Option A**: Set up SSL on your backend (recommended)
**Option B**: Use Next.js API routes as a proxy:

```javascript
// pages/api/blog/index.js
export default async function handler(req, res) {
  const response = await fetch('http://170.64.177.253:8000/api/blog/');
  const data = await response.json();
  res.status(200).json(data);
}
```

Then fetch from `/api/blog` instead of the direct API URL.

### 3. **Caching & Performance**

For better performance:
- Use `getStaticProps` with `revalidate` for ISR
- Implement client-side caching (SWR or React Query)
- Cache images with Next.js Image component

---

## 🎯 Recommended Setup

### For Your Vercel/Netlify Deployment:

Add these environment variables in your hosting dashboard:

```
NEXT_PUBLIC_API_URL=http://170.64.177.253:8000
```

### For Local Development:

Create `.env.local`:
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

This allows you to:
- ✅ Test with local backend during development
- ✅ Use live API in production
- ✅ Switch environments easily

---

## 🔍 Troubleshooting

### CORS Errors:
- Check browser console for exact error
- Verify origin matches exactly (https vs http, www vs non-www)
- Backend already configured for your domain

### 404 Not Found:
- Check API URL is correct
- Verify endpoint path (must start with `/api/`)

### Network Error:
- Check if backend is running: `ssh root@170.64.177.253 "ps aux | grep gunicorn"`
- Test API directly: `curl http://170.64.177.253:8000/api/blog/`

---

## 📝 Next Steps

1. ✅ Backend CORS configured
2. ⬜ Create API utility file in Next.js
3. ⬜ Update components to use live API
4. ⬜ Test on sustainableshine.com.au
5. ⬜ Set up SSL (recommended)
6. ⬜ Set up subdomain for API (optional but professional)

---

**API Base URL**: `http://170.64.177.253:8000`
**Your Domain**: `https://sustainableshine.com.au`
**Status**: ✅ CORS Enabled & Ready to Use
