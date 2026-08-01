from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from config import DATABASE_URL

engine=create_engine(DATABASE_URL)

SessionLocal=sessionmaker(autocommit=False,autoflush=False,bind=engine,expire_on_commit=True)
# After commit(), SQLAlchemy "forgets" the values inside db_note
# (this is called expire_on_commit)(it is TRUE by default)
# refresh() asks the database for the latest values and fills db_note again,
# so we can return it with all its data instead of {}.
#or use db.refresh(db_note) 

def get_db():
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()