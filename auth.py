from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from jose import JWTError, jwt
from passlib.context import CryptContext

from sqlalchemy.orm import Session

import database
import database_models


# ==================================================
# JWT Configuration
# ==================================================

SECRET_KEY = "kung-fu-panda"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


# ==================================================
# Password Hashing
# ==================================================

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


# ==================================================
# OAuth2 Configuration
# ==================================================

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="login"
)


# ==================================================
# Password Utilities
# ==================================================

def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(
    plain_password: str,
    hashed_password: str
) -> bool:
    return pwd_context.verify(
        plain_password,
        hashed_password
    )


# ==================================================
# JWT Utilities
# ==================================================

def create_access_token(
    data: dict,
    expires_delta: Optional[timedelta] = None,
) -> str:

    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = (
            datetime.now(timezone.utc)
            + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        )

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM,
    )

    return encoded_jwt


# ==================================================
# User Authentication
# ==================================================

def get_user_by_email(
    db: Session,
    email: str,
) -> Optional[database_models.User]:

    return (
        db.query(database_models.User)
        .filter(database_models.User.email == email)
        .first()
    )


def authenticate_user(
    db: Session,
    email: str,
    password: str,
) -> Optional[database_models.User]:

    user = get_user_by_email(db, email)

    if not user:
        return None

    if not verify_password(
        password,
        user.hashed_password,
    ):
        return None

    return user


# ==================================================
# Current Logged-in User
# ==================================================

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(database.get_db),
) -> database_models.User:

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
        )

        user_id = payload.get("sub")

        if user_id is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    user = (
        db.query(database_models.User)
        .filter(database_models.User.id == int(user_id))
        .first()
    )

    if user is None:
        raise credentials_exception

    return user


# ==================================================
# Admin Authorization
# ==================================================

def get_current_admin(
    current_user: database_models.User = Depends(get_current_user),
) -> database_models.User:

    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required",
        )

    return current_user