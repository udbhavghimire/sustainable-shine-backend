# Edit & Delete Functionality Guide

## Overview

Your Django API already supports full CRUD (Create, Read, Update, Delete) operations for both Bookings and Blog Posts! Here's how to use them.

---

## 🔧 Bookings/Leads - Edit & Delete

### Update Booking (PATCH - Partial Update)

**Endpoint**: `PATCH /api/bookings/{id}/`

**Example - Update Status:**

```bash
curl -X PATCH http://localhost:8000/api/bookings/1/ \
  -H "Content-Type: application/json" \
  -d '{
    "status": "confirmed"
  }'
```

**Example - Update Multiple Fields:**

```bash
curl -X PATCH http://localhost:8000/api/bookings/1/ \
  -H "Content-Type: application/json" \
  -d '{
    "status": "confirmed",
    "phone": "0412345679",
    "special_notes": "Updated notes"
  }'
```

### Update Booking (PUT - Full Update)

**Endpoint**: `PUT /api/bookings/{id}/`

**Note**: PUT requires ALL fields to be sent. Use PATCH for partial updates instead.

### Delete Booking

**Endpoint**: `DELETE /api/bookings/{id}/`

**Example:**

```bash
curl -X DELETE http://localhost:8000/api/bookings/1/
```

---

## 📝 Blog Posts - Edit & Delete

### Update Blog Post (PATCH - Partial Update)

**Endpoint**: `PATCH /api/blog/{slug}/`

**Example - Update Title:**

```bash
curl -X PATCH http://localhost:8000/api/blog/my-blog-post/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Updated Title"
  }'
```

**Example - Publish a Draft:**

```bash
curl -X PATCH http://localhost:8000/api/blog/my-blog-post/ \
  -H "Content-Type: application/json" \
  -d '{
    "status": "published"
  }'
```

**Example - Update Content:**

```bash
curl -X PATCH http://localhost:8000/api/blog/my-blog-post/ \
  -H "Content-Type: application/json" \
  -d '{
    "content": "<p>Updated content here...</p>",
    "excerpt": "Updated excerpt"
  }'
```

### Delete Blog Post

**Endpoint**: `DELETE /api/blog/{slug}/`

**Example:**

```bash
curl -X DELETE http://localhost:8000/api/blog/my-blog-post/
```

---

## 🎨 Next.js Frontend Examples

### Example: Edit Booking Component

Create `/app/admin/bookings/edit/[id]/page.jsx`:

```javascript
"use client";

import { useState, useEffect } from "react";
import { useParams, useRouter } from "next/navigation";

export default function EditBookingPage() {
  const params = useParams();
  const router = useRouter();
  const [booking, setBooking] = useState(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);

  // Form states
  const [status, setStatus] = useState("");
  const [phone, setPhone] = useState("");
  const [email, setEmail] = useState("");
  const [specialNotes, setSpecialNotes] = useState("");

  useEffect(() => {
    fetchBooking();
  }, []);

  const fetchBooking = async () => {
    try {
      const response = await fetch(
        `http://localhost:8000/api/bookings/${params.id}/`,
        {
          credentials: "include",
        }
      );

      if (response.ok) {
        const data = await response.json();
        setBooking(data);
        setStatus(data.status);
        setPhone(data.phone);
        setEmail(data.email);
        setSpecialNotes(data.special_notes || "");
      }
    } catch (error) {
      console.error("Error fetching booking:", error);
    } finally {
      setLoading(false);
    }
  };

  const handleUpdate = async (e) => {
    e.preventDefault();
    setSaving(true);

    try {
      const response = await fetch(
        `http://localhost:8000/api/bookings/${params.id}/`,
        {
          method: "PATCH",
          headers: {
            "Content-Type": "application/json",
          },
          credentials: "include",
          body: JSON.stringify({
            status: status,
            phone: phone,
            email: email,
            special_notes: specialNotes,
          }),
        }
      );

      if (response.ok) {
        alert("Booking updated successfully!");
        router.push("/admin/bookings");
      } else {
        alert("Failed to update booking");
      }
    } catch (error) {
      console.error("Error updating booking:", error);
      alert("An error occurred while updating");
    } finally {
      setSaving(false);
    }
  };

  const handleDelete = async () => {
    if (!confirm("Are you sure you want to delete this booking?")) {
      return;
    }

    try {
      const response = await fetch(
        `http://localhost:8000/api/bookings/${params.id}/`,
        {
          method: "DELETE",
          credentials: "include",
        }
      );

      if (response.ok) {
        alert("Booking deleted successfully!");
        router.push("/admin/bookings");
      } else {
        alert("Failed to delete booking");
      }
    } catch (error) {
      console.error("Error deleting booking:", error);
      alert("An error occurred while deleting");
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-xl">Loading...</div>
      </div>
    );
  }

  if (!booking) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-xl text-red-600">Booking not found</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="max-w-4xl mx-auto">
        <div className="bg-white rounded-lg shadow p-8">
          <div className="flex justify-between items-center mb-6">
            <h1 className="text-3xl font-bold">Edit Booking #{booking.id}</h1>
            <button
              onClick={handleDelete}
              className="bg-red-600 text-white px-4 py-2 rounded-lg hover:bg-red-700"
            >
              Delete Booking
            </button>
          </div>

          <form onSubmit={handleUpdate} className="space-y-6">
            {/* Customer Info (Read-only) */}
            <div>
              <h2 className="text-xl font-semibold mb-4">
                Customer Information
              </h2>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Name
                  </label>
                  <input
                    type="text"
                    value={booking.full_name}
                    disabled
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg bg-gray-100"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Service
                  </label>
                  <input
                    type="text"
                    value={booking.service_type}
                    disabled
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg bg-gray-100"
                  />
                </div>
              </div>
            </div>

            {/* Editable Fields */}
            <div>
              <h2 className="text-xl font-semibold mb-4">Update Details</h2>

              {/* Status */}
              <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Status
                </label>
                <select
                  value={status}
                  onChange={(e) => setStatus(e.target.value)}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emerald-500"
                >
                  <option value="pending">Pending</option>
                  <option value="confirmed">Confirmed</option>
                  <option value="completed">Completed</option>
                  <option value="cancelled">Cancelled</option>
                </select>
              </div>

              {/* Phone */}
              <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Phone
                </label>
                <input
                  type="tel"
                  value={phone}
                  onChange={(e) => setPhone(e.target.value)}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emerald-500"
                />
              </div>

              {/* Email */}
              <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Email
                </label>
                <input
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emerald-500"
                />
              </div>

              {/* Special Notes */}
              <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Special Notes
                </label>
                <textarea
                  value={specialNotes}
                  onChange={(e) => setSpecialNotes(e.target.value)}
                  rows={4}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emerald-500"
                />
              </div>
            </div>

            {/* Buttons */}
            <div className="flex space-x-4">
              <button
                type="submit"
                disabled={saving}
                className="bg-emerald-600 text-white px-6 py-2 rounded-lg hover:bg-emerald-700 disabled:opacity-50"
              >
                {saving ? "Saving..." : "Save Changes"}
              </button>
              <button
                type="button"
                onClick={() => router.push("/admin/bookings")}
                className="bg-gray-200 text-gray-700 px-6 py-2 rounded-lg hover:bg-gray-300"
              >
                Cancel
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}
```

---

### Example: Edit Blog Post Component

Create `/app/admin/blog/edit/[slug]/page.jsx`:

```javascript
"use client";

import { useState, useEffect } from "react";
import { useParams, useRouter } from "next/navigation";

export default function EditBlogPostPage() {
  const params = useParams();
  const router = useRouter();
  const [post, setPost] = useState(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);

  // Form states
  const [title, setTitle] = useState("");
  const [excerpt, setExcerpt] = useState("");
  const [content, setContent] = useState("");
  const [category, setCategory] = useState("");
  const [tags, setTags] = useState("");
  const [status, setStatus] = useState("draft");
  const [featured, setFeatured] = useState(false);

  useEffect(() => {
    fetchPost();
  }, []);

  const fetchPost = async () => {
    try {
      const response = await fetch(
        `http://localhost:8000/api/blog/${params.slug}/`,
        {
          credentials: "include",
        }
      );

      if (response.ok) {
        const data = await response.json();
        setPost(data);
        setTitle(data.title);
        setExcerpt(data.excerpt);
        setContent(data.content);
        setCategory(data.category || "");
        setTags(data.tags || "");
        setStatus(data.status);
        setFeatured(data.featured);
      }
    } catch (error) {
      console.error("Error fetching post:", error);
    } finally {
      setLoading(false);
    }
  };

  const handleUpdate = async (e) => {
    e.preventDefault();
    setSaving(true);

    try {
      const response = await fetch(
        `http://localhost:8000/api/blog/${params.slug}/`,
        {
          method: "PATCH",
          headers: {
            "Content-Type": "application/json",
          },
          credentials: "include",
          body: JSON.stringify({
            title: title,
            excerpt: excerpt,
            content: content,
            category: category,
            tags: tags,
            status: status,
            featured: featured,
          }),
        }
      );

      if (response.ok) {
        alert("Blog post updated successfully!");
        router.push("/admin/blog");
      } else {
        const error = await response.json();
        alert(`Failed to update: ${JSON.stringify(error)}`);
      }
    } catch (error) {
      console.error("Error updating post:", error);
      alert("An error occurred while updating");
    } finally {
      setSaving(false);
    }
  };

  const handleDelete = async () => {
    if (!confirm("Are you sure you want to delete this blog post?")) {
      return;
    }

    try {
      const response = await fetch(
        `http://localhost:8000/api/blog/${params.slug}/`,
        {
          method: "DELETE",
          credentials: "include",
        }
      );

      if (response.ok) {
        alert("Blog post deleted successfully!");
        router.push("/admin/blog");
      } else {
        alert("Failed to delete blog post");
      }
    } catch (error) {
      console.error("Error deleting post:", error);
      alert("An error occurred while deleting");
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-xl">Loading...</div>
      </div>
    );
  }

  if (!post) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-xl text-red-600">Blog post not found</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="max-w-4xl mx-auto">
        <div className="bg-white rounded-lg shadow p-8">
          <div className="flex justify-between items-center mb-6">
            <h1 className="text-3xl font-bold">Edit Blog Post</h1>
            <button
              onClick={handleDelete}
              className="bg-red-600 text-white px-4 py-2 rounded-lg hover:bg-red-700"
            >
              Delete Post
            </button>
          </div>

          <form onSubmit={handleUpdate} className="space-y-6">
            {/* Title */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Title *
              </label>
              <input
                type="text"
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                required
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emerald-500"
              />
            </div>

            {/* Excerpt */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Excerpt * (max 300 characters)
              </label>
              <textarea
                value={excerpt}
                onChange={(e) => setExcerpt(e.target.value)}
                required
                maxLength={300}
                rows={3}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emerald-500"
              />
              <div className="text-sm text-gray-500 mt-1">
                {excerpt.length}/300 characters
              </div>
            </div>

            {/* Content */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Content * (HTML supported)
              </label>
              <textarea
                value={content}
                onChange={(e) => setContent(e.target.value)}
                required
                rows={12}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emerald-500 font-mono text-sm"
              />
            </div>

            {/* Category and Tags */}
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Category
                </label>
                <input
                  type="text"
                  value={category}
                  onChange={(e) => setCategory(e.target.value)}
                  placeholder="e.g., Cleaning Tips"
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emerald-500"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Tags (comma-separated)
                </label>
                <input
                  type="text"
                  value={tags}
                  onChange={(e) => setTags(e.target.value)}
                  placeholder="eco-friendly, tips, guide"
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emerald-500"
                />
              </div>
            </div>

            {/* Status and Featured */}
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Status
                </label>
                <select
                  value={status}
                  onChange={(e) => setStatus(e.target.value)}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emerald-500"
                >
                  <option value="draft">Draft</option>
                  <option value="published">Published</option>
                  <option value="archived">Archived</option>
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Featured
                </label>
                <div className="flex items-center h-full">
                  <input
                    type="checkbox"
                    checked={featured}
                    onChange={(e) => setFeatured(e.target.checked)}
                    className="w-5 h-5 accent-emerald-600"
                  />
                  <span className="ml-2 text-gray-700">Show on homepage</span>
                </div>
              </div>
            </div>

            {/* Buttons */}
            <div className="flex space-x-4">
              <button
                type="submit"
                disabled={saving}
                className="bg-emerald-600 text-white px-6 py-2 rounded-lg hover:bg-emerald-700 disabled:opacity-50"
              >
                {saving ? "Saving..." : "Save Changes"}
              </button>
              <button
                type="button"
                onClick={() => router.push("/admin/blog")}
                className="bg-gray-200 text-gray-700 px-6 py-2 rounded-lg hover:bg-gray-300"
              >
                Cancel
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}
```

---

## 🔐 Authentication Note

For edit and delete operations, you'll need authentication. The endpoints require:

1. **Session Authentication** (if using Django admin login)
2. **Token Authentication** (for production - you'd need to implement this)

For development, you can:

- Login to Django admin first: http://localhost:8000/admin/
- Then your API calls will work with `credentials: 'include'`

---

## 🎯 Quick Test

### Test Update Booking:

```bash
# First, create a test booking or get an existing ID from admin
# Then update it:
curl -X PATCH http://localhost:8000/api/bookings/1/ \
  -H "Content-Type: application/json" \
  -d '{"status": "confirmed"}'
```

### Test Update Blog Post:

```bash
# First, create a blog post in admin
# Then update it:
curl -X PATCH http://localhost:8000/api/blog/your-post-slug/ \
  -H "Content-Type: application/json" \
  -d '{"title": "Updated Title"}'
```

### Test Delete:

```bash
# Delete booking
curl -X DELETE http://localhost:8000/api/bookings/1/

# Delete blog post
curl -X DELETE http://localhost:8000/api/blog/your-post-slug/
```

---

## ✅ Summary

**All CRUD operations are already working!**

- ✅ Create (POST) - Already implemented
- ✅ Read (GET) - Already implemented
- ✅ **Update (PUT/PATCH) - Already working!**
- ✅ **Delete (DELETE) - Already working!**

You can use these endpoints from:

- Django Admin (manual editing)
- cURL (command line testing)
- Your Next.js frontend (see examples above)
- Any API client (Postman, Insomnia, etc.)

The examples above show you how to build edit and delete UI in your Next.js app!
