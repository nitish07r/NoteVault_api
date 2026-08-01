#region Intial basic project setup by me
# from fastapi import Depends, FastAPI
# from pydantic_models import Note
# import database_models
# import json
# from http import HTTPStatus
# from database import engine, SessionLocal
# from sqlalchemy.orm import Session
# from fastapi.middleware.cors import CORSMiddleware

# #here database_models.Note is different from pydantic_models.Note,we use database_models.Note to create tables in database and pydantic_models.Note to validate the data coming from the user,we cant write from database_models import Note because it will create confusion between the two Note classes, so we use different names for them,instead we can use from database_models import Note as DatabaseNote to avoid confusion
# app = FastAPI()
# database_models.Base.metadata.create_all(bind=engine)

# # CORS for React dev server
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://localhost:3000"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()


# # list of notes with 5 Note objects
# notes = [
#     Note(created_by="User1", name="Meeting Notes", description="Discussion about project timeline", priority=8),
#     Note(created_by="User2", name="Todo List", description="Tasks for the week", priority=5),
#     Note(created_by="User3", name="Ideas", description="Brainstorming new features", priority=3),
#     Note(created_by="User1", name="Code Review", description="Review pull request #123", priority=9),
#     Note(created_by="User4", name="Documentation", description="Update API documentation", priority=6),
# ]




# def init_db():
#     db = SessionLocal()

#     existing_count = db.query(database_models.Note).count()

#     if existing_count == 0:
#         for note in notes:
#             db.add(database_models.Note(**note.model_dump()))
#         db.commit()
#         print("Database initialized with sample notes.")
        
#     db.close()

# init_db()    


# #create note
# @app.post("/notes") 
# def create_note(note: Note,db:Session= Depends(get_db)):
#     #u can use model_dump() method to convert pydantic model to dictionary and then pass it to database model also
#     db_note=database_models.Note(
#         created_by=note.created_by,
#         name=note.name,
#         description=note.description,
#         priority=note.priority
#     )
#     db.add(db_note)
#     db.commit()
#     db.refresh(db_note)
#     return {"message":"note created","Note":db_note}
#     #region JSON POST implementation    
#     # with open("Notes.json", "r") as file:
#     #     data = json.load(file)

#     # new_note = {
#     #     "id": len(data) + 1,
#     #     "created_by": note.created_by,
#     #     "name": note.name,
#     #     "description": note.description,
#     #     "priority": note.priority
#     # }

#     # data.append(new_note)

#     # with open("Notes.json", "w") as file:
#     #     json.dump(data, file, indent=4)

#     # return {"message": "Note created", "note": new_note}
#     # #return new_note
#     #endregion    

# #get all notes
# @app.get("/notes")
# def greet(db: Session = Depends(get_db)):
#     db_notes= db.query(database_models.Note).all()
#     if db_notes:
#         return db_notes
#     return {"message":"no notes found"}
#     #region JSON GET implementation
#     # with open("Notes.json", "r") as file:
#     #     data = json.load(file)
#     # #return "hii welcome to my fastapi server"
#     # return data
#     #endregion

# #get note by id
# @app.get("/notes/{note_id}")
# def get_note_byId(note_id:int,db: Session= Depends(get_db)):

#     db_note=db.query(database_models.Note).filter(database_models.Note.id==note_id).first()
#     if db_note:
#         return db_note
#     return {"message":"note not found"}
#     #region JSON GET implementation
#     # with open("Notes.json","r") as file:
#     #     data=json.load(file)
#     # for i in range(len(data)):
#     #     if data[i]["id"]==note_id:
#     #         return {"message":"note fetched succesfully","note":data[i]}
#     # return {"message":"note not found"}
#     #endregion


# #edit note by id
# @app.put("/notes/{note_id}")
# def modify_note(note_id:int,note:Note,db:Session=Depends(get_db)):
#     db_note=db.query(database_models.Note).filter(database_models.Note.id==note_id).first()
#     if db_note:
#         db_note.created_by = note.created_by
#         db_note.name = note.name
#         db_note.description = note.description
#         db_note.priority = note.priority
#         db.commit()
#         db.refresh(db_note)
#         return {"message":f"note with id-{note_id} is updated","note":db_note}
#     return {"message":"note not found"}
#     #region JSON PUT implementation
#     # with open("Notes.json","r") as file:
#     #     data=json.load(file)
#     # for i in range(len(data)):
#     #     if data[i]["id"]==note_id:
#     #         data[i]={
#     #             "id":note_id,
#     #             "created_by":notes.created_by,
#     #             "name":notes.name,
#     #             "description":notes.description,
#     #             "priority":notes.priority
#     #         }
#     #         with open("Notes.json","w") as file:
#     #             json.dump(data,file,indent=4)
#     #         return {"message": "note updated", "note": data[i]}
#     # return{"message":"note not found to update"}
#     #endregion

# #delete note by id           
# @app.delete("/notes/{note_id}")
# def delete_note(note_id:int,db:Session=Depends(get_db)):
#     db_note=db.query(database_models.Note).filter(database_models.Note.id==note_id).first()
#     if db_note:
#         db.delete(db_note)
#         db.commit()
#         return {"message":f"note with id-{note_id} deleted"}
#     return {"message":"note not found"}
#     #region JSON DELETE implementation
    # with open("Notes.json","r") as f:
    #     data=json.load(f)
    # for i in range(len(data)):
    #     if data[i]["id"]==note_id:
    #         del data[i]
    #         with open("Notes.json","w") as file:
    #             json.dump(data,file,indent=4)
    #         return{"message":f"note with id-{note_id} deleted"}
    # return {"message":"note not found"}
    #endregion
######################################################################################################################################

#######################################################################################################################################

from datetime import timedelta
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import FastAPI, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_

import auth
import database
import database_models
import pydantic_models


# ==================================================
# Create Tables
# ==================================================

database_models.Base.metadata.create_all(bind=database.engine)


# ==================================================
# FastAPI App
# ==================================================

app = FastAPI()


# ==================================================
# Database Initialization
# ==================================================

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


# ==================================================
# Authentication Endpoints
# In larger projects these endpoints are usually moved
# to routers/auth.py
# ==================================================


@app.post(
    "/register",
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
    response_model=pydantic_models.Token,
)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(database.get_db),
):

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
    response_model=pydantic_models.UserResponse,
)
def get_current_logged_in_user(
    current_user: database_models.User = Depends(auth.get_current_user),
):
    return current_user


# ==================================================
# Note Endpoints
# In larger projects these endpoints are usually moved
# to routers/notes.py
# ==================================================


@app.post(
    "/notes",
    response_model=pydantic_models.NoteResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_note(
    note: pydantic_models.NoteCreate,
    db: Session = Depends(database.get_db),
    
    current_user: database_models.User = Depends(auth.get_current_user),
):

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
    response_model=pydantic_models.NoteResponse,
)
def get_note_by_id(
    note_id: int,
    db: Session = Depends(database.get_db),
    current_user: database_models.User = Depends(auth.get_current_user),
):

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
    response_model=pydantic_models.NoteResponse,
)
def update_note_by_id(
    note_id: int,
    note_update: pydantic_models.NoteUpdate,
    db: Session = Depends(database.get_db),
    current_user: database_models.User = Depends(auth.get_current_user),
):

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


@app.delete("/notes/{note_id}")
def delete_note_by_id(
    note_id: int,
    db: Session = Depends(database.get_db),
    current_user: database_models.User = Depends(auth.get_current_user),
):

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
    response_model=list[pydantic_models.UserResponse],
)
def get_all_users(
    db: Session = Depends(database.get_db),
    current_admin: database_models.User = Depends(auth.get_current_admin),
):

    users = db.query(database_models.User).all()

    return users


@app.get(
    "/admin/users/{user_id}",
    response_model=pydantic_models.UserResponse,
)
def get_user_by_id(
    user_id: int,
    db: Session = Depends(database.get_db),
    current_admin: database_models.User = Depends(auth.get_current_admin),
):

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
    response_model=list[pydantic_models.NoteResponse],
)
def get_notes_of_user(
    user_id: int,
    db: Session = Depends(database.get_db),
    current_admin: database_models.User = Depends(auth.get_current_admin),
):

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


@app.delete("/admin/notes/{note_id}")
def delete_any_note(
    note_id: int,
    db: Session = Depends(database.get_db),
    current_admin: database_models.User = Depends(auth.get_current_admin),
):

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
)
def create_admin(
    admin_data: pydantic_models.AdminCreate,
    db: Session = Depends(database.get_db),
    current_admin: database_models.User = Depends(auth.get_current_admin),
):

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