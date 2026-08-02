from datetime import timedelta
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import FastAPI, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_

import time
from sqlalchemy import text
from sqlalchemy.exc import OperationalError

import auth
import database
import database_models
import pydantic_models


# ==================================================
# Create Tables
# ==================================================

# Wait for the database to be ready before creating tables for the first time. This is especially useful in containerized environments where the database might take a few seconds to start up.
def wait_for_db(max_retries=10, delay=2):
    print("Waiting for database...")

    for attempt in range(max_retries):
        try:
            with database.engine.connect() as connection:
                connection.execute(text("SELECT 1"))

            print("Database is ready!")
            return

        except OperationalError:
            print(
                f"Database not ready (attempt {attempt + 1}/{max_retries}), "
                f"retrying in {delay} seconds..."
            )
            time.sleep(delay)

    raise RuntimeError("Could not connect to the database.")
            
wait_for_db()

# Create all database tables from the SQLAlchemy models if they do not exist.
database_models.Base.metadata.create_all(bind=database.engine)


# ==================================================
# FastAPI App
# ==================================================

tags_metadata = [
    {
        "name": "Information",
        "description": "General API information and health endpoint.",
    },
    {
        "name": "Authentication",
        "description": "User registration, login, and profile endpoints.",
    },
    {
        "name": "Notes",
        "description": "CRUD operations for authenticated users.",
    },
    {
        "name": "Admin",
        "description": "Administrative endpoints requiring the admin role.",
    },
]

app = FastAPI(
    title="NoteVault API",
    description="A secure Notes Management REST API.",
    version="1.0.0",
    openapi_tags=tags_metadata,
)


# ==================================================
# Database Initialization
# ==================================================


# Seed the database with initial users and notes when the app starts.
# This runs only if an admin user is not already present.
def init_db():

    db = database.SessionLocal()

    try:

        existing_admin = (
            db.query(database_models.User)
            .filter(database_models.User.role == "admin")
            .first()
        )

        if existing_admin:
            return

        users = [

            database_models.User(
                username="admin",
                email="admin@gmail.com",
                hashed_password=auth.hash_password("Admin@123"),
                role="admin",
            ),

            database_models.User(
                username="nitish",
                email="nitish@gmail.com",
                hashed_password=auth.hash_password("Nitish@123"),
            ),

            database_models.User(
                username="rahul",
                email="rahul@gmail.com",
                hashed_password=auth.hash_password("Rahul@123"),
            ),
        ]

        db.add_all(users)
        db.commit()

        for user in users:
            db.refresh(user)

        notes = [

            database_models.Note(
                name="Server Maintenance",
                description="Deploy backend updates on Sunday.",
                priority=3,
                user_id=users[0].id,
            ),

            database_models.Note(
                name="API Roadmap",
                description="Plan JWT and RBAC implementation.",
                priority=2,
                user_id=users[0].id,
            ),

            database_models.Note(
                name="DSA Revision",
                description="Solve 5 Dynamic Programming problems.",
                priority=3,
                user_id=users[1].id,
            ),

            database_models.Note(
                name="Backend Project",
                description="Complete JWT Authentication module.",
                priority=2,
                user_id=users[1].id,
            ),

            database_models.Note(
                name="Vacation Planning",
                description="Book hotel and flights.",
                priority=2,
                user_id=users[2].id,
            ),

            database_models.Note(
                name="Grocery List",
                description="Milk, Eggs, Bread, Fruits.",
                priority=1,
                user_id=users[2].id,
            ),
        ]

        db.add_all(notes)
        db.commit()

        print("Database initialized successfully.")

    finally:
        db.close()


init_db()

#root end point welcome message
@app.get(
    "/",
    tags=["Information"],
    summary="API Information",
    description="Returns basic information about the NoteVault API."
)
def root():
    return {
        "message": "Welcome to NoteVault API!",
        "status": "API is running and healthy ✅.",
        "documentation": "/docs",
        "info": "Visit /docs to explore and test all available API endpoints using the interactive Swagger UI."
    }
# ==================================================
# Authentication Endpoints
# In larger projects these endpoints are usually moved
# to routers/auth.py
# ==================================================


@app.post(
    "/register",
    tags=["Authentication"],
    response_model=pydantic_models.UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def register(
    user: pydantic_models.UserCreate,
    db: Session = Depends(database.get_db),
):

    existing_email = (
        db.query(database_models.User)
        .filter(database_models.User.email == user.email)
        .first()
    )

    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    existing_username = (
        db.query(database_models.User)
        .filter(database_models.User.username == user.username)
        .first()
    )

    if existing_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken",
        )

    new_user = database_models.User(
        username=user.username,
        email=user.email,
        hashed_password=auth.hash_password(user.password),
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


# @app.post(
#     "/login",
#     response_model=pydantic_models.Token,
# )
# def login(
#     user_credentials: pydantic_models.UserLogin,
#     db: Session = Depends(database.get_db),
# ):

#     user = auth.authenticate_user(
#         db,
#         user_credentials.email,
#         user_credentials.password,
#     )

#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid email or password",
#         )

#     access_token = auth.create_access_token(
#         data={
#             "sub": str(user.id)
#         },
#         expires_delta=timedelta(
#             minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES
#         ),
#     )

#     return {
#         "access_token": access_token,
#         "token_type": "bearer",
#     }
# for oauth authorize button form
@app.post(
    "/login",
    tags=["Authentication"],
    response_model=pydantic_models.Token,
)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(database.get_db),
):

    # Authenticate using OAuth2 form data so Swagger UI can submit the login form.
    user = auth.authenticate_user(
        db,
        form_data.username,
        form_data.password,
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    access_token = auth.create_access_token(
        data={"sub": str(user.id)},
        expires_delta=timedelta(
            minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES
        ),
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }


# ==================================================
# Current Logged-in User
# In larger projects this endpoint is usually moved
# to routers/users.py
# ==================================================


@app.get(
    "/me",
    tags=["Authentication"],
    response_model=pydantic_models.UserResponse,
)
def get_current_logged_in_user(
    current_user: database_models.User = Depends(auth.get_current_user),
):
    # Return the authenticated user's profile information.
    # Requires a valid bearer token provided via Authorization header.
    return current_user


# ==================================================
# Note Endpoints
# In larger projects these endpoints are usually moved
# to routers/notes.py
# ==================================================


@app.post(
    "/notes",
    tags=["Notes"],
    response_model=pydantic_models.NoteResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_note(
    note: pydantic_models.NoteCreate,
    db: Session = Depends(database.get_db),
    
    current_user: database_models.User = Depends(auth.get_current_user),
):

    # Create a new note for the authenticated user.
    # The user must be logged in to associate the note with their account.
    new_note = database_models.Note(
        name=note.name,
        description=note.description,
        priority=note.priority,
        user_id=current_user.id,
    )

    db.add(new_note)
    db.commit()
    db.refresh(new_note)

    return new_note

#notes with search and priority filter, if both are provided then both filters will be applied, if only one is provided then only that filter will be applied, if none is provided then all notes of the user will be returned
@app.get(
    "/notes",
    tags=["Notes"],
    response_model=pydantic_models.PaginatedNotes,
)
def get_my_notes(
    search: str | None = None,
    priority: int | None = None,
    db: Session = Depends(database.get_db),
    sort: str | None = None,
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    current_user: database_models.User = Depends(auth.get_current_user),
):

    # Return notes for the authenticated user with optional search,
    # priority filtering, sorting, and pagination.
    query = (
        db.query(database_models.Note)
        .filter(database_models.Note.user_id == current_user.id)
    )

    if search:
        query = query.filter(
            or_(
                database_models.Note.name.ilike(f"%{search}%"),
                database_models.Note.description.ilike(f"%{search}%"),
            )
        )

    if priority is not None:
        query = query.filter(
            database_models.Note.priority == priority
        )
        
    if sort:

        descending = sort.startswith("-")

        sort_field = sort[1:] if descending else sort

        allowed_fields = {
            "priority": database_models.Note.priority,
            "created_at": database_models.Note.created_at,
            "updated_at": database_models.Note.updated_at,
            "name": database_models.Note.name,
        }

        if sort_field not in allowed_fields:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid sort field",
            )

        column = allowed_fields[sort_field]

        if descending:
            query = query.order_by(column.desc())
        else:
            query = query.order_by(column.asc())

    total = query.count()
    
    notes = (
        query
        .offset((page - 1) * limit)
        .limit(limit)
        .all()
    )

    return {
        "total": total,
        "page": page,
        "limit": limit,
        "items": notes,
    }

@app.get(
    "/notes/{note_id}",
    tags=["Notes"],
    response_model=pydantic_models.NoteResponse,
)
def get_note_by_id(
    note_id: int,
    db: Session = Depends(database.get_db),
    current_user: database_models.User = Depends(auth.get_current_user),
):

    # Retrieve a single note by ID for the authenticated user.
    # The note must belong to the requesting user.
    note = (
        db.query(database_models.Note)
        .filter(
            database_models.Note.id == note_id,
            database_models.Note.user_id == current_user.id,
        )
        .first()
    )

    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found",
        )

    return note


@app.patch(
    "/notes/{note_id}",
    tags=["Notes"],
    response_model=pydantic_models.NoteResponse,
)
def update_note_by_id(
    note_id: int,
    note_update: pydantic_models.NoteUpdate,
    db: Session = Depends(database.get_db),
    current_user: database_models.User = Depends(auth.get_current_user),
):

    # Update only fields provided by the user, leaving other values unchanged.
    note = (
        db.query(database_models.Note)
        .filter(
            database_models.Note.id == note_id,
            database_models.Note.user_id == current_user.id,
        )
        .first()
    )

    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found",
        )

    update_data = note_update.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(note, key, value)

    db.commit()
    db.refresh(note)

    return note


@app.delete("/notes/{note_id}", tags=["Notes"])
def delete_note_by_id(
    note_id: int,
    db: Session = Depends(database.get_db),
    current_user: database_models.User = Depends(auth.get_current_user),
):
    # Delete a note owned by the authenticated user.
    # Users cannot delete notes belonging to other users.

    note = (
        db.query(database_models.Note)
        .filter(
            database_models.Note.id == note_id,
            database_models.Note.user_id == current_user.id,
        )
        .first()
    )

    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found",
        )

    db.delete(note)
    db.commit()

    return {
        "detail": "Note deleted successfully"
    }
    
# ==================================================
# Admin Endpoints
# In larger projects these endpoints are usually moved
# to routers/admin.py
# ==================================================


@app.get(
    "/admin/users",
    tags=["Admin"],
    response_model=list[pydantic_models.UserResponse],
)
def get_all_users(
    db: Session = Depends(database.get_db),
    current_admin: database_models.User = Depends(auth.get_current_admin),
):
    # Return all registered users; restricted to admin users only.
    users = db.query(database_models.User).all()

    return users


@app.get(
    "/admin/users/{user_id}",
    tags=["Admin"],
    response_model=pydantic_models.UserResponse,
)
def get_user_by_id(
    user_id: int,
    db: Session = Depends(database.get_db),
    current_admin: database_models.User = Depends(auth.get_current_admin),
):
    # Retrieve a specific user by ID. Only admins may access this endpoint.
    user = (
        db.query(database_models.User)
        .filter(database_models.User.id == user_id)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return user


@app.get(
    "/admin/users/{user_id}/notes",
    tags=["Admin"],
    response_model=list[pydantic_models.NoteResponse],
)
def get_notes_of_user(
    user_id: int,
    db: Session = Depends(database.get_db),
    current_admin: database_models.User = Depends(auth.get_current_admin),
):
    # Admin endpoint to view notes for a specific user.
    user = (
        db.query(database_models.User)
        .filter(database_models.User.id == user_id)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    notes = (
        db.query(database_models.Note)
        .filter(database_models.Note.user_id == user_id)
        .all()
    )

    return notes

#with search and priority filter, if both are provided then both filters will be applied, if only one is provided then only that filter will be applied, if none is provided then all notes of the user will be returned
@app.get(
    "/admin/notes",
    tags=["Admin"],
    response_model=pydantic_models.PaginatedNotes,
)
def get_all_notes(
    search: str | None = None,
    priority: int | None = None,
    sort: str | None = None,
    db: Session = Depends(database.get_db),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    current_admin: database_models.User = Depends(auth.get_current_admin),
    
):

    # Return all notes across all users for admins.
    # Supports search, priority filtering, sorting, and pagination.
    query = db.query(database_models.Note)

    if search:
        query = query.filter(
            or_(
                database_models.Note.name.ilike(f"%{search}%"),
                database_models.Note.description.ilike(f"%{search}%"),
            )
        )

    if priority is not None:
        query = query.filter(
            database_models.Note.priority == priority
        )
        
    if sort:

        descending = sort.startswith("-")

        sort_field = sort[1:] if descending else sort

        allowed_fields = {
            "priority": database_models.Note.priority,
            "created_at": database_models.Note.created_at,
            "updated_at": database_models.Note.updated_at,
            "name": database_models.Note.name,
        }

        if sort_field not in allowed_fields:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid sort field",
            )

        column = allowed_fields[sort_field]

        if descending:
            query = query.order_by(column.desc())
        else:
            query = query.order_by(column.asc())

    total = query.count()
    notes = (
        query
        .offset((page - 1) * limit)
        .limit(limit)
        .all()
    )

    return {
        "total": total,
        "page": page,
        "limit": limit,
        "items": notes,
    }


@app.delete("/admin/notes/{note_id}", tags=["Admin"])
def delete_any_note(
    note_id: int,
    db: Session = Depends(database.get_db),
    current_admin: database_models.User = Depends(auth.get_current_admin),
):
    # Admin may delete any note by ID, regardless of ownership.
    note = (
        db.query(database_models.Note)
        .filter(database_models.Note.id == note_id)
        .first()
    )

    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found",
        )

    db.delete(note)
    db.commit()

    return {
        "detail": "Note deleted successfully"
    }
    
#Admin can create another admin user, but only if they are logged in as an admin. This endpoint is protected by the get_current_admin dependency, which checks if the current user is an admin before allowing access to this endpoint.

@app.post(
    "/admin/create-admin",
    response_model=pydantic_models.UserResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Admin"]
)
def create_admin(
    admin_data: pydantic_models.AdminCreate,
    db: Session = Depends(database.get_db),
    current_admin: database_models.User = Depends(auth.get_current_admin),
):
    # Create a new admin user. Only an existing admin can perform this action.
    existing_email = (
        db.query(database_models.User)
        .filter(database_models.User.email == admin_data.email)
        .first()
    )

    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    existing_username = (
        db.query(database_models.User)
        .filter(database_models.User.username == admin_data.username)
        .first()
    )

    if existing_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken",
        )

    new_admin = database_models.User(
        username=admin_data.username,
        email=admin_data.email,
        hashed_password=auth.hash_password(admin_data.password),
        role="admin",
    )

    db.add(new_admin)
    db.commit()
    db.refresh(new_admin)

    return new_admin


import os
import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8000)),
    )