# API Documentation

## Base URL

`/api/`

## Authentication

This API uses Token Authentication. Include the token in the Authorization header:

```
Authorization: Token <your-token-here>
```

### Register a new user

- URL: `POST /api/auth/register/`
- Content-Type: `application/json`

Request Body:
```json
{
  "username": "your_username",
  "email": "your_email@example.com",
  "password": "your_password"
}
```

Response (201 Created):
```json
{
  "token": "your-auth-token",
  "user_id": 1,
  "email": "your_email@example.com",
  "username": "your_username",
  "message": "User created successfully"
}
```

### Login

- URL: `POST /api/auth/`
- Content-Type: `application/json`

Request Body:
```json
{
  "username": "your_username",
  "password": "your_password"
}
```

Response (200 OK):
```json
{
  "token": "your-auth-token",
  "user_id": 1,
  "email": "your_email@example.com",
  "username": "your_username"
}
```

**Note:** Most endpoints are read-only without authentication, but authentication is required for write operations (POST, PUT, DELETE).

## Endpoints

### List Employees

- URL: `GET /api/employees/`
- Description: Returns all employee records.
- Authentication: Optional (read-only)

Response Example:

```json
[
  {
    "id": 1,
    "emp_id": 1001,
    "first_name": "Alice",
    "last_name": "Zhang",
    "email": "alice.zhang@example.com",
    "department": "Engineering",
    "position": "Software Engineer",
    "hire_date": "2024-08-01",
    "salary": "58000.00",
    "created_at": "2026-04-09T00:00:00Z",
    "updated_at": "2026-04-09T00:00:00Z"
  }
]
```

### Create Employee

- URL: `POST /api/employees/`
- Description: Create a new employee record.
- Authentication: Required
- Content-Type: `application/json`

Request Body:

```json
{
  "emp_id": 1002,
  "first_name": "Bob",
  "last_name": "Smith",
  "email": "bob.smith@example.com",
  "department": "Sales",
  "position": "Account Manager",
  "hire_date": "2025-01-15",
  "salary": "45000.00"
}
```

Response: `201 Created`

### Retrieve Employee

- URL: `GET /api/employees/{id}/`
- Description: Get details of a single employee by record ID.
- Authentication: Optional (read-only)

### Update Employee

- URL: `PUT /api/employees/{id}/`
- Description: Replace employee record.
- Authentication: Required
- Content-Type: `application/json`

### Partial Update Employee

- URL: `PATCH /api/employees/{id}/`
- Description: Update one or more fields.
- Authentication: Required
- Content-Type: `application/json`

### Delete Employee

- URL: `DELETE /api/employees/{id}/`
- Description: Remove an employee record.
- Authentication: Required

### Search Employees

- URL: `GET /api/employees/search/?query={text}`
- Description: Search employees by first name, last name, department, position, or email.
- Authentication: Optional
- Response: Array of matching employees.

### Department Statistics

- URL: `GET /api/employees/stats/`
- Description: Returns counts of employees by department.
- Authentication: Optional

Response Example:

```json
{
  "department_counts": [
    {"department": "Engineering", "total": 3},
    {"department": "Sales", "total": 2}
  ]
}
```

## Error Codes

- `200 OK`: Success
- `201 Created`: Resource created
- `204 No Content`: Resource deleted
- `400 Bad Request`: Invalid request data
- `401 Unauthorized`: Authentication required
- `404 Not Found`: Resource not found
- `500 Internal Server Error`: Server error
