# Rapido Ride-Sharing API

A Django REST Framework-based API for a ride-sharing platform that enables users to request rides, accept ride requests (as drivers), and manage ride statuses.

## Features

- 👥 User Management
  - User registration and authentication
  - User profiles with driver/rider roles
  - JWT (JSON Web Token) authentication
  - Secure token refresh mechanism

- 🚗 Ride Management
  - Create ride requests
  - Accept ride requests (drivers)
  - Ride status management
  - Ride history tracking


## Tech Stack

- Python 3.12
- Django 5.2
- Django REST Framework
- Django REST Framework Simple JWT
- SQLite (Development)
- CORS support for frontend integration

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
- `POST /api/token/` - Obtain JWT access & refresh tokens
- `POST /api/token/refresh/` - Refresh access token
- `POST /api/token/verify/` - Verify token validity

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
2. Use the authentication flow:
   - Register a new user using the Register endpoint
   - Get JWT tokens using the login endpoint
   - The access token will be automatically used for subsequent requests
   - Use the refresh token endpoint when the access token expires

The collection is configured to use JWT authentication automatically. The access token is stored in the `access_token` collection variable and is included in the Authorization header as `Bearer <token>` for all requests.

## Models

### User Profile
- User information
- Driver/Rider status
- Current location
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

## Usage Examples

### Authentication Flow

```http
# 1. Register a new user
POST /api/users/register/
Content-Type: application/json

{
    "username": "user1",
    "password": "secure123",
    "email": "user1@example.com",
    "first_name": "John",
    "last_name": "Doe"
}

# 2. Get JWT tokens
POST /api/token/
Content-Type: application/json

{
    "username": "user1",
    "password": "secure123"
}

# Response will include access and refresh tokens
```

### Managing Driver Status

```http
# Toggle driver status
POST /api/profiles/toggle_driver_status/
Authorization: Bearer <access_token>

# Update location
POST /api/profiles/update_location/
Authorization: Bearer <access_token>
Content-Type: application/json

{
    "latitude": 12.9716,
    "longitude": 77.5946,
    "address": "Current Location"
}
```

### Ride Management Flow

```http
# 1. Create a ride request (as rider)
POST /api/rides/
Authorization: Bearer <rider_token>
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

# 2. Accept the ride (as driver)
POST /api/rides/{ride_id}/accept_ride/
Authorization: Bearer <driver_token>

# 3. Start the ride
POST /api/rides/{ride_id}/start_ride/
Authorization: Bearer <driver_token>

# 4. Complete the ride
POST /api/rides/{ride_id}/complete_ride/
Authorization: Bearer <driver_token>
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
