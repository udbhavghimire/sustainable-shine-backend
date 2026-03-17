// ============================================
// QUICK FIX: Mixed Content Problem
// ============================================

// THE PROBLEM:
// ❌ https://sustainableshine.com.au → http://170.64.177.253:8000
//    (HTTPS site trying to call HTTP API = BLOCKED!)

// THE SOLUTION:
// ✅ https://sustainableshine.com.au → /api/bookings/ (same origin)
//    Next.js proxy → http://170.64.177.253:8000 (server-side, allowed)

// ============================================
// STEP 1: Create pages/api/bookings/index.js
// ============================================

const API_URL = 'http://170.64.177.253:8000';

export default async function handler(req, res) {
  const { method, body } = req;

  const options = {
    method,
    headers: {
      'Content-Type': 'application/json',
      'Accept': 'application/json',
    },
  };

  if (method !== 'GET') {
    options.body = JSON.stringify(body);
  }

  const response = await fetch(`${API_URL}/api/bookings/`, options);
  const data = await response.json();

  res.status(response.status).json(data);
}

// ============================================
// STEP 2: Create pages/api/blog/index.js
// ============================================

const API_URL = 'http://170.64.177.253:8000';

export default async function handler(req, res) {
  const response = await fetch(`${API_URL}/api/blog/`);
  const data = await response.json();
  res.status(response.status).json(data);
}

// ============================================
// STEP 3: Update Your Components
// ============================================

// BEFORE (doesn't work in production):
const response = await fetch('http://170.64.177.253:8000/api/bookings/');

// AFTER (works everywhere):
const response = await fetch('/api/bookings/');

// ============================================
// STEP 4: Update lib/api.js
// ============================================

export const api = {
  blog: {
    getAll: () => fetch('/api/blog/').then(r => r.json()),
    getBySlug: (slug) => fetch(`/api/blog/${slug}`).then(r => r.json()),
  },
  bookings: {
    getAll: () => fetch('/api/bookings/').then(r => r.json()),
    create: (data) => fetch('/api/bookings/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    }).then(r => r.json()),
  },
};

// ============================================
// DONE! Now Deploy and Test
// ============================================

// Your requests will work like this:
// Browser → /api/bookings/ (HTTPS, same-origin ✅)
// Next.js → http://170.64.177.253:8000 (server-side ✅)
