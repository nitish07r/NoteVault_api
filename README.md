# 📝 NoteVault

A production-ready Notes Management REST API built with **FastAPI**, **PostgreSQL**, and **SQLAlchemy**, featuring **JWT Authentication**, **Role-Based Access Control (RBAC)**, **Docker**, **GitHub Actions CI**, and **Railway Deployment**.

🚀 **Live API Docs:** https://notevaultapi-production-918d.up.railway.app/docs

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
NoteVault_api/
│
├── tests/                  # Automated API tests
│
├── auth.py                 # JWT authentication & authorization
├── config.py               # Environment variable configuration
├── database.py             # Database connection & session management
├── database_models.py      # SQLAlchemy ORM models
├── main.py                 # FastAPI application & API endpoints
├── pydantic_models.py      # Request/Response schemas
│
├── Dockerfile              # Docker image configuration
├── docker-compose.yml      # Multi-container setup
├── requirements.txt        # Python dependencies
├── .env.example            # Environment variable template
├── .gitignore
├── LICENSE
└── README.md
```

## 🔐 Authentication

The API uses **OAuth2 Password Flow** with **JWT (JSON Web Tokens)** for secure authentication.

### User Roles

| Role | Permissions |
|------|-------------|
| **User** | Manage only their own notes |
| **Admin** | Full access to users and notes |

Include the generated JWT access token in the Authorization header:

```http
Authorization: Bearer <your_access_token>
```

## 📚 API Endpoints

### 🔐 Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API health/root endpoint |
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

1. Register a new user using `/register`.
2. Log in via `/login` to receive a JWT access token.
3. Include the token in subsequent requests:

```http
Authorization: Bearer <your_access_token>
```

4. Access protected endpoints such as `/notes` or `/me`.
5. Admin-only endpoints require an account with the **admin** role.


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

### Current Test Status

- ✅ 19 automated API tests
- ✅ 90% code coverage
- ✅ Authentication and authorization tests
- ✅ CRUD operation tests
- ✅ Admin endpoint tests


## ⚙️ Continuous Integration

GitHub Actions automatically validates every push to the `main` branch by:

- Installing project dependencies
- Starting a PostgreSQL service
- Running the complete Pytest suite
- Building the Docker image

This helps ensure new changes don't break existing functionality before deployment.


## ☁️ Deployment

The application is deployed on **Railway**.

### Live API

https://notevaultapi-production-918d.up.railway.app

### Swagger Documentation

https://notevaultapi-production-918d.up.railway.app/docs

## 🚀 Future Enhancements

- Email verification
- Password reset via email
- Refresh token support
- Pagination for notes
- Redis caching
- Rate limiting
- API versioning
- Request logging and monitoring

## 📄 License

This project is licensed under the MIT License.

## 👨‍💻 Author

**S Nitish Kumar**

- GitHub: https://github.com/nitish07r
- LinkedIn: https://www.linkedin.com/in/nitish-kumar-s-ba8928247/

If you found this project helpful, consider giving it a ⭐.
