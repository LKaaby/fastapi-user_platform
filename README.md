# FastAPI User Platform

A modern, secure user authentication and management platform built with FastAPI, featuring role-based access control, JWT authentication, and admin dashboard.

## Features

- **User Authentication**: Register, login, and JWT-based session management
- **Role-Based Access Control**: User and Admin roles with different permissions
- **Admin Dashboard**: Administrative interface for user management
- **Secure Password Hashing**: PBKDF2 with SHA256 for password security
- **PostgreSQL Database**: SQLAlchemy ORM with Alembic migrations
- **Jinja2 Templates**: Server-side rendered HTML pages
- **RESTful API**: Fully documented FastAPI endpoints

## Project Structure
fastapi-user-platform/
├── src/
│ ├── api/v1/ # API routes (auth, admin)
│ ├── core/ # Configuration and security
│ ├── crud/ # Database operations
│ ├── db/ # Database session and connection
│ ├── models/ # SQLAlchemy models
│ ├── schemas/ # Pydantic schemas
│ ├── templates/ # Jinja2 HTML templates
│ ├── static/ # CSS, JS, images
│ └── utils/ # Utilities and dependencies
├── migrations/ # Alembic database migrations
├── tests/ # Test suite
└── requirements.txt # Python dependencies

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/LKaaby/fastapi-user_platform.git
   cd fastapi-user_platform
2. **Create virtual environment**:
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\Activate.ps1/bat
3. **Install dependencies**:
   pip install -r requirements.txt
4. **Environment Configuration**:
   DATABASE_URL=postgresql+psycopg2://username:password@localhost:5432/user_platform
   SECRET_KEY=your-secret-key-here
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   REFRESH_TOKEN_EXPIRE_DAYS=7
   ENVIRONMENT=development
5. **Database Setup**:
   alembic upgrade head

## Key Endpoints

### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/login` - User login  
- `POST /auth/logout` - User logout
- `GET /auth/me` - Get current user

### Pages
- `GET /login` - Login page
- `GET /register` - Registration page
- `GET /dashboard` - User dashboard (protected)

### Admin
- `GET /admin/users` - List all users (admin only)
- `GET /admin/users/{id}` - Get user details (admin only)
- `PUT /admin/users/{id}` - Update user (admin only)
- `DELETE /admin/users/{id}` - Delete user (admin only)

## Running the Application
Start the development server
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
