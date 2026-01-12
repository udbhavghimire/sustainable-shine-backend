from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import BlogPost
from .serializers import BlogPostSerializer, BlogPostListSerializer, BlogPostCreateSerializer


class BlogPostViewSet(viewsets.ModelViewSet):
    """
    ViewSet for BlogPost management
    
    Endpoints:
    - GET /api/blog/ - List all published blog posts (public)
    - POST /api/blog/ - Create new blog post (requires authentication)
    - GET /api/blog/{slug}/ - Retrieve specific blog post
    - PUT/PATCH /api/blog/{slug}/ - Update blog post
    - DELETE /api/blog/{slug}/ - Delete blog post
    """
    
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    lookup_field = 'slug'
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    
    # Filter options
    filterset_fields = ['status', 'category', 'featured', 'author']
    
    # Search options
    search_fields = ['title', 'excerpt', 'content', 'tags', 'category']
    
    # Ordering options
    ordering_fields = ['published_date', 'created_at', 'views', 'title']
    ordering = ['-published_date']
    
    def get_serializer_class(self):
        """Use appropriate serializer based on action"""
        if self.action == 'list':
            return BlogPostListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return BlogPostCreateSerializer
        return BlogPostSerializer
    
    def get_queryset(self):
        """
        Filter queryset based on user authentication
        Public users only see published posts
        Authenticated users see all posts
        """
        queryset = BlogPost.objects.all()
        
        if not self.request.user.is_authenticated:
            # Public users only see published posts
            queryset = queryset.filter(status='published')
        
        return queryset
    
    def get_permissions(self):
        """
        Allow public read access
        Require authentication for create, update, delete
        """
        if self.action in ['list', 'retrieve']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticatedOrReadOnly]
        return [permission() for permission in permission_classes]
    
    def retrieve(self, request, *args, **kwargs):
        """Retrieve blog post and increment view count"""
        instance = self.get_object()
        
        # Increment views (only for published posts)
        if instance.status == 'published':
            instance.increment_views()
        
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    def create(self, request, *args, **kwargs):
        """Create new blog post"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Set author to current user if not provided
        if not serializer.validated_data.get('author') and request.user.is_authenticated:
            serializer.validated_data['author'] = request.user
        
        self.perform_create(serializer)
        
        headers = self.get_success_headers(serializer.data)
        return Response(
            {
                'success': True,
                'message': 'Blog post created successfully!',
                'data': serializer.data
            },
            status=status.HTTP_201_CREATED,
            headers=headers
        )
    
    @action(detail=False, methods=['get'])
    def featured(self, request):
        """Get featured blog posts"""
        featured_posts = self.get_queryset().filter(featured=True, status='published')[:5]
        serializer = BlogPostListSerializer(featured_posts, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def categories(self, request):
        """Get list of all categories with post counts"""
        from django.db.models import Count
        
        categories = (
            self.get_queryset()
            .filter(status='published')
            .values('category')
            .annotate(count=Count('category'))
            .order_by('-count')
        )
        
        return Response(categories)
    
    @action(detail=False, methods=['get'])
    def popular(self, request):
        """Get most popular blog posts (by views)"""
        popular_posts = self.get_queryset().filter(status='published').order_by('-views')[:10]
        serializer = BlogPostListSerializer(popular_posts, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def recent(self, request):
        """Get recent blog posts"""
        recent_posts = self.get_queryset().filter(status='published').order_by('-published_date')[:10]
        serializer = BlogPostListSerializer(recent_posts, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['patch'])
    def publish(self, request, slug=None):
        """Publish a blog post"""
        blog_post = self.get_object()
        blog_post.status = 'published'
        
        if not blog_post.published_date:
            from django.utils import timezone
            blog_post.published_date = timezone.now()
        
        blog_post.save()
        
        serializer = self.get_serializer(blog_post)
        return Response({
            'success': True,
            'message': 'Blog post published successfully!',
            'data': serializer.data
        })
    
    @action(detail=True, methods=['patch'])
    def unpublish(self, request, slug=None):
        """Unpublish a blog post"""
        blog_post = self.get_object()
        blog_post.status = 'draft'
        blog_post.save()
        
        serializer = self.get_serializer(blog_post)
        return Response({
            'success': True,
            'message': 'Blog post unpublished successfully!',
            'data': serializer.data
        })
