from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Booking
from .serializers import BookingSerializer, BookingListSerializer


class BookingViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Booking/Lead management
    
    Endpoints:
    - GET /api/bookings/ - List all bookings (requires authentication for admin)
    - POST /api/bookings/ - Create new booking (public)
    - GET /api/bookings/{id}/ - Retrieve specific booking
    - PUT/PATCH /api/bookings/{id}/ - Update booking
    - DELETE /api/bookings/{id}/ - Delete booking
    """
    
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    
    # Filter options
    filterset_fields = ['service_type', 'frequency', 'status', 'selected_date']
    
    # Search options
    search_fields = ['first_name', 'last_name', 'email', 'phone', 'suburb', 'postcode']
    
    # Ordering options
    ordering_fields = ['created_at', 'selected_date', 'status']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        """Use simplified serializer for list view"""
        if self.action == 'list':
            return BookingListSerializer
        return BookingSerializer
    
    def get_permissions(self):
        """
        Allow public access to create endpoint
        Require authentication for list, update, delete
        """
        if self.action == 'create':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticatedOrReadOnly]
        return [permission() for permission in permission_classes]
    
    def create(self, request, *args, **kwargs):
        """Create new booking/lead"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        headers = self.get_success_headers(serializer.data)
        return Response(
            {
                'success': True,
                'message': 'Booking request received successfully!',
                'data': serializer.data
            },
            status=status.HTTP_201_CREATED,
            headers=headers
        )
    
    @action(detail=True, methods=['patch'])
    def update_status(self, request, pk=None):
        """Update booking status"""
        booking = self.get_object()
        new_status = request.data.get('status')
        
        if new_status not in dict(Booking.STATUS_CHOICES):
            return Response(
                {'error': 'Invalid status'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        booking.status = new_status
        booking.save()
        
        serializer = self.get_serializer(booking)
        return Response({
            'success': True,
            'message': f'Booking status updated to {new_status}',
            'data': serializer.data
        })
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Get booking statistics"""
        from django.db.models import Count, Q
        from datetime import datetime, timedelta
        
        # Total bookings
        total = self.queryset.count()
        
        # Status breakdown
        status_counts = dict(
            self.queryset.values('status')
            .annotate(count=Count('status'))
            .values_list('status', 'count')
        )
        
        # Service type breakdown
        service_counts = dict(
            self.queryset.values('service_type')
            .annotate(count=Count('service_type'))
            .values_list('service_type', 'count')
        )
        
        # Recent bookings (last 30 days)
        thirty_days_ago = datetime.now() - timedelta(days=30)
        recent_count = self.queryset.filter(created_at__gte=thirty_days_ago).count()
        
        return Response({
            'total_bookings': total,
            'status_breakdown': status_counts,
            'service_breakdown': service_counts,
            'recent_bookings_30_days': recent_count,
        })
