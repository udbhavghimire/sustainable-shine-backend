from rest_framework import serializers
from .models import Booking


class BookingSerializer(serializers.ModelSerializer):
    """Serializer for Booking model"""
    
    full_name = serializers.ReadOnlyField()
    full_address = serializers.ReadOnlyField()
    total_price = serializers.ReadOnlyField()
    
    class Meta:
        model = Booking
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at', 'status')
    
    def validate_email(self, value):
        """Validate email format"""
        if value and '@' not in value:
            raise serializers.ValidationError("Enter a valid email address.")
        return value.lower()
    
    def validate_phone(self, value):
        """Basic phone validation"""
        if value and len(value) < 8:
            raise serializers.ValidationError("Phone number must be at least 8 digits.")
        return value


class BookingListSerializer(serializers.ModelSerializer):
    """Simplified serializer for listing bookings (admin view)"""
    
    full_name = serializers.ReadOnlyField()
    full_address = serializers.ReadOnlyField()
    total_price = serializers.ReadOnlyField()
    
    class Meta:
        model = Booking
        fields = [
            'id',
            'full_name',
            'email',
            'phone',
            'service_type',
            'frequency',
            'selected_date',
            'status',
            'total_price',
            'full_address',
            'created_at',
        ]

