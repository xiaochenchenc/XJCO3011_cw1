# Employee Management API — Documentation

This document matches the **current** Django + Django REST Framework implementation in this repository (`webapp/views.py`, `webapp/urls.py`, `webapp/serializers.py`, `cw1/settings.py`).

**URL (development):** `https://caoyuchen688.pythonanywhere.com/`


## 1. Overview

| Item | Value |
|------|--------|
| API style | REST over HTTP, JSON bodies |
| Default format | `application/json` |
| Browsable API | Enabled (HTML responses in browser for many GETs when not sending `Accept: application/json`) |
| Database | SQLite (`Employee` model) |

**Important:** Coursework asks for a **PDF** copy of API documentation in the submission pack. Export this Markdown to PDF when you submit (or print from browser).

---

## 2. Discovery endpoints

### 2.1 JSON API index (custom)

- **URL:** `GET /api/info/`
- **Auth:** Not required  
- **Response:** `200 OK`, `Content-Type: application/json`  

Returns a small JSON object listing main entry points (employees list, search, stats, auth URLs).

### 2.2 DRF router root (framework default)

- **URL:** `GET /api/`  
- **Auth:** Not required for GET in default setup  
- **Response:** Django REST Framework **“Api Root”** page (HTML) with a hyperlink to `employees`. This is **not** the same payload as `GET /api/info/`.

---

## 3. Authentication and permissions

### 3.1 Mechanisms

| Mechanism | When it applies |
|-----------|------------------|
| **Token** | Send header `Authorization: Token <token>` on write requests (and optionally on reads). |
| **Session** | If you are logged into the same site in a browser (e.g. Django admin), the session cookie may satisfy `SessionAuthentication` for same-origin API calls. |

### 3.2 Global permission rule (`REST_FRAMEWORK`)

Default permission class: **`IsAuthenticatedOrReadOnly`**.

| HTTP method on `/api/employees/...` | Anonymous (no token / no session) | Authenticated |
|--------------------------------------|-------------------------------------|---------------|
| GET, HEAD, OPTIONS | Allowed | Allowed |
| POST, PUT, PATCH, DELETE | **401 Unauthorized** | Allowed (subject to validation) |

**Auth endpoints**

| Endpoint | Anonymous |
|----------|-----------|
| `POST /api/auth/register/` | Allowed (`AllowAny` on view) |
| `POST /api/auth/` (login) | Allowed (DRF token obtain view) |

### 3.3 Obtaining a token

**Register**

- **URL:** `POST /api/auth/register/`
- **Content-Type:** `application/json`  

**Request body (JSON):**

| Field | Required | Notes |
|-------|----------|--------|
| `username` | Yes | Must be unique. |
| `email` | Yes | Must be unique. |
| `password` | Yes | Stored hashed. |

**Success:** `201 Created`

```json
{
  "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b",
  "user_id": 1,
  "email": "your_email@example.com",
  "username": "your_username",
  "message": "User created successfully"
}
```

**Errors:** `400 Bad Request` with JSON such as:

```json
{ "error": "Username already exists" }
```

or

```json
{ "error": "Username, email, and password are required" }
```

---

**Login**

- **URL:** `POST /api/auth/`  
- **Content-Type:** `application/json`  

**Request body:**

| Field | Required |
|-------|----------|
| `username` | Yes |
| `password` | Yes |

**Success:** `200 OK`

```json
{
  "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b",
  "user_id": 1,
  "email": "your_email@example.com",
  "username": "your_username"
}
```

**Errors:** Invalid credentials typically yield **`400 Bad Request`** with DRF’s default validation error structure (not the custom `{ "error": "..." }` shape used by register).

---

## 4. Employee resource

### 4.1 Fields (JSON representation)

| Field | Type | Writable via API | Notes |
|-------|------|------------------|--------|
| `id` | integer | No (read-only) | Django primary key. **Do not** assume it equals the sequence in `employees.json`. |
| `export_id` | integer or `null` | No (read-only) | Optional. Set when loading `employees.json` via `import_employees_json` (maps JSON `"id"`). Used for stable ordering and lookup. |
| `emp_id` | integer | Yes on create; yes on update | Business employee number; **unique**. |
| `first_name` | string | Yes | Max length 50. |
| `last_name` | string | Yes | Max length 50. |
| `email` | string (email) | Yes | **Unique**. |
| `department` | string | Yes | May be empty string. |
| `position` | string | Yes | May be empty string. |
| `hire_date` | string (`YYYY-MM-DD`) or `null` | Yes | ISO date. |
| `salary` | string (decimal) or `null` | Yes | e.g. `"58000.00"`. |
| `created_at` | string (ISO 8601 datetime) | No | Set by server. |
| `updated_at` | string (ISO 8601 datetime) | No | Set by server. |

### 4.2 List ordering

`GET /api/employees/` returns rows ordered by:

1. `export_id` ascending, treating missing `export_id` as a large sort value (so manually created rows without `export_id` appear after imported rows), then  
2. `emp_id` ascending.

---

## 5. Employee endpoints (`/api/employees/`)

All paths below are relative to the site root (e.g. `http://127.0.0.1:8000/api/employees/`).

### 5.1 List employees

- **Method / URL:** `GET /api/employees/`  
- **Auth:** Optional  
- **Success:** `200 OK` — JSON **array** of employee objects.  

**Example response (truncated):**

```json
[
  {
    "id": 1,
    "export_id": 1,
    "emp_id": 1001,
    "first_name": "Alice",
    "last_name": "Zhang",
    "email": "alice.zhang1@example.com",
    "department": "Engineering",
    "position": "Software Engineer",
    "hire_date": "2024-08-01",
    "salary": "58000.02",
    "created_at": "2026-04-10T03:32:42.820298Z",
    "updated_at": "2026-04-19T08:14:23.065303Z"
  }
]
```

---

### 5.2 Create employee

- **Method / URL:** `POST /api/employees/`  
- **Auth:** **Required** (token or session)  
- **Content-Type:** `application/json`  

**Request body (minimal example):**

```json
{
  "emp_id": 2001,
  "first_name": "Sam",
  "last_name": "Lee",
  "email": "sam.lee@example.com",
  "department": "Engineering",
  "position": "Intern",
  "hire_date": "2026-04-01",
  "salary": "30000.00"
}
```

**Success:** `201 Created` — response body is the created employee object.

**Typical errors:**

| Code | Situation |
|------|-----------|
| `400 Bad Request` | Validation error (e.g. duplicate `email` / `emp_id`, invalid field). Body is usually DRF field errors. |
| `401 Unauthorized` | Missing/invalid token for anonymous POST. |

---

### 5.3 Retrieve, update, delete (single employee)

The path parameter in the router is named **`pk`** in URLconf, but the application resolves it in this **fixed order** (must be a **decimal integer** string):

1. **`id`** — Django primary key  
2. **`export_id`** — JSON sequence from import (if used)  
3. **`emp_id`** — business id  

**Examples**

- `GET /api/employees/42/` — first tries `Employee.id == 42`, then `export_id == 42`, then `emp_id == 42`.  
- After importing `employees.json` with `export_id` populated, `GET /api/employees/6/` can return the row whose JSON `"id"` was `6` **as long as** no other row uses `id=6` earlier in the resolution order.

**Retrieve**

- **Method / URL:** `GET /api/employees/{pk}/`  
- **Auth:** Optional  
- **Success:** `200 OK` — one employee object.  
- **Not found:** `404 Not Found` (invalid non-integer `pk` also yields 404).

**Full replace**

- **Method / URL:** `PUT /api/employees/{pk}/`  
- **Auth:** Required  
- **Body:** Full resource (same fields as create; read-only fields ignored on input).  
- **Success:** `200 OK`  

**Partial update**

- **Method / URL:** `PATCH /api/employees/{pk}/`  
- **Auth:** Required  
- **Body:** Any subset of writable fields.  
- **Success:** `200 OK`  

**Delete**

- **Method / URL:** `DELETE /api/employees/{pk}/`  
- **Auth:** Required  
- **Success:** `204 No Content` (typical DRF destroy response; no JSON body).  
- **Not found:** `404 Not Found`  

---

### 5.4 Search

- **Method / URL:** `GET /api/employees/search/`  
- **Query parameter:** `query` (required)  
- **Auth:** Optional  

**Behaviour**

- Case-insensitive substring match on: `first_name`, `last_name`, `department`, `position`, `email`.  
- If `query` consists **only of digits** (e.g. `"1006"`, `"6"`), the result also includes rows where **`emp_id`**, **`id`**, or **`export_id`** equals that integer (in addition to text matches).

**Errors**

- Missing or empty `query`: `400 Bad Request`  

```json
{ "detail": "The query parameter is required." }
```

**Success:** `200 OK` — JSON array (may be empty).

---

### 5.5 Department statistics

- **Method / URL:** `GET /api/employees/stats/`  
- **Auth:** Optional  
- **Success:** `200 OK`  

```json
{
  "department_counts": [
    { "department": "Engineering", "total": 12 },
    { "department": "Sales", "total": 5 }
  ]
}
```

Notes:

- Counts **all** rows in `Employee` (not filtered by the annotated list queryset).  
- Empty-string departments are grouped as `""` in JSON.

---

## 6. Error handling

This section describes **how errors are expressed** using HTTP status codes and JSON bodies, so clients (and examiners) can rely on predictable behaviour.

### 6.1 Principles

- **Use status codes for outcome classes:** success (`2xx`), client error (`4xx`), server error (`5xx`).  
- **Prefer JSON bodies for errors** where DRF returns them; some successes (e.g. `204 No Content`) correctly have **no** response body.  
- **Separate authentication from validation:** unauthenticated writes to employee endpoints → `401`; invalid fields → `400`.

### 6.2 Common status codes

| Code | Meaning | Typical use in this API |
|------|---------|-------------------------|
| `200 OK` | Success | Successful GET, PUT, or PATCH |
| `201 Created` | Created | Successful POST (employee or register) |
| `204 No Content` | Success, no body | Successful DELETE (usually no JSON body) |
| `400 Bad Request` | Bad request | Validation failure, missing `query`, bad login/register payload |
| `401 Unauthorized` | Not authenticated | Anonymous POST/PUT/PATCH/DELETE on `/api/employees/...` |
| `404 Not Found` | Not found | No employee matches detail URL; non-integer `{pk}` also yields 404 |
| `405 Method Not Allowed` | Wrong method | HTTP verb not allowed for that URL |
| `415 Unsupported Media Type` | Unsupported media type | e.g. POST without `Content-Type: application/json` (depends on client and DRF) |
| `500 Internal Server Error` | Server error | Unhandled exception (debug via server logs) |

### 6.3 Response body shapes

**(1) DRF field validation (`400`)** — field name → list of messages:

```json
{
  "email": ["employee with this email already exists."]
}
```

**(2) Register endpoint custom error (`400`)** — single `error` string:

```json
{ "error": "Username already exists" }
```

**(3) Search missing parameter (`400`)**

```json
{ "detail": "The query parameter is required." }
```

**(4) Unauthenticated write to employees (`401`)** — typical DRF payload:

```json
{
  "detail": "Authentication credentials were not provided."
}
```

**(5) Login failure (`400`)** — DRF’s serializer errors for invalid username/password (shape may differ from register’s `{ "error": "..." }`).

### 6.4 By scenario

| Scenario | Status | Notes |
|----------|--------|--------|
| Anonymous `POST` / `PUT` / `PATCH` / `DELETE` on `/api/employees/...` | `401` | Obtain a token via `POST /api/auth/` or register, then send `Authorization: Token ...` |
| Create/update employee: duplicate `email` / `emp_id`, invalid types | `400` | See field-error JSON in section 6.3 |
| `GET /api/employees/search/` with missing or empty `query` | `400` | `detail` as above |
| `GET` / `PUT` / `PATCH` / `DELETE` on `.../employees/{pk}/` with no match or non-integer `pk` | `404` | No row matches after `id` → `export_id` → `emp_id` resolution |

---

## 7. cURL examples

### 7.1 What this section is for

This section is **not part of the API contract**. It only provides **copy-paste command-line examples** using [cURL](https://curl.se/) so you can call the same URLs as a browser or Postman without writing application code. Flags such as `-s` (silent), `-X POST`, `-H` (headers), and `-d` (JSON body) are normal terminal usage.

**List (no auth)**

```bash
curl -s http://127.0.0.1:8000/api/employees/
```

**Create (with token)**

```bash
curl -s -X POST http://127.0.0.1:8000/api/employees/ \
  -H "Authorization: Token YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d "{\"emp_id\":3001,\"first_name\":\"Bo\",\"last_name\":\"Hu\",\"email\":\"bo.hu@example.com\",\"department\":\"IT\",\"position\":\"Dev\",\"hire_date\":\"2026-01-01\",\"salary\":\"60000.00\"}"
```

**Login**

```bash
curl -s -X POST http://127.0.0.1:8000/api/auth/ \
  -H "Content-Type: application/json" \
  -d "{\"username\":\"your_username\",\"password\":\"your_password\"}"
```

---

## 8. Bulk data (not HTTP API)

### 8.1 Why the title says “not HTTP API”

Bulk loading from `employees.json` is implemented as a **Django management command** (`python manage.py ...`), which runs **in the server shell**, not over HTTP. This project **does not** expose `POST /api/import` (by design): the coursework API is REST CRUD over HTTP, while one-off bulk import is a **deployment / maintenance** task. The label **“not HTTP API”** means you **cannot** invoke `import_employees_json` with `curl` against a URL the way you do for `/api/employees/`.

### 8.2 Commands reference

Loading `employees.json` uses a Django management command (not a REST endpoint):

```bash
python manage.py import_employees_json
python manage.py import_employees_json --clear --yes
```

See `README.md` for semantics of `export_id` and `--clear`.

---

## 9. Review notes (accuracy checklist)

| Topic | Status |
|-------|--------|
| Write auth | Correct: anonymous POST/PUT/PATCH/DELETE on employees → **401**. |
| Register/login | Correct: `POST` only; separate URLs. |
| Detail `{pk}` | Correct: resolves **`id` → `export_id` → `emp_id`** (integer only). |
| Search digits | Doc previously under-stated; now includes **`export_id`**. |
| `GET /api/` vs `GET /api/info/` | Router owns `/api/`; custom JSON index is **`/api/info/`** (added in `webapp/urls.py`). |
| `export_id` via API | Intentionally **read-only** in serializer; set via import command only. |

