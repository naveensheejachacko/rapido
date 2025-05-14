# Rapido Ride-Sharing API

A Django REST Framework-based API for a ride-sharing platform that enables users to request rides, accept ride requests (as drivers), and manage ride statuses.

## Features

- 👥 User Management
  - User registration and authentication
  - User profiles with driver/rider roles
  - Token-based authentication

- 🚗 Ride Management
  - Create ride requests
  - Accept ride requests (drivers)
  - Real-time ride status updates
  - Ride history tracking

- 📍 Location Services
  - Track pickup and dropoff locations
  - Update driver's current location
  - Location-based ride matching

## Tech Stack

- Python 3.12
- Django 5.2
- Django REST Framework
- SQLite (Development)
- Token Authentication

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd rapido
```

2. Create and activate a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Apply database migrations:
```bash
python manage.py migrate
```

5. Create a superuser (admin):
```bash
python manage.py createsuperuser
```

6. Start the development server:
```bash
python manage.py runserver
```

The API will be available at `http://127.0.0.1:8000/api/`

## API Endpoints

### Authentication
- `POST /api/users/register/` - Register a new user
- `POST /api-token-auth/` - Obtain authentication token

### User Profile Management
- `GET /api/profiles/` - List user profiles
- `POST /api/profiles/toggle_driver_status/` - Toggle driver availability
- `POST /api/profiles/update_location/` - Update driver's current location

### Ride Management
- `GET /api/rides/` - List all rides
- `POST /api/rides/` - Create a new ride request
- `GET /api/rides/{id}/` - Get ride details
- `POST /api/rides/{id}/accept_ride/` - Accept a ride (drivers only)
- `POST /api/rides/{id}/start_ride/` - Start a ride
- `POST /api/rides/{id}/complete_ride/` - Complete a ride
- `POST /api/rides/{id}/cancel_ride/` - Cancel a ride
- `GET /api/rides/available_rides/` - List available rides (drivers only)

## Testing

Run the test suite:
```bash
python manage.py test
```

## Postman Collection

A Postman collection is included in the repository (`postman_collection.json`). To use it:

1. Import the collection into Postman
2. Set up environment variables:
   - `auth_token`: Your authentication token
   - `ride_id`: ID of the ride you're testing

## Models

### User Profile
- User information
- Driver/Rider status
- Current location
- Vehicle details
- Rating

### Ride
- Rider and Driver references
- Pickup and dropoff locations
- Ride status
- Timestamps

### Location
- Latitude and Longitude
- Address
- Timestamp

## Usage Guide

### 1. Creating Users and Managing Roles

#### Register a Rider
```http
POST /api/users/register/
Content-Type: application/json

{
    "username": "john_rider",
    "password": "securepass123",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe"
}
```

#### Register a Driver
1. First, register a user (same as above)
2. Get authentication token:
```http
POST /api-token-auth/
Content-Type: application/json

{
    "username": "mike_driver",
    "password": "securepass123"
}
```
Response:
```json
{
    "token": "your-auth-token"
}
```

3. Update driver status:
```http
POST /api/profiles/toggle_driver_status/
Authorization: Token your-auth-token
```

4. Update driver's current location:
```http
POST /api/profiles/update_location/
Authorization: Token your-auth-token
Content-Type: application/json

{
    "latitude": 12.9716,
    "longitude": 77.5946,
    "address": "Current Location"
}
```

### 2. Managing Rides

#### Request a Ride (as Rider)
```http
POST /api/rides/
Authorization: Token rider-auth-token
Content-Type: application/json

{
    "pickup_location": {
        "latitude": 12.9716,
        "longitude": 77.5946,
        "address": "Pickup Location"
    },
    "dropoff_location": {
        "latitude": 13.0827,
        "longitude": 77.5090,
        "address": "Dropoff Location"
    }
}
```

#### Accept a Ride (as Driver)
1. View available rides:
```http
GET /api/rides/available_rides/
Authorization: Token driver-auth-token
```

2. Accept a specific ride:
```http
POST /api/rides/{ride_id}/accept_ride/
Authorization: Token driver-auth-token
```

### 3. Complete Ride Flow
1. Driver starts the ride:
```http
POST /api/rides/{ride_id}/start_ride/
Authorization: Token driver-auth-token
```

2. Driver completes the ride:
```http
POST /api/rides/{ride_id}/complete_ride/
Authorization: Token driver-auth-token
```

### 4. Cancel Ride (if needed)
Either rider or assigned driver can cancel:
```http
POST /api/rides/{ride_id}/cancel_ride/
Authorization: Token user-auth-token
```

### Example Workflow

1. Create a rider and driver:
```bash
# Register rider
curl -X POST http://127.0.0.1:8000/api/users/register/ \
  -H "Content-Type: application/json" \
  -d '{"username":"john_rider","password":"pass123","email":"john@example.com"}'

# Register driver
curl -X POST http://127.0.0.1:8000/api/users/register/ \
  -H "Content-Type: application/json" \
  -d '{"username":"mike_driver","password":"pass123","email":"mike@example.com"}'
```

2. Get authentication tokens:
```bash
# Get rider token
curl -X POST http://127.0.0.1:8000/api-token-auth/ \
  -H "Content-Type: application/json" \
  -d '{"username":"john_rider","password":"pass123"}'

# Get driver token
curl -X POST http://127.0.0.1:8000/api-token-auth/ \
  -H "Content-Type: application/json" \
  -d '{"username":"mike_driver","password":"pass123"}'
```

3. Enable driver status:
```bash
curl -X POST http://127.0.0.1:8000/api/profiles/toggle_driver_status/ \
  -H "Authorization: Token driver-token-here"
```

4. Create a ride request (as rider):
```bash
curl -X POST http://127.0.0.1:8000/api/rides/ \
  -H "Authorization: Token rider-token-here" \
  -H "Content-Type: application/json" \
  -d '{
    "pickup_location": {
        "latitude": 12.9716,
        "longitude": 77.5946,
        "address": "Pickup Location"
    },
    "dropoff_location": {
        "latitude": 13.0827,
        "longitude": 77.5090,
        "address": "Dropoff Location"
    }
}'
```

5. Complete the ride flow (as driver):
```bash
# Accept the ride
curl -X POST http://127.0.0.1:8000/api/rides/1/accept_ride/ \
  -H "Authorization: Token driver-token-here"

# Start the ride
curl -X POST http://127.0.0.1:8000/api/rides/1/start_ride/ \
  -H "Authorization: Token driver-token-here"

# Complete the ride
curl -X POST http://127.0.0.1:8000/api/rides/1/complete_ride/ \
  -H "Authorization: Token driver-token-here"
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, please create an issue in the repository or contact the maintainers.
