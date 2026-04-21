# Employee Management API

This Django project implements an employee management web platform for the XJCO3011 coursework.

**Repository:** https://github.com/xiaochenchenc/XJCO3011_cw1

## Features

- **Web Interface**: Full-featured web application for managing employees
- **REST API**: Complete CRUD operations for employee records with authentication
- **Search Functionality**: Search employees by name, department, position, or email
- **Analytics Dashboard**: Department statistics and employee counts
- **User Authentication**: Token-based authentication system
- **Admin Interface**: Django admin panel for data management
- **Responsive Design**: Bootstrap-based UI that works on all devices

## Setup

From the **repository root** (the folder that contains `manage.py`):

1. Create a Python virtual environment and activate it (Python 3.10+ recommended).
2. Install dependencies:

```bash
pip install -r requirements.txt
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

## Tests

```bash
python manage.py test
```

This runs the automated API and import-command tests in `webapp/tests.py`.

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

The API is available under `http://127.0.0.1:8000/api/`. A small JSON index of routes is at `http://127.0.0.1:8000/api/info/` (the bare `/api/` URL is the DRF browsable router root).

Endpoints include:

#### Authentication Endpoints
- `POST /api/auth/register/` - Register new user
- `POST /api/auth/` - Login and get token

#### Employee Endpoints
- `GET /api/employees/` - List all employees
- `POST /api/employees/` - Create employee (requires auth)
- `GET /api/employees/{id}/` - Get employee details (`{id}` = database `id`, then JSON `export_id`, then `emp_id`)
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

## employees.json (optional bulk import)

If you keep `employees.json` in the project root (array of objects with `emp_id`, names, `email`, etc.), you can load it into the database with:

```bash
python manage.py import_employees_json
```

Dry run (validate only):

```bash
python manage.py import_employees_json --dry-run
```

Custom path:

```bash
python manage.py import_employees_json --json path/to/employees.json
```

The importer stores the JSON **`id`** field as `export_id` (so list order and the “JSON #” column match your file). It still ignores `created_at` and `updated_at` (Django sets those on save).

To wipe the database and reload exactly from the file (removes stray rows that break ordering or IDs):

```bash
python manage.py import_employees_json --clear --yes
```

## API Documentation

See `docs/API_DOCUMENTATION.md` for detailed endpoint documentation with examples.

For coursework submission, the brief typically expects a **PDF** export of the API documentation: open the Markdown in an editor or browser and export/print to PDF (see the note at the top of that file).

## Technical Report

See `docs/TECHNICAL_REPORT.md` for design rationale, stack decisions, testing approach, and **appendices** (GenAI declaration and ChatGPT screenshot in **Appendix A**, GitHub upload/commit evidence in **Appendix B**, submission links, checklists). Place evidence images next to that file under `docs/` (`ChatGPT.png`, `github_upload_history.png`) or adjust paths in the Markdown before PDF export.

## Presentation slides

Coursework visuals are drafted in `presentation_slides.md` at the repository root (export to PPTX/PDF per your module instructions).

## Project structure

```
<repository root>/
├── manage.py
├── requirements.txt
├── README.md
├── employees.json          # Optional seed data (import command)
├── cw1/                    # Django project settings package
│   ├── settings.py
│   └── urls.py
├── webapp/                 # Main application
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   ├── urls.py
│   ├── admin.py
│   ├── tests.py
│   └── management/commands/
│       └── import_employees_json.py
├── templates/
├── static/
└── docs/
    ├── API_document.pdf
    └── Technical_report.pdf
    └── cw1 pre.pptx

```
