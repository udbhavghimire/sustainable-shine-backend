// ============================================
// QUICK REFERENCE: API Integration
// ============================================

// 1. ADD TO YOUR NEXT.JS .env.local FILE:
// ============================================
NEXT_PUBLIC_API_URL=http://170.64.177.253:8000

// 2. CREATE lib/api.js IN YOUR NEXT.JS PROJECT:
// ============================================
const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export const api = {
  blog: {
    getAll: async () => {
      const res = await fetch(`${API_URL}/api/blog/`);
      return res.json();
    },
    getBySlug: async (slug) => {
      const res = await fetch(`${API_URL}/api/blog/${slug}/`);
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

// 3. USE IN YOUR PAGES:
// ============================================

// Server-side (SEO friendly):
import api from '@/lib/api';

export async function getServerSideProps() {
  const posts = await api.blog.getAll();
  return { props: { posts } };
}

// Client-side:
import { useEffect, useState } from 'react';
import api from '@/lib/api';

function BlogPage() {
  const [posts, setPosts] = useState([]);
  
  useEffect(() => {
    api.blog.getAll().then(data => setPosts(data.results));
  }, []);
  
  return <div>{/* render posts */}</div>;
}

// 4. AVAILABLE ENDPOINTS:
// ============================================
GET  http://170.64.177.253:8000/api/blog/           // All posts
GET  http://170.64.177.253:8000/api/blog/{slug}/    // Single post
GET  http://170.64.177.253:8000/api/blog/?featured=true
POST http://170.64.177.253:8000/api/bookings/       // Create booking

// 5. EXAMPLE POST DATA FOR BOOKINGS:
// ============================================
{
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "0412345678",
  "message": "I need cleaning services"
}

// 6. RESPONSE STRUCTURE:
// ============================================
{
  "count": 4,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 10,
      "title": "How to clean a house fast",
      "slug": "how-to-clean-a-house-fast",
      "excerpt": "Quick cleaning tips...",
      "featured_image": "https://res.cloudinary.com/...",
      "category": "cleaning-tips",
      "published_date": "2026-03-10T09:56:17.874957Z",
      "featured": true,
      "reading_time": 3
    }
  ]
}
