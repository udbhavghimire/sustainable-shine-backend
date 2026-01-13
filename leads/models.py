from django.db import models
from django.utils import timezone


class Booking(models.Model):
    """Model to store booking/lead information from the frontend calculator"""
    
    # Service details
    SERVICE_TYPES = [
        ('general', 'General Cleaning'),
        ('deep', 'Deep Cleaning'),
        ('endOfLease', 'End of Lease'),
        ('moveIn', 'Move-in Cleaning'),
    ]
    
    FREQUENCY_CHOICES = [
        ('once', 'Just Once'),
        ('weekly', 'Weekly'),
        ('fortnightly', 'Fortnightly'),
        ('monthly', 'Monthly'),
    ]
    
    service_type = models.CharField(max_length=20, choices=SERVICE_TYPES)
    frequency = models.CharField(max_length=20, choices=FREQUENCY_CHOICES, default='once')
    
    # Property details
    bedrooms = models.IntegerField(default=1)
    bathrooms = models.IntegerField(default=1)
    kitchen = models.IntegerField(default=1)
    living_dining = models.IntegerField(default=1)
    laundry = models.IntegerField(default=0)
    storey = models.IntegerField(default=1)
    
    # Add-ons (stored as JSON)
    selected_add_ons = models.JSONField(default=dict, blank=True, null=True)
    add_on_details = models.JSONField(default=dict, blank=True, null=True)
    
    # Booking date
    selected_date = models.DateField()
    
    # Customer details
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    sms_reminders = models.BooleanField(default=True)
    
    # Address details
    unit_number = models.CharField(max_length=50, blank=True)
    street = models.CharField(max_length=200)
    suburb = models.CharField(max_length=100)
    postcode = models.CharField(max_length=10)
    
    # Additional information
    HAS_PET_CHOICES = [
        ('yes', 'Yes'),
        ('no', 'No'),
    ]
    
    HEAR_ABOUT_US_CHOICES = [
        ('google', 'Google Search'),
        ('facebook', 'Facebook'),
        ('instagram', 'Instagram'),
        ('friend', 'Friend/Family Referral'),
        ('flyer', 'Flyer'),
        ('other', 'Other'),
    ]
    
    has_pet = models.CharField(max_length=10, choices=HAS_PET_CHOICES, blank=True)
    hear_about_us = models.CharField(max_length=50, choices=HEAR_ABOUT_US_CHOICES, blank=True)
    special_notes = models.TextField(blank=True)
    
    # Access & other information
    CLEANLINESS_CHOICES = [
        ('1', '1 - Very Clean'),
        ('2', '2 - Moderately Clean'),
        ('3', '3 - Needs Cleaning'),
        ('4', '4 - Heavily Soiled'),
    ]
    
    PARKING_CHOICES = [
        ('driveway', 'Driveway'),
        ('street', 'Street Parking'),
        ('garage', 'Garage'),
        ('visitor', 'Visitor Parking'),
        ('other', 'Other'),
    ]
    
    ACCESS_CHOICES = [
        ('home', 'I will be home'),
        ('key', 'Leave a key'),
        ('lockbox', 'Lockbox'),
        ('doorcode', 'Door code'),
        ('other', 'Other'),
    ]
    
    FLEXIBLE_CHOICES = [
        ('yes', 'Yes'),
        ('no', 'No'),
    ]
    
    cleanliness_level = models.CharField(max_length=10, choices=CLEANLINESS_CHOICES, blank=True)
    parking = models.CharField(max_length=20, choices=PARKING_CHOICES, blank=True)
    flexible_date_time = models.CharField(max_length=10, choices=FLEXIBLE_CHOICES, blank=True)
    access = models.CharField(max_length=20, choices=ACCESS_CHOICES, blank=True)
    
    # Price details (stored as JSON)
    price_details = models.JSONField(default=dict, blank=True, null=True)
    
    # Status tracking
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Booking'
        verbose_name_plural = 'Bookings'
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.service_type} ({self.selected_date})"
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def full_address(self):
        address_parts = []
        if self.unit_number:
            address_parts.append(self.unit_number)
        address_parts.extend([self.street, self.suburb, self.postcode])
        return ", ".join(address_parts)
    
    @property
    def total_price(self):
        if isinstance(self.price_details, dict) and 'total' in self.price_details:
            return self.price_details['total']
        return 0
