# Technical Report

## Project Overview

This coursework implements an employee management web platform for the XJCO3011 coursework. The API supports full CRUD operations on employee data, search functionality, analytics, and includes authentication for secure write operations.

## Technology Stack and Rationale

**Backend:**
- Python 3.12
- Django 5.2 with Django REST Framework 3.14
- SQLite database

**Frontend:**
- HTML5, CSS3, JavaScript with Bootstrap 5
- AJAX calls for dynamic interactions

**Authentication:**
- Token-based authentication using Django REST Framework
- User registration and login endpoints

Django was chosen because it provides a robust, scalable framework for web development with excellent REST API support through DRF. SQLite was selected for development simplicity while being fully compatible with SQL standards.

## Data Model

The `Employee` model includes:

- `emp_id` (unique identifier)
- `first_name`, `last_name`
- `email` (unique)
- `department`, `position`
- `hire_date`, `salary`
- `created_at`, `updated_at` (auto-timestamps)

## API Design

The project exposes the following endpoints:

**Core CRUD Endpoints:**
- `GET /api/employees/` - List all employees
- `POST /api/employees/` - Create employee (authenticated)
- `GET /api/employees/{id}/` - Get employee details
- `PUT /api/employees/{id}/` - Update employee (authenticated)
- `PATCH /api/employees/{id}/` - Partial update (authenticated)
- `DELETE /api/employees/{id}/` - Delete employee (authenticated)

**Additional Features:**
- `GET /api/employees/search/?query={text}` - Search employees
- `GET /api/employees/stats/` - Department analytics
- `POST /api/auth/register/` - User registration
- `POST /api/auth/` - User login

All endpoints return JSON responses with appropriate HTTP status codes.

## Authentication System

**Token Authentication:**
- Users can register with username, email, and password
- Login returns an authentication token
- Write operations (POST, PUT, DELETE) require authentication
- Read operations are publicly accessible

**Security Features:**
- Password hashing using Django's secure hashing
- Token-based authentication for API access
- Unique constraints on email and username

## Testing Approach

**Automated Tests:**
- API endpoint testing using Django REST Framework's APITestCase
- Tests cover employee CRUD operations and search functionality
- Authentication endpoint testing

**Manual Testing:**
- Web interface functionality testing
- API responses validation with different clients
- Authentication flow testing

## Database Integration

**SQLite Database:**
- Fully SQL-compliant database
- ACID transactions support
- Foreign key constraints
- Proper indexing on unique fields

**CRUD Operations:**
- Create: INSERT with validation
- Read: SELECT with filtering and ordering
- Update: UPDATE with partial support
- Delete: DELETE with cascade handling

## Error Handling

**HTTP Status Codes:**
- 200 OK: Successful GET requests
- 201 Created: Successful POST requests
- 204 No Content: Successful DELETE requests
- 400 Bad Request: Invalid data or missing parameters
- 401 Unauthorized: Authentication required
- 404 Not Found: Resource not found

**Validation:**
- Email format validation
- Unique constraint enforcement
- Required field validation
- Data type validation

## GenAI Usage Declaration

**Tools Used:**
- GitHub Copilot for code generation and debugging
- Assisted with:
  - Django model and serializer creation
  - API view implementation
  - Authentication system setup
  - Frontend JavaScript logic
  - Error handling approaches
  - Documentation writing

**Usage Level:** Medium to High
- Code structure and patterns generation
- Authentication implementation guidance
- API design suggestions
- Testing approach recommendations

**All GenAI assistance has been reviewed, adapted, and documented.**

## Future Improvements

**Short Term:**
- Password reset functionality
- Email verification for registration
- API rate limiting
- Advanced search filters
- Employee photo uploads

**Long Term:**
- Role-based permissions
- Audit logging
- Multi-tenant support
- GraphQL API alternative
- Mobile application

## Deployment Considerations

**Local Development:**
- SQLite database
- Debug mode enabled
- Development server

**Production Deployment:**
- PostgreSQL database migration
- Environment variables for secrets
- HTTPS configuration
- Static file serving optimization
- Database connection pooling

## GenAI Declaration

This project used GitHub Copilot as a GenAI tool to assist with code generation, project structure, and documentation writing. All code and file changes were reviewed and adapted for the coursework context.

## Future Improvements

- Add authentication for protected employee endpoints
- Add pagination for large employee lists
- Add data import from CSV or external HR datasets
- Add Swagger / OpenAPI schema generation for richer API docs
