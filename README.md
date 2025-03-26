# PDAM ERP System Backend

A FastAPI-based backend for PDAM ERP System that handles various modules including procurement, customer management, finance, journal entries, vendor management, operations, and employee management.

## Features

- JWT Authentication with refresh tokens
- Argon2 password hashing
- PostgreSQL database integration
- Role-based access control
- RESTful API endpoints
- Modular architecture

## Prerequisites

- Python 3.8+
- PostgreSQL
- Virtual environment (recommended)

## Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd backend_pdam_v3
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the root directory with the following content:
```env
PROJECT_NAME=PDAM ERP System
PROJECT_VERSION=1.0.0

# Database
POSTGRES_SERVER=localhost
POSTGRES_USER=your_user
POSTGRES_PASSWORD=your_password
POSTGRES_DB=pdam_erp

# Security
SECRET_KEY=your-secret-key-here  # Generate using: openssl rand -hex 32
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# CORS
ALLOWED_ORIGINS=["http://localhost:3000","http://localhost:8000"]
```

5. Initialize the database:
```bash
alembic init alembic
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

## Running the Application

1. Start the development server:
```bash
uvicorn app.main:app --reload
```

2. Access the API documentation:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API Endpoints

### Authentication
- POST `/api/v1/login` - User login
- POST `/api/v1/refresh-token` - Refresh access token

### Users
- GET `/api/v1/users/` - List all users (admin only)
- POST `/api/v1/users/` - Create new user (admin only)
- GET `/api/v1/users/me` - Get current user profile
- PUT `/api/v1/users/me` - Update current user profile
- GET `/api/v1/users/{user_id}` - Get user by ID
- PUT `/api/v1/users/{user_id}` - Update user (admin only)
- DELETE `/api/v1/users/{user_id}` - Delete user (admin only)

## Project Structure

```
.
├── app
│   ├── __init__.py
│   ├── main.py
│   ├── dependencies.py
│   ├── routers/
│   ├── crud/
│   ├── schemas/
│   ├── models/
│   ├── external_services/
│   └── utils/
├── tests/
├── requirements.txt
├── .gitignore
└── README.md
```

## Security

- JWT tokens for authentication
- Argon2 password hashing
- Role-based access control
- Environment variables for sensitive data
- CORS protection

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License

This project is licensed under the MIT License. 