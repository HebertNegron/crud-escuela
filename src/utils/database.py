from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from os import environ as env
from sqlalchemy.ext.declarative import declarative_base

SQL_DATABASE_URL = f"mysql+mysqlconnector://{env['DB_USER']}:{env['DB_PASSWORD']}@{env['DB_HOST']}:{env['DB_PORT']}/{env['DB_NAME']}"

engine = create_engine(SQL_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()