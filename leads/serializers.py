from rest_framework import serializers
from .models import Booking
import json


class BookingSerializer(serializers.ModelSerializer):
    """Serializer for Booking model"""
    
    full_name = serializers.ReadOnlyField()
    full_address = serializers.ReadOnlyField()
    total_price = serializers.ReadOnlyField()
    
    # Allow these JSON fields to accept both dict and string (will be parsed)
    selected_add_ons = serializers.JSONField(required=False, default=dict)
    add_on_details = serializers.JSONField(required=False, default=dict)
    price_details = serializers.JSONField(required=False, default=dict)
    
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
    
    def validate_selected_add_ons(self, value):
        """Ensure selected_add_ons is a dict"""
        if value is None or value == '':
            return {}
        if isinstance(value, str):
            try:
                return json.loads(value) or {}
            except json.JSONDecodeError:
                raise serializers.ValidationError("Invalid JSON format for selected_add_ons")
        return value if value else {}
    
    def validate_add_on_details(self, value):
        """Ensure add_on_details is a dict"""
        if value is None or value == '':
            return {}
        if isinstance(value, str):
            try:
                return json.loads(value) or {}
            except json.JSONDecodeError:
                raise serializers.ValidationError("Invalid JSON format for add_on_details")
        return value if value else {}
    
    def validate_price_details(self, value):
        """Ensure price_details is a dict"""
        if value is None or value == '':
            return {}
        if isinstance(value, str):
            try:
                return json.loads(value) or {}
            except json.JSONDecodeError:
                raise serializers.ValidationError("Invalid JSON format for price_details")
        return value if value else {}
    
    def validate(self, data):
        """Ensure all JSON fields have default values if not provided"""
        if 'selected_add_ons' not in data or data.get('selected_add_ons') is None:
            data['selected_add_ons'] = {}
        if 'add_on_details' not in data or data.get('add_on_details') is None:
            data['add_on_details'] = {}
        if 'price_details' not in data or data.get('price_details') is None:
            data['price_details'] = {}
        return data


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

