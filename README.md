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
                                      ┌─────────────────────────────┐
                                      │      Client Applications    │
                                      │ Browser • Postman • Swagger │
                                      └──────────────┬──────────────┘
                                                     │
                                             HTTP / HTTPS
                                                     │
                                                     ▼
                                ┌──────────────────────────────────┐
                                │          FastAPI Server          │
                                │      REST API Endpoints          │
                                └────────────────┬─────────────────┘
                                                 │
                         ┌───────────────────────┼────────────────────────┐
                         │                       │                        │
                         ▼                       ▼                        ▼
                ┌────────────────┐      ┌────────────────┐      ┌────────────────┐
                │ JWT/OAuth2 Auth│      │ Pydantic Models│      │ Request Routing │
                │ Access Tokens  │      │ Validation     │      │ Dependency Inj. │
                └────────┬───────┘      └────────┬───────┘      └────────┬───────┘
                         │                       │                       │
                         └───────────────────────┼───────────────────────┘
                                                 ▼
                                ┌──────────────────────────────────┐
                                │        Business Logic Layer      │
                                │ CRUD • RBAC • Search • Filtering │
                                └────────────────┬─────────────────┘
                                                 │
                                                 ▼
                                ┌──────────────────────────────────┐
                                │         SQLAlchemy ORM           │
                                └────────────────┬─────────────────┘
                                                 │
                                                 ▼
                                ┌──────────────────────────────────┐
                                │          PostgreSQL DB           │
                                └──────────────────────────────────┘


────────────────────────────────────────────────────────────────────────────────────────

            Development & Deployment Pipeline

        ┌─────────────┐      ┌──────────────┐      ┌──────────────┐
        │ GitHub Push │ ───▶ │ GitHub Actions│ ───▶ │ Pytest (19)  │
        └─────────────┘      └───────┬──────┘      └──────┬───────┘
                                     │                    │
                                     ▼                    ▼
                              Docker Image Build      89% Coverage
                                     │
                                     ▼
                          Railway Cloud Deployment
```
