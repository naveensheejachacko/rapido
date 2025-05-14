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
