from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Ride, Location, UserProfile

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'first_name', 'last_name')

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ('id', 'latitude', 'longitude', 'address', 'created_at')

class RideSerializer(serializers.ModelSerializer):
    pickup_location = LocationSerializer()
    dropoff_location = LocationSerializer()
    rider = UserSerializer(read_only=True)
    driver = UserSerializer(read_only=True)

    class Meta:
        model = Ride
        fields = ('id', 'rider', 'driver', 'pickup_location', 'dropoff_location',
                 'status', 'created_at', 'updated_at')

    def create(self, validated_data):
        pickup_location_data = validated_data.pop('pickup_location')
        dropoff_location_data = validated_data.pop('dropoff_location')
        
        pickup_location = Location.objects.create(**pickup_location_data)
        dropoff_location = Location.objects.create(**dropoff_location_data)
        
        ride = Ride.objects.create(
            pickup_location=pickup_location,
            dropoff_location=dropoff_location,
            **validated_data
        )
        return ride

class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    current_location = LocationSerializer(required=False)

    class Meta:
        model = UserProfile
        fields = ('id', 'user', 'is_driver', 'is_available', 'current_location',
                 'vehicle_number', 'rating')
