from django.contrib import admin
from .models import Ride, Location, UserProfile

@admin.register(Ride)
class RideAdmin(admin.ModelAdmin):
    list_display = ('id', 'rider', 'driver', 'status', 'created_at', 'updated_at')
    list_filter = ('status', 'created_at')
    search_fields = ('rider__username', 'driver__username')

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('id', 'address', 'latitude', 'longitude', 'created_at')
    search_fields = ('address',)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_driver', 'is_available', 'rating')
    list_filter = ('is_driver', 'is_available')
    search_fields = ('user__username', 'vehicle_number')
