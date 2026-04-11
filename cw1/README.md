# Employee Management API

This Django project implements an employee management web platform for the XJCO3011 coursework.

## Features

- **Web Interface**: Full-featured web application for managing employees
- **REST API**: Complete CRUD operations for employee records
- **Search Functionality**: Search employees by name, department, position, or email
- **Analytics Dashboard**: Department statistics and employee counts
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

4. Run the development server:

```bash
python manage.py runserver
```

## Usage

### Web Interface

Visit `http://127.0.0.1:8000/` to access the main web application where you can:
- View all employees in a table
- Add new employees
- Edit existing employees
- Delete employees
- Search employees
- View department statistics

### REST API

The API is available at `http://127.0.0.1:8000/api/` with the following endpoints:

- `GET /api/employees/` - List all employees
- `POST /api/employees/` - Create new employee
- `GET /api/employees/{id}/` - Get employee details
- `PUT /api/employees/{id}/` - Update employee
- `PATCH /api/employees/{id}/` - Partial update employee
- `DELETE /api/employees/{id}/` - Delete employee
- `GET /api/employees/search/?query={text}` - Search employees
- `GET /api/employees/stats/` - Department statistics

### Admin Panel

Access the Django admin at `http://127.0.0.1:8000/admin/` to manage data directly.

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
