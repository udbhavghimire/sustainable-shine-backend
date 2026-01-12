from django.contrib import admin
from .models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    """Admin interface for Booking model"""
    
    list_display = [
        'id',
        'full_name',
        'email',
        'phone',
        'service_type',
        'frequency',
        'selected_date',
        'status',
        'total_price',
        'created_at',
    ]
    
    list_filter = [
        'service_type',
        'frequency',
        'status',
        'selected_date',
        'has_pet',
        'created_at',
    ]
    
    search_fields = [
        'first_name',
        'last_name',
        'email',
        'phone',
        'street',
        'suburb',
        'postcode',
    ]
    
    readonly_fields = [
        'created_at',
        'updated_at',
        'full_name',
        'full_address',
        'total_price',
    ]
    
    fieldsets = (
        ('Service Information', {
            'fields': (
                'service_type',
                'frequency',
                'selected_date',
                'status',
            )
        }),
        ('Property Details', {
            'fields': (
                'bedrooms',
                'bathrooms',
                'kitchen',
                'living_dining',
                'laundry',
                'storey',
            )
        }),
        ('Add-ons', {
            'fields': (
                'selected_add_ons',
                'add_on_details',
            ),
            'classes': ('collapse',),
        }),
        ('Customer Details', {
            'fields': (
                'first_name',
                'last_name',
                'full_name',
                'email',
                'phone',
                'sms_reminders',
            )
        }),
        ('Address', {
            'fields': (
                'unit_number',
                'street',
                'suburb',
                'postcode',
                'full_address',
            )
        }),
        ('Additional Information', {
            'fields': (
                'has_pet',
                'hear_about_us',
                'special_notes',
                'cleanliness_level',
                'parking',
                'flexible_date_time',
                'access',
            ),
            'classes': ('collapse',),
        }),
        ('Price Details', {
            'fields': (
                'price_details',
                'total_price',
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
    date_hierarchy = 'created_at'
    
    actions = ['mark_as_confirmed', 'mark_as_completed', 'mark_as_cancelled']
    
    def mark_as_confirmed(self, request, queryset):
        """Bulk action to mark bookings as confirmed"""
        updated = queryset.update(status='confirmed')
        self.message_user(request, f'{updated} booking(s) marked as confirmed.')
    mark_as_confirmed.short_description = "Mark selected as Confirmed"
    
    def mark_as_completed(self, request, queryset):
        """Bulk action to mark bookings as completed"""
        updated = queryset.update(status='completed')
        self.message_user(request, f'{updated} booking(s) marked as completed.')
    mark_as_completed.short_description = "Mark selected as Completed"
    
    def mark_as_cancelled(self, request, queryset):
        """Bulk action to mark bookings as cancelled"""
        updated = queryset.update(status='cancelled')
        self.message_user(request, f'{updated} booking(s) marked as cancelled.')
    mark_as_cancelled.short_description = "Mark selected as Cancelled"
