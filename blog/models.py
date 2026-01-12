from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User


class BlogPost(models.Model):
    """Model to store blog posts"""
    
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    ]
    
    # Basic information
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='blog_posts')
    
    # Content
    excerpt = models.TextField(max_length=300, help_text="Short description for preview (max 300 characters)")
    content = models.TextField(help_text="Full blog post content (supports HTML)")
    featured_image = models.ImageField(upload_to='blog/images/', blank=True, null=True)
    
    # SEO
    meta_description = models.CharField(max_length=160, blank=True, help_text="SEO meta description (max 160 characters)")
    meta_keywords = models.CharField(max_length=200, blank=True, help_text="Comma-separated keywords")
    
    # Categories and tags
    category = models.CharField(max_length=100, blank=True, help_text="e.g., Cleaning Tips, Eco-Friendly, Home Care")
    tags = models.CharField(max_length=200, blank=True, help_text="Comma-separated tags")
    
    # Publishing
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    published_date = models.DateTimeField(blank=True, null=True)
    
    # Engagement metrics
    views = models.IntegerField(default=0)
    featured = models.BooleanField(default=False, help_text="Show on homepage")
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-published_date', '-created_at']
        verbose_name = 'Blog Post'
        verbose_name_plural = 'Blog Posts'
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        # Auto-generate slug from title if not provided
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            # Ensure unique slug
            while BlogPost.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        
        # Set published_date when status changes to published
        if self.status == 'published' and not self.published_date:
            from django.utils import timezone
            self.published_date = timezone.now()
        
        super().save(*args, **kwargs)
    
    def increment_views(self):
        """Increment view count"""
        self.views += 1
        self.save(update_fields=['views'])
    
    @property
    def reading_time(self):
        """Estimate reading time in minutes (average 200 words per minute)"""
        word_count = len(self.content.split())
        minutes = word_count // 200
        return max(1, minutes)  # At least 1 minute
