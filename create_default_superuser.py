#!/usr/bin/env python
"""
Script to create a default superuser on first deployment
Run this after migrations
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Only create if no users exist
if not User.objects.exists():
    username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
    email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@sustainableshine.com.au')
    password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'ChangeMeNow123!')
    
    User.objects.create_superuser(
        username=username,
        email=email,
        password=password
    )
    print(f'✅ Superuser created: {username}')
else:
    print('ℹ️ Superuser already exists, skipping creation')

