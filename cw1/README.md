# Employee Management API

This Django project implements an employee management web platform for the XJCO3011 coursework.

## Features

- **Web Interface**: Full-featured web application for managing employees
- **REST API**: Complete CRUD operations for employee records with authentication
- **Search Functionality**: Search employees by name, department, position, or email
- **Analytics Dashboard**: Department statistics and employee counts
- **User Authentication**: Token-based authentication system
- **Admin Interface**: Django admin panel for data management
- **Responsive Design**: Bootstrap-based UI that works on all devices

## Setup

1. Create a Python virtual environment and activate it.
2. Install dependencies:

```bash
pip install django djangorestframework
```

3. Run migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

4. Create a superuser for admin access:

```bash
python manage.py createsuperuser
```

5. Run the development server:

```bash
python manage.py runserver
```

## Usage

### Web Interface

Visit `http://127.0.0.1:8000/` to access the main web application where you can:
- View all employees in a table
- Register/login to get API token in the browser
- Add new employees (requires login)
- Edit existing employees (requires login)
- Delete employees (requires login)
- Search employees
- View department statistics

### Web UI Authentication Flow

The web page includes an Authentication panel:

1. Register a new account from the **Register** form (or login with an existing account).
2. The token is saved in browser local storage automatically.
3. Write operations (create/update/delete) are enabled only after login.
4. Use **Logout** to clear the stored token.

### REST API

The API is available at `http://127.0.0.1:8000/api/` with the following endpoints:

#### Authentication Endpoints
- `POST /api/auth/register/` - Register new user
- `POST /api/auth/` - Login and get token

#### Employee Endpoints
- `GET /api/employees/` - List all employees
- `POST /api/employees/` - Create employee (requires auth)
- `GET /api/employees/{id}/` - Get employee details
- `PUT /api/employees/{id}/` - Update employee (requires auth)
- `PATCH /api/employees/{id}/` - Partial update (requires auth)
- `DELETE /api/employees/{id}/` - Delete employee (requires auth)
- `GET /api/employees/search/?query={text}` - Search employees
- `GET /api/employees/stats/` - Department statistics

### Admin Panel

Access the Django admin at `http://127.0.0.1:8000/admin/` to manage data directly.

## API Authentication

Most endpoints are read-only without authentication, but write operations require a token:

1. Register a user: `POST /api/auth/register/`
2. Login to get token: `POST /api/auth/`
3. Include token in requests: `Authorization: Token <your-token>`

For the browser UI, this token handling is automatic after successful login/register.

## API Documentation

See `docs/API_DOCUMENTATION.md` for detailed endpoint documentation with examples.

## Technical Report

See `docs/TECHNICAL_REPORT.md` for design rationale, stack decisions, testing approach, and GenAI declaration.

## Project Structure

```
cw1/
├── cw1/                    # Project settings
├── webapp/                 # Main app
│   ├── models.py          # Employee model
│   ├── views.py           # API and web views
│   ├── serializers.py     # DRF serializers
│   ├── urls.py            # URL routing
│   ├── admin.py           # Admin configuration
│   └── tests.py           # API tests
├── templates/             # HTML templates
├── static/                # CSS and JS files
├── docs/                  # Documentation
└── README.md             # This file
```
