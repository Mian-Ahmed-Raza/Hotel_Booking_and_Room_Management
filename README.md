# Hotel Booking and Room Management System

A desktop application for managing hotel bookings, room availability, and customer management built with Python and Tkinter.

## Features

- **User Authentication**: Secure login and registration with password hashing (SHA-256)
- **Admin Dashboard**: Centralized management interface
- **Room Management**: Track room availability and bookings (placeholder)
- **Check-in/Check-out**: Manage guest check-ins and check-outs (placeholder)
- **Billing System**: Generate and manage bills (placeholder)
- **Feedback & Reviews**: Collect and manage customer feedback (placeholder)

## Prerequisites

- Python 3.7+
- MySQL Server 5.7+

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Hotel_Booking_and_Room_Management
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up the database**
   - Create a MySQL database:
     ```sql
     CREATE DATABASE hotel_db;
     ```
   - Copy `.env.example` to `.env` and configure your database credentials:
     ```
     DB_HOST=localhost
     DB_USER=root
     DB_PASS=your_password
     DB_NAME=hotel_db
     ```

4. **Run the application**
   ```bash
   python -m app.main
   ```
   
   The application will automatically create necessary database tables on first run.

## Project Structure

```
Hotel_Booking_and_Room_Management/
├── app/
│   ├── __init__.py
│   ├── main.py              # Application entry point
│   ├── models/
│   │   └── user.py          # User model and database operations
│   ├── services/
│   │   ├── auth.py          # Authentication service
│   │   └── db.py            # Database connection management
│   ├── utils/
│   │   └── style.py         # UI styling utilities
│   └── views/
│       ├── login.py         # Login interface
│       ├── register.py      # Registration interface
│       ├── dashboard.py     # Main dashboard
│       └── billing.py       # Billing interface (placeholder)
├── tests/
│   ├── test_services/
│   └── test_views/
├── .env.example             # Example environment configuration
├── requirements.txt         # Python dependencies
└── README.md
```

## Usage

### First Time Setup
1. Run the application
2. Click "Create Account" to register a new user
3. Fill in username, full name, and password (minimum 6 characters)
4. Login with your credentials

### Default Credentials
Create your own account using the registration form. The system uses secure password hashing.

## Testing

Run the test suite:
```bash
pytest
```

Run tests with coverage:
```bash
pytest --cov=app tests/
```

## Security Features

- Password hashing using SHA-256
- Input validation on login and registration
- Secure database connection management
- Environment-based configuration

## Development

### Adding New Features
1. Create models in `app/models/`
2. Add business logic in `app/services/`
3. Design UI in `app/views/`
4. Write tests in `tests/`

### Code Style
- Follow PEP 8 guidelines
- Use descriptive variable names
- Add docstrings to functions and classes

## License

See LICENSE file for details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Write/update tests
5. Submit a pull request