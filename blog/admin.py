from django.contrib import admin
from .models import BlogPost


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    """Admin interface for BlogPost model"""
    
    list_display = [
        'title',
        'author',
        'category',
        'status',
        'featured',
        'views',
        'published_date',
        'created_at',
    ]
    
    list_filter = [
        'status',
        'featured',
        'category',
        'author',
        'published_date',
        'created_at',
    ]
    
    search_fields = [
        'title',
        'excerpt',
        'content',
        'tags',
        'category',
    ]
    
    prepopulated_fields = {
        'slug': ('title',)
    }
    
    readonly_fields = [
        'slug',
        'views',
        'reading_time',
        'created_at',
        'updated_at',
    ]
    
    fieldsets = (
        ('Basic Information', {
            'fields': (
                'title',
                'slug',
                'author',
                'category',
                'status',
                'featured',
            )
        }),
        ('Content', {
            'fields': (
                'excerpt',
                'content',
                'featured_image',
            )
        }),
        ('SEO', {
            'fields': (
                'meta_description',
                'meta_keywords',
                'tags',
            ),
            'classes': ('collapse',),
        }),
        ('Publishing', {
            'fields': (
                'published_date',
            ),
        }),
        ('Analytics', {
            'fields': (
                'views',
                'reading_time',
            ),
            'classes': ('collapse',),
        }),
        ('Metadata', {
            'fields': (
                'created_at',
                'updated_at',
            ),
            'classes': ('collapse',),
        }),
    )
    
    list_per_page = 25
    date_hierarchy = 'published_date'
    
    actions = ['publish_posts', 'unpublish_posts', 'mark_as_featured', 'unmark_as_featured']
    
    def publish_posts(self, request, queryset):
        """Bulk action to publish blog posts"""
        from django.utils import timezone
        
        updated = 0
        for post in queryset:
            if post.status != 'published':
                post.status = 'published'
                if not post.published_date:
                    post.published_date = timezone.now()
                post.save()
                updated += 1
        
        self.message_user(request, f'{updated} blog post(s) published.')
    publish_posts.short_description = "Publish selected posts"
    
    def unpublish_posts(self, request, queryset):
        """Bulk action to unpublish blog posts"""
        updated = queryset.update(status='draft')
        self.message_user(request, f'{updated} blog post(s) unpublished.')
    unpublish_posts.short_description = "Unpublish selected posts"
    
    def mark_as_featured(self, request, queryset):
        """Bulk action to mark posts as featured"""
        updated = queryset.update(featured=True)
        self.message_user(request, f'{updated} blog post(s) marked as featured.')
    mark_as_featured.short_description = "Mark as Featured"
    
    def unmark_as_featured(self, request, queryset):
        """Bulk action to unmark posts as featured"""
        updated = queryset.update(featured=False)
        self.message_user(request, f'{updated} blog post(s) unmarked as featured.')
    unmark_as_featured.short_description = "Unmark as Featured"
