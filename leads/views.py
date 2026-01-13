from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Booking
from .serializers import BookingSerializer


class BookingViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Booking/Lead management
    
    Endpoints:
    - GET /api/bookings/ - List all bookings with full details (requires authentication for admin)
    - POST /api/bookings/ - Create new booking (public)
    - GET /api/bookings/{id}/ - Retrieve specific booking
    - GET /api/bookings/{id}/detailed/ - Get detailed structured booking information
    - PATCH /api/bookings/{id}/update_status/ - Update booking status
    - GET /api/bookings/statistics/ - Get booking statistics
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
        """Use full serializer with all details"""
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
        try:
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
        except Exception as e:
            # Log the error for debugging
            import traceback
            error_detail = {
                'success': False,
                'message': 'Failed to create booking',
                'error': str(e),
                'traceback': traceback.format_exc()
            }
            print("Booking creation error:", error_detail)  # This will appear in server logs
            
            # Return user-friendly error
            return Response(
                {
                    'success': False,
                    'message': 'Failed to create booking',
                    'error': str(e)
                },
                status=status.HTTP_400_BAD_REQUEST
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
    
    @action(detail=True, methods=['get'])
    def detailed(self, request, pk=None):
        """Get detailed booking information in a structured format"""
        booking = self.get_object()
        
        # Get human-readable labels
        service_type_label = dict(Booking.SERVICE_TYPES).get(booking.service_type, booking.service_type)
        frequency_label = dict(Booking.FREQUENCY_CHOICES).get(booking.frequency, booking.frequency)
        has_pet_label = dict(Booking.HAS_PET_CHOICES).get(booking.has_pet, booking.has_pet) if booking.has_pet else 'N/A'
        cleanliness_label = dict(Booking.CLEANLINESS_CHOICES).get(booking.cleanliness_level, booking.cleanliness_level) if booking.cleanliness_level else 'N/A'
        parking_label = dict(Booking.PARKING_CHOICES).get(booking.parking, booking.parking) if booking.parking else 'N/A'
        access_label = dict(Booking.ACCESS_CHOICES).get(booking.access, booking.access) if booking.access else 'N/A'
        flexible_label = dict(Booking.FLEXIBLE_CHOICES).get(booking.flexible_date_time, booking.flexible_date_time) if booking.flexible_date_time else 'N/A'
        hear_about_label = dict(Booking.HEAR_ABOUT_US_CHOICES).get(booking.hear_about_us, booking.hear_about_us) if booking.hear_about_us else 'N/A'
        
        # Structure the response
        detailed_data = {
            'id': booking.id,
            'status': booking.status,
            'service_details': {
                'service_type': service_type_label,
                'frequency': frequency_label,
                'preferred_date': booking.selected_date,
            },
            'customer_information': {
                'name': booking.full_name,
                'first_name': booking.first_name,
                'last_name': booking.last_name,
                'email': booking.email,
                'phone': booking.phone,
                'sms_reminders': booking.sms_reminders,
            },
            'property_details': {
                'address': booking.full_address,
                'unit_number': booking.unit_number,
                'street': booking.street,
                'suburb': booking.suburb,
                'postcode': booking.postcode,
                'bedrooms': booking.bedrooms,
                'bathrooms': booking.bathrooms,
                'storeys': booking.storey,
                'laundries': booking.laundry,
                'kitchen': booking.kitchen,
                'living_dining': booking.living_dining,
            },
            'additional_information': {
                'has_pet': has_pet_label,
                'cleanliness_level': cleanliness_label,
                'parking': parking_label,
                'access': access_label,
                'flexible_date_time': flexible_label,
                'hear_about_us': hear_about_label,
                'special_notes': booking.special_notes or '',
            },
            'add_ons': {
                'selected': booking.selected_add_ons,
                'details': booking.add_on_details,
            },
            'pricing_details': booking.price_details,
            'metadata': {
                'created_at': booking.created_at,
                'updated_at': booking.updated_at,
            }
        }
        
        return Response({
            'success': True,
            'data': detailed_data
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
