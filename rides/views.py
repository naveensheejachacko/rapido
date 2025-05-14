from django.shortcuts import render
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import Ride, Location, UserProfile, RideStatus
from .serializers import (
    UserSerializer, RideSerializer, LocationSerializer, UserProfileSerializer
)
from django.db.models import Q
from math import radians, sin, cos, sqrt, atan2

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    @action(detail=False, methods=['post'], permission_classes=[permissions.AllowAny], url_path='register')
    def register(self, request):
        print("Registration endpoint hit with data:", request.data)  # Debug print
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            UserProfile.objects.create(user=user)
            return Response({
                "status": "success",
                "user": serializer.data,
                "message": "User registered successfully"
            }, status=status.HTTP_201_CREATED)
        return Response({"status": "error", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class RideViewSet(viewsets.ModelViewSet):
    queryset = Ride.objects.all()
    serializer_class = RideSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(rider=self.request.user)

    def calculate_distance(self, lat1, lon1, lat2, lon2):
        R = 6371  # Earth's radius in kilometers

        lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
        dlat = lat2 - lat1
        dlon = lon1 - lon2

        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * atan2(sqrt(a), sqrt(1-a))
        distance = R * c

        return distance

    @action(detail=True, methods=['post'])
    def accept_ride(self, request, pk=None):
        ride = self.get_object()
        if ride.status != RideStatus.REQUESTED:
            return Response(
                {"error": "This ride cannot be accepted"},
                status=status.HTTP_400_BAD_REQUEST
            )

        profile = request.user.userprofile
        if not profile.is_driver or not profile.is_available:
            return Response(
                {"error": "You must be an available driver to accept rides"},
                status=status.HTTP_403_FORBIDDEN
            )

        ride.driver = request.user
        ride.status = RideStatus.ACCEPTED
        ride.save()
        return Response(RideSerializer(ride).data)

    @action(detail=True, methods=['post'])
    def start_ride(self, request, pk=None):
        ride = self.get_object()
        if ride.status != RideStatus.ACCEPTED or ride.driver != request.user:
            return Response(
                {"error": "Cannot start this ride"},
                status=status.HTTP_400_BAD_REQUEST
            )

        ride.status = RideStatus.IN_PROGRESS
        ride.save()
        return Response(RideSerializer(ride).data)

    @action(detail=True, methods=['post'])
    def complete_ride(self, request, pk=None):
        ride = self.get_object()
        if ride.status != RideStatus.IN_PROGRESS or ride.driver != request.user:
            return Response(
                {"error": "Cannot complete this ride"},
                status=status.HTTP_400_BAD_REQUEST
            )

        ride.status = RideStatus.COMPLETED
        ride.save()
        return Response(RideSerializer(ride).data)

    @action(detail=True, methods=['post'])
    def cancel_ride(self, request, pk=None):
        ride = self.get_object()
        if ride.status in [RideStatus.COMPLETED, RideStatus.CANCELLED]:
            return Response(
                {"error": "Cannot cancel this ride"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Allow only rider or assigned driver to cancel
        if request.user != ride.rider and request.user != ride.driver:
            return Response(
                {"error": "You cannot cancel this ride"},
                status=status.HTTP_403_FORBIDDEN
            )

        ride.status = RideStatus.CANCELLED
        ride.save()
        return Response(RideSerializer(ride).data)

    @action(detail=False, methods=['get'])
    def available_rides(self, request):
        if not request.user.userprofile.is_driver:
            return Response(
                {"error": "Only drivers can view available rides"},
                status=status.HTTP_403_FORBIDDEN
            )

        rides = Ride.objects.filter(status=RideStatus.REQUESTED)
        serializer = self.get_serializer(rides, many=True)
        return Response(serializer.data)

class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['post'])
    def toggle_driver_status(self, request):
        profile = request.user.userprofile
        # If user is not a driver, make them a driver and set availability
        if not profile.is_driver:
            profile.is_driver = True
            profile.is_available = True
        else:
            # If already a driver, just toggle availability
            profile.is_available = not profile.is_available
        profile.save()
        return Response(UserProfileSerializer(profile).data)

    @action(detail=False, methods=['post'])
    def update_location(self, request):
        profile = request.user.userprofile
        location_serializer = LocationSerializer(data=request.data)
        
        if location_serializer.is_valid():
            location = location_serializer.save()
            profile.current_location = location
            profile.save()
            return Response(UserProfileSerializer(profile).data)
        return Response(location_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
