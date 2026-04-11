# Technical Report

## Project Overview

This coursework implements an employee management API using Django and Django REST Framework. The API supports full CRUD operations on employee data, search functionality, and analytic summaries by department.

## Technology Stack and Rationale

- Python 3.12
- Django 5.2
- Django REST Framework
- SQLite database

Django was chosen because the existing project is already a Django application, and Django REST Framework provides fast, standard REST API development.

## Data Model

The `Employee` model includes:

- `emp_id`: unique employee identifier
- `first_name`, `last_name`
- `email`
- `department`, `position`
- `hire_date`, `salary`
- `created_at`, `updated_at`

## API Design

The project exposes the following main endpoints:

- `GET /api/employees/`
- `POST /api/employees/`
- `GET /api/employees/{id}/`
- `PUT /api/employees/{id}/`
- `PATCH /api/employees/{id}/`
- `DELETE /api/employees/{id}/`
- `GET /api/employees/search/?query={text}`
- `GET /api/employees/stats/`

These endpoints satisfy the coursework requirement for at least four HTTP-accessible API endpoints and full CRUD functionality.

## Testing Approach

A small API test suite is defined in `webapp/tests.py` using Django REST Framework's `APITestCase`.

The tests cover:

- Listing employees
- Creating employees
- Searching employees

## GenAI Declaration

This project used GitHub Copilot as a GenAI tool to assist with code generation, project structure, and documentation writing. All code and file changes were reviewed and adapted for the coursework context.

## Future Improvements

- Add authentication for protected employee endpoints
- Add pagination for large employee lists
- Add data import from CSV or external HR datasets
- Add Swagger / OpenAPI schema generation for richer API docs
