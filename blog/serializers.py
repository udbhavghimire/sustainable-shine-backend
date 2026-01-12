from rest_framework import serializers
from .models import BlogPost


class BlogPostSerializer(serializers.ModelSerializer):
    """Full serializer for BlogPost model"""
    
    author_name = serializers.SerializerMethodField()
    reading_time = serializers.ReadOnlyField()
    tags_list = serializers.SerializerMethodField()
    
    class Meta:
        model = BlogPost
        fields = [
            'id',
            'title',
            'slug',
            'author',
            'author_name',
            'excerpt',
            'content',
            'featured_image',
            'meta_description',
            'meta_keywords',
            'category',
            'tags',
            'tags_list',
            'status',
            'published_date',
            'views',
            'featured',
            'reading_time',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ('slug', 'views', 'created_at', 'updated_at', 'reading_time')
    
    def get_author_name(self, obj):
        """Get author's full name"""
        if obj.author:
            return f"{obj.author.first_name} {obj.author.last_name}".strip() or obj.author.username
        return "Anonymous"
    
    def get_tags_list(self, obj):
        """Convert comma-separated tags to list"""
        if obj.tags:
            return [tag.strip() for tag in obj.tags.split(',') if tag.strip()]
        return []


class BlogPostListSerializer(serializers.ModelSerializer):
    """Simplified serializer for listing blog posts"""
    
    author_name = serializers.SerializerMethodField()
    reading_time = serializers.ReadOnlyField()
    tags_list = serializers.SerializerMethodField()
    
    class Meta:
        model = BlogPost
        fields = [
            'id',
            'title',
            'slug',
            'author_name',
            'excerpt',
            'featured_image',
            'category',
            'tags_list',
            'status',
            'published_date',
            'views',
            'featured',
            'reading_time',
            'created_at',
        ]
    
    def get_author_name(self, obj):
        """Get author's full name"""
        if obj.author:
            return f"{obj.author.first_name} {obj.author.last_name}".strip() or obj.author.username
        return "Anonymous"
    
    def get_tags_list(self, obj):
        """Convert comma-separated tags to list"""
        if obj.tags:
            return [tag.strip() for tag in obj.tags.split(',') if tag.strip()]
        return []


class BlogPostCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating/updating blog posts"""
    
    class Meta:
        model = BlogPost
        fields = [
            'title',
            'author',
            'excerpt',
            'content',
            'featured_image',
            'meta_description',
            'meta_keywords',
            'category',
            'tags',
            'status',
            'featured',
        ]
    
    def validate_title(self, value):
        """Validate title is not empty"""
        if not value or not value.strip():
            raise serializers.ValidationError("Title cannot be empty.")
        return value.strip()
    
    def validate_excerpt(self, value):
        """Validate excerpt length"""
        if len(value) > 300:
            raise serializers.ValidationError("Excerpt must be 300 characters or less.")
        return value

