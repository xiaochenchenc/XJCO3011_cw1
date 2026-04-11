# API Documentation

## Base URL

`/api/`

## Endpoints

### List Employees

- URL: `GET /api/employees/`
- Description: Returns all employee records.
- Response Example:

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
- Request Body:

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

- Response: `201 Created`

### Retrieve Employee

- URL: `GET /api/employees/{id}/`
- Description: Get details of a single employee by record ID.

### Update Employee

- URL: `PUT /api/employees/{id}/`
- Description: Replace employee record.

### Partial Update Employee

- URL: `PATCH /api/employees/{id}/`
- Description: Update one or more fields.

### Delete Employee

- URL: `DELETE /api/employees/{id}/`
- Description: Remove an employee record.

### Search Employees

- URL: `GET /api/employees/search/?query={text}`
- Description: Search employees by first name, last name, department, position, or email.
- Response: Array of matching employees.

### Department Statistics

- URL: `GET /api/employees/stats/`
- Description: Returns counts of employees by department.
- Response Example:

```json
{
  "department_counts": [
    {"department": "Engineering", "total": 3},
    {"department": "Sales", "total": 2}
  ]
}
```
