# Frontend Integration Guide

## Setting Up Your Next.js Frontend to Work with Django Backend

### 1. Update Your Next.js API Route (if you have one)

If you're currently using `/app/api/send-booking/route.js` in your Next.js app, you can either:

**Option A: Remove it and call Django directly** (Recommended)
**Option B: Keep it as a proxy to Django backend**

### Option A: Direct API Calls (Recommended)

Update your `BookingCalculator.jsx` component to call Django directly:

#### Step 1: Update the handleSubmit function

Replace the current API call in your `BookingCalculator.jsx`:

```javascript
// OLD CODE (remove this)
const response = await fetch("/api/send-booking", {
  method: "POST",
  ...
});

// NEW CODE (use this instead)
const response = await fetch("http://localhost:8000/api/bookings/", {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
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
```

#### Step 2: Update the response handling

The Django backend returns a structured response:

```javascript
const result = await response.json();

if (result.success) {
  setSubmitSuccess(true);
  // Optionally: redirect or show success message
} else {
  setSubmitError(result.error || "Failed to submit booking. Please try again.");
}
```

### Complete Updated handleSubmit Function

```javascript
const handleSubmit = async () => {
  // Reset previous states
  setSubmitError("");
  setSubmitSuccess(false);

  // Validate form
  if (!validateForm()) {
    window.scrollTo({ top: 0, behavior: "smooth" });
    return;
  }

  setIsSubmitting(true);

  try {
    // Prepare add-on details for submission
    const addOnDetails = {};
    Object.keys(selectedAddOns).forEach((key) => {
      if (selectedAddOns[key]) {
        const addOn = addOnsData.find((a) => a.id === key);
        if (addOn) {
          const quantity = addOnQuantities[key] || 1;
          addOnDetails[key] = {
            name: addOn.name,
            price: addOn.price,
            quantity: quantity,
            totalPrice: addOn.price * quantity,
          };
        }
      }
    });

    // Send to Django backend
    const response = await fetch("http://localhost:8000/api/bookings/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
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

    if (response.ok && result.success) {
      setSubmitSuccess(true);
      window.scrollTo({ top: 0, behavior: "smooth" });
    } else {
      setSubmitError(
        result.message || result.error || "Failed to submit booking. Please try again."
      );
      window.scrollTo({ top: 0, behavior: "smooth" });
    }
  } catch (error) {
    console.error("Submission error:", error);
    setSubmitError(
      "An error occurred while submitting your booking. Please try again."
    );
    window.scrollTo({ top: 0, behavior: "smooth" });
  } finally {
    setIsSubmitting(false);
  }
};
```

---

## 2. Creating a Blog Page in Next.js

### Create a Blog List Page

Create `/app/blog/page.jsx`:

```javascript
"use client";

import { useState, useEffect } from "react";
import Link from "next/link";

export default function BlogPage() {
  const [posts, setPosts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    fetchBlogPosts();
  }, []);

  const fetchBlogPosts = async () => {
    try {
      const response = await fetch(
        "http://localhost:8000/api/blog/?status=published&ordering=-published_date"
      );
      const data = await response.json();
      setPosts(data.results || []);
    } catch (error) {
      console.error("Error fetching blog posts:", error);
      setError("Failed to load blog posts");
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-xl">Loading blog posts...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-xl text-red-600">{error}</div>
      </div>
    );
  }

  return (
    <section className="min-h-screen bg-gradient-to-br from-emerald-50 via-white to-blue-50 py-20">
      <div className="container mx-auto px-4 max-w-6xl">
        <div className="text-center mb-12">
          <h1 className="text-4xl md:text-5xl font-bold text-gray-900 mb-4">
            Our Blog
          </h1>
          <p className="text-xl text-gray-600">
            Tips, guides, and insights for a cleaner, greener home
          </p>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
          {posts.map((post) => (
            <Link key={post.id} href={`/blog/${post.slug}`}>
              <div className="bg-white rounded-2xl shadow-lg overflow-hidden hover:shadow-xl transition-shadow duration-300 cursor-pointer h-full">
                {post.featured_image && (
                  <img
                    src={`http://localhost:8000${post.featured_image}`}
                    alt={post.title}
                    className="w-full h-48 object-cover"
                  />
                )}
                <div className="p-6">
                  {post.category && (
                    <span className="text-sm text-emerald-600 font-semibold">
                      {post.category}
                    </span>
                  )}
                  <h2 className="text-xl font-bold text-gray-900 mt-2 mb-3">
                    {post.title}
                  </h2>
                  <p className="text-gray-600 mb-4 line-clamp-3">
                    {post.excerpt}
                  </p>
                  <div className="flex items-center justify-between text-sm text-gray-500">
                    <span>{post.author_name}</span>
                    <span>{post.reading_time} min read</span>
                  </div>
                  <div className="mt-2 text-sm text-gray-400">
                    {new Date(post.published_date).toLocaleDateString()}
                  </div>
                </div>
              </div>
            </Link>
          ))}
        </div>

        {posts.length === 0 && (
          <div className="text-center py-20">
            <p className="text-xl text-gray-600">No blog posts yet. Check back soon!</p>
          </div>
        )}
      </div>
    </section>
  );
}
```

### Create a Single Blog Post Page

Create `/app/blog/[slug]/page.jsx`:

```javascript
"use client";

import { useState, useEffect } from "react";
import { useParams, useRouter } from "next/navigation";
import Link from "next/link";

export default function BlogPostPage() {
  const params = useParams();
  const router = useRouter();
  const [post, setPost] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    if (params.slug) {
      fetchBlogPost(params.slug);
    }
  }, [params.slug]);

  const fetchBlogPost = async (slug) => {
    try {
      const response = await fetch(`http://localhost:8000/api/blog/${slug}/`);
      
      if (!response.ok) {
        throw new Error("Blog post not found");
      }
      
      const data = await response.json();
      setPost(data);
    } catch (error) {
      console.error("Error fetching blog post:", error);
      setError("Blog post not found");
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-xl">Loading...</div>
      </div>
    );
  }

  if (error || !post) {
    return (
      <div className="min-h-screen flex items-center justify-center flex-col">
        <div className="text-xl text-red-600 mb-4">{error}</div>
        <Link href="/blog" className="text-emerald-600 hover:underline">
          ← Back to Blog
        </Link>
      </div>
    );
  }

  return (
    <article className="min-h-screen bg-gradient-to-br from-emerald-50 via-white to-blue-50 py-20">
      <div className="container mx-auto px-4 max-w-4xl">
        <Link href="/blog" className="text-emerald-600 hover:underline mb-6 inline-block">
          ← Back to Blog
        </Link>

        <div className="bg-white rounded-2xl shadow-lg p-8 md:p-12">
          {post.featured_image && (
            <img
              src={`http://localhost:8000${post.featured_image}`}
              alt={post.title}
              className="w-full h-64 md:h-96 object-cover rounded-xl mb-8"
            />
          )}

          {post.category && (
            <span className="text-sm text-emerald-600 font-semibold">
              {post.category}
            </span>
          )}

          <h1 className="text-4xl md:text-5xl font-bold text-gray-900 mt-4 mb-6">
            {post.title}
          </h1>

          <div className="flex items-center justify-between text-gray-600 mb-8 pb-8 border-b">
            <div className="flex items-center space-x-4">
              <span className="font-semibold">{post.author_name}</span>
              <span>•</span>
              <span>{new Date(post.published_date).toLocaleDateString()}</span>
              <span>•</span>
              <span>{post.reading_time} min read</span>
            </div>
            <div className="text-sm text-gray-500">{post.views} views</div>
          </div>

          {/* Blog content - renders HTML */}
          <div 
            className="prose prose-lg max-w-none"
            dangerouslySetInnerHTML={{ __html: post.content }}
          />

          {/* Tags */}
          {post.tags_list && post.tags_list.length > 0 && (
            <div className="mt-12 pt-8 border-t">
              <div className="flex flex-wrap gap-2">
                {post.tags_list.map((tag, index) => (
                  <span
                    key={index}
                    className="bg-emerald-100 text-emerald-700 px-3 py-1 rounded-full text-sm"
                  >
                    #{tag}
                  </span>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </article>
  );
}
```

---

## 3. Environment Variables (Production)

For production, use environment variables instead of hardcoded URLs.

Create `.env.local` in your Next.js project:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api
```

For production:
```env
NEXT_PUBLIC_API_URL=https://api.yourdomain.com/api
```

Then update your API calls:

```javascript
const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api";

// Use in your fetch calls
const response = await fetch(`${API_URL}/bookings/`, {
  method: "POST",
  ...
});
```

---

## 4. Testing the Integration

1. **Start Django backend**:
```bash
cd /Users/udbhavghimire/Desktop/sustainable-shine-backend
source venv/bin/activate
python manage.py runserver
```

2. **Start Next.js frontend**:
```bash
cd /path/to/your/nextjs-app
npm run dev
```

3. **Test booking submission**:
   - Navigate to your booking calculator page
   - Fill out the form
   - Submit and check if it appears in Django admin

4. **Test blog**:
   - Create a blog post in Django admin (http://localhost:8000/admin)
   - Mark it as "Published"
   - Navigate to `/blog` in your Next.js app
   - You should see the blog post

---

## 5. Admin Access for Managing Leads

To view and manage leads (bookings) from your frontend admin:

### Create API endpoints for authenticated admin users

You can create admin pages in your Next.js app that:
1. Require authentication (use NextAuth.js or similar)
2. Fetch bookings from `/api/bookings/` endpoint
3. Display them in a table/dashboard
4. Allow status updates via `/api/bookings/{id}/update_status/`

Example admin dashboard component coming in next file...

---

## Need Help?

If you encounter any issues:
1. Check Django server is running on port 8000
2. Check Next.js app is running on port 3000
3. Check CORS settings in Django `settings.py`
4. Check browser console for errors
5. Check Django server logs for API errors

