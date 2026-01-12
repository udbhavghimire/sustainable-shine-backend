#!/bin/bash

# Exit on error
set -e

echo "🚀 Starting deployment..."

# Run migrations
echo "📦 Running migrations..."
python manage.py migrate --noinput

# Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput

# Create superuser if it doesn't exist
echo "👤 Creating superuser..."
python create_default_superuser.py

echo "✅ Setup complete! Starting server..."

# Start gunicorn
exec gunicorn core.wsgi:application

