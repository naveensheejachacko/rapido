from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Ride, Location, UserProfile, RideStatus

class UserTests(APITestCase):
    def setUp(self):
        self.user_data = {
            'username': 'testuser',
            'password': 'testpass123',
            'email': 'test@example.com'
        }

    def test_create_user(self):
        response = self.client.post('/api/users/register/', self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'testuser')

class RideTests(APITestCase):
    def setUp(self):
        # Create a rider
        self.rider = User.objects.create_user(username='rider', password='pass123')
        self.rider_profile = UserProfile.objects.create(user=self.rider)
        
        # Create a driver
        self.driver = User.objects.create_user(username='driver', password='pass123')
        self.driver_profile = UserProfile.objects.create(
            user=self.driver,
            is_driver=True,
            is_available=True
        )

        # Create locations
        self.pickup = Location.objects.create(
            latitude=12.9716,
            longitude=77.5946,
            address="Pickup Location"
        )
        self.dropoff = Location.objects.create(
            latitude=13.0827,
            longitude=77.5090,
            address="Dropoff Location"
        )

        # Authenticate as rider
        self.client.force_authenticate(user=self.rider)

    def test_create_ride(self):
        data = {
            'pickup_location': {
                'latitude': 12.9716,
                'longitude': 77.5946,
                'address': "Test Pickup"
            },
            'dropoff_location': {
                'latitude': 13.0827,
                'longitude': 77.5090,
                'address': "Test Dropoff"
            }
        }
        
        response = self.client.post('/api/rides/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Ride.objects.count(), 1)
        self.assertEqual(Ride.objects.get().status, RideStatus.REQUESTED)

    def test_ride_flow(self):
        # Create a ride
        ride = Ride.objects.create(
            rider=self.rider,
            pickup_location=self.pickup,
            dropoff_location=self.dropoff
        )

        # Driver accepts ride
        self.client.force_authenticate(user=self.driver)
        response = self.client.post(f'/api/rides/{ride.id}/accept_ride/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        ride.refresh_from_db()
        self.assertEqual(ride.status, RideStatus.ACCEPTED)

        # Start ride
        response = self.client.post(f'/api/rides/{ride.id}/start_ride/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        ride.refresh_from_db()
        self.assertEqual(ride.status, RideStatus.IN_PROGRESS)

        # Complete ride
        response = self.client.post(f'/api/rides/{ride.id}/complete_ride/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        ride.refresh_from_db()
        self.assertEqual(ride.status, RideStatus.COMPLETED)
