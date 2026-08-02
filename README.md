# 📝 NoteVault

A production-ready Notes Management REST API built with **FastAPI**, **PostgreSQL**, and **SQLAlchemy**, featuring **JWT Authentication**, **Role-Based Access Control (RBAC)**, **Docker**, **GitHub Actions CI**, and **Railway Deployment**.

---

## 🚀 Try the Live API

### 📖 Interactive Swagger UI

https://notevaultapi-production-918d.up.railway.app/docs

### 🔑 Test Credentials

#### 👑 Admin

| Field | Value |
|------|-------|
| **Email** | `admin@gmail.com` |
| **Password** | `Admin@123` |

#### 👤 User

| Field | Value |
|------|-------|
| **Email** | `nitish@gmail.com` |
| **Password** | `Nitish@123` |

### ⚡ Quick Start

1. Open the **Swagger UI**.
2. Click **Authorize**.
3. Enter:
   - **username** → Use the email above.
   - **password** → Use the corresponding password.
4. Leave **client_id** and **client_secret** empty.
5. Click **Authorize**.
6. Explore the protected API endpoints.

> **Note:** Swagger labels the field as **username**, but this API authenticates users using their **email address**.

---

## ✨ Features

- 🔐 JWT Authentication & Authorization
- 👥 Role-Based Access Control (Admin & User)
- 📝 Complete CRUD Operations for Notes
- 🔍 Search and Filtering Support
- ✅ Request Validation with Pydantic
- 🗄️ PostgreSQL + SQLAlchemy ORM
- 🐳 Docker & Docker Compose Support
- ☁️ Deployed on Railway
- 🧪 Automated Testing with Pytest
- ⚙️ GitHub Actions Continuous Integration
- 📖 Interactive Swagger/OpenAPI Documentation

## 🛠️ Tech Stack

| Category | Technologies |
|----------|--------------|
| **Backend** | FastAPI |
| **Language** | Python |
| **Database** | PostgreSQL |
| **ORM** | SQLAlchemy |
| **Authentication** | JWT (python-jose), OAuth2 |
| **Testing** | Pytest |
| **Containerization** | Docker, Docker Compose |
| **CI/CD** | GitHub Actions |
| **Deployment** | Railway |

## 🏗️ System Architecture

```text
                                        ┌────────────────────────────────────┐
                                        │      Client Applications           │
                                        │ Browser • Postman • Swagger UI     │
                                        └────────────────┬───────────────────┘
                                                         │
                                                   HTTP / HTTPS
                                                         │
                                                         ▼
                              ┌──────────────────────────────────────────────────────┐
                              │                FastAPI REST API                      │
                              │                  Request Handler                     │
                              └─────────────────────┬────────────────────────────────┘
                                                    │
          ┌───────────────────────────────┬─────────┼─────────┬──────────────────────────────┐
          ▼                               ▼                   ▼                              ▼
 ┌─────────────────────┐        ┌──────────────────┐  ┌──────────────────┐        ┌────────────────────┐
 │ JWT Authentication  │        │ Request          │  │ Dependency       │        │ Exception Handling │
 │ OAuth2 + AccessToken│        │ Validation       │  │ Injection        │        │ HTTP Responses     │
 └──────────┬──────────┘        │ Pydantic Models  │  │ FastAPI Depends  │        └──────────┬─────────┘
            │                   └────────┬─────────┘  └────────┬─────────┘                   │
            └────────────────────────────┴──────────────────────┴─────────────────────────────┘
                                                     │
                                                     ▼
                              ┌──────────────────────────────────────────────────────┐
                              │              Business Logic Layer                    │
                              │      RBAC • CRUD • Search • Filtering                │
                              └─────────────────────┬────────────────────────────────┘
                                                    │
                                                    ▼
                              ┌──────────────────────────────────────────────────────┐
                              │                SQLAlchemy ORM                        │
                              └─────────────────────┬────────────────────────────────┘
                                                    │
                                                    ▼
                              ┌──────────────────────────────────────────────────────┐
                              │                PostgreSQL Database                   │
                              └──────────────────────────────────────────────────────┘


══════════════════════════════════════════════════════════════════════════════════════════════════════════════

                                   Development & Delivery Workflow

                                                Developer
                                                    │
                                                    ▼
                                              Git Push
                                                    │
                        ┌───────────────────────────┴────────────────────────────┐
                        ▼                                                        ▼
              GitHub Actions CI                                      Railway Auto Deploy
                        │                                                        │
          ┌─────────────┼─────────────┐                               Pull Latest Code
          ▼             ▼             ▼                                        │
  Install Dependencies  Start PostgreSQL  Build Docker Image                   ▼
          │             │             │                                 Build Application
          └─────────────┼─────────────┘                                        │
                        ▼                                                      ▼
               Execute Pytest Suite                                   Launch FastAPI Server
                        │                                                      │
                        ▼                                                      ▼
              ✅ 19 Tests Passed                                     🌐 Live API & Swagger Docs
              ✅ 90% Code Coverage
```

## 📂 Project Structure

```text
NoteVault_API/
│
├── .github/
│   └── workflows/
│       └── ci.yml                 # GitHub Actions CI pipeline
│
├── tests/                         # Pytest test suite
│   ├── conftest.py
│   ├── test_auth.py
│   ├── test_notes.py
│   ├── test_admin.py
│   └── ...
│
├── auth.py                        # JWT authentication & password hashing
├── database.py                    # Database connection & SQLAlchemy session
├── database_models.py             # SQLAlchemy ORM models
├── pydantic_models.py             # Request/Response schemas
├── main.py                        # FastAPI application & API routes
│
├── Dockerfile                     # Docker image configuration
├── docker-compose.yml             # Multi-container setup (API + PostgreSQL)
├── requirements.txt               # Python dependencies
├── pytest.ini                     # Pytest configuration
├── .env.example                   # Example environment variables
├── .dockerignore                  # Docker ignore rules
├── .gitignore                     # Git ignore rules
│
└── README.md                      # Project documentation
```

## 🔐 Authentication

The API uses **OAuth2 Password Flow** with **JWT (JSON Web Tokens)** for secure authentication.

### User Roles

| Role | Permissions |
|------|-------------|
| **User** | Create, view, update, and delete only their own notes |
| **Admin** | Full access to users, notes, and administrative endpoints |

### Using Swagger Authorization

1. Open the **Swagger UI** (`/docs`).
2. Click the **Authorize** button.
3. Enter the following credentials:

- **username** → Your **email address**
- **password** → Your password

Leave the following fields empty:

- `client_id`
- `client_secret`

Click **Authorize**, then **Close**.

All protected endpoints will automatically include the JWT access token in the `Authorization` header for the remainder of your session.

> **Note:** Although Swagger labels the field as **username**, this API authenticates users using their **email address**.

## 📚 API Endpoints

### 🔐 Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/register` | Register a new user |
| POST | `/login` | Authenticate and receive a JWT access token |
| GET | `/me` | Retrieve the currently authenticated user's profile |

---

### 📝 Notes

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/notes` | Create a new note |
| GET | `/notes` | Retrieve all notes belonging to the authenticated user |
| GET | `/notes/{note_id}` | Retrieve a specific note |
| PATCH | `/notes/{note_id}` | Update a specific note |
| DELETE | `/notes/{note_id}` | Delete a specific note |

---

### 👑 Admin

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/admin/users` | Retrieve all registered users |
| GET | `/admin/users/{user_id}` | Retrieve a user by ID |
| GET | `/admin/users/{user_id}/notes` | Retrieve all notes of a specific user |
| GET | `/admin/notes` | Retrieve all notes across the system |
| DELETE | `/admin/notes/{note_id}` | Delete any user's note |
| POST | `/admin/create-admin` | Create a new administrator |

> **Note:** All `/notes` and `/admin` endpoints require a valid JWT access token in the `Authorization: Bearer <token>` header.

## 🔑 Authentication Flow

### Option 1 (Recommended) — Swagger UI

1. Open the **Swagger UI** (`/docs`).
2. Click **Authorize**.
3. Log in using one of the demo accounts.
4. Click **Authorize**, then **Close**.
5. Test any protected endpoint directly from Swagger.

---

### Option 2 — Using the `/login` Endpoint

1. Send a request to `/login` with your email and password.
2. Copy the returned JWT access token.
3. Include it in the `Authorization` header for protected endpoints:

```http
Authorization: Bearer <your_access_token>
```

4. Access endpoints such as `/me`, `/notes`, and all other protected resources.

## 🚀 Running Locally

### 1. Clone the Repository

```bash
git clone https://github.com/nitish07r/NoteVault_api.git
cd NoteVault_api
```

### 2. Create a Virtual Environment

Windows

```bash
python -m venv myenv
myenv\Scripts\activate
```

Linux / macOS

```bash
python3 -m venv myenv
source myenv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root using the following template:

```env
DATABASE_URL=your_database_url
TEST_DATABASE_URL=your_test_database_url
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 5. Run the Application

```bash
uvicorn main:app --reload
```

Visit:

```
http://127.0.0.1:8000/docs
```

for the interactive Swagger UI.

## 🐳 Running with Docker

Build and start the application along with PostgreSQL:

```bash
docker compose up --build
```

To stop all running containers:

```bash
docker compose down
```

The API will be available at:

```
http://localhost:8000/docs
```

## 🧪 Testing

Run the complete test suite:

```bash
pytest
```

Generate a coverage report:

```bash
pytest --cov
```

### Current Test Coverage

- ✅ 19 automated integration tests
- ✅ ~90% code coverage
- ✅ Authentication & Authorization
- ✅ User CRUD operations
- ✅ Admin endpoints
- ✅ Role-Based Access Control


## ⚙️ Continuous Integration

Every push to the `main` branch automatically triggers a GitHub Actions workflow that:

- Installs project dependencies
- Starts a PostgreSQL service
- Executes the complete Pytest suite
- Generates the coverage report
- Builds the Docker image

This ensures new changes are continuously validated before deployment.


## ☁️ Deployment

The application is deployed on **Railway** and is publicly accessible.

| Service | URL |
|---------|-----|
| 📖 Swagger UI | https://notevaultapi-production-918d.up.railway.app/docs |

## 📄 License

This project is licensed under the MIT License.

## 👨‍💻 Author

**S Nitish Kumar**

- GitHub: https://github.com/nitish07r
- LinkedIn: https://www.linkedin.com/in/nitish-kumar-s-ba8928247/

If you found this project helpful, consider giving it a ⭐.
