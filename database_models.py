from datetime import datetime, timezone

from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    DateTime,
)
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)

    # Stores bcrypt hash
    hashed_password = Column(String, nullable=False)

    # "admin" or "user"
    role = Column(String, nullable=False, default="user")

    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    notes = relationship(
        "Note",
        back_populates="user",
        cascade="all, delete-orphan",
    )


class Note(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    priority = Column(Integer, nullable=False)

    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    user = relationship(
        "User",
        back_populates="notes",
    )