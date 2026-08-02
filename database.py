from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from config import DATABASE_URL

# Create a SQLAlchemy engine for the configured database URL.
# pool_pre_ping=True ensures stale or closed connections are detected before use.
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
)

# SessionLocal returns a new session for each request.
# expire_on_commit=True means objects are cleared after commit, so refresh()
# is required to access up-to-date values after database writes.
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    expire_on_commit=True,
)

# After commit(), SQLAlchemy "forgets" the values inside db_note
# (this is called expire_on_commit)(it is TRUE by default)
# refresh() asks the database for the latest values and fills db_note again,
# so we can return it with all its data instead of {}.
# or use db.refresh(db_note)

def get_db():
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()