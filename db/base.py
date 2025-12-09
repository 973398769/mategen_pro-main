# -*- coding: utf-8 -*-
"""
Author: MuYu_Cheney
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy.exc import SQLAlchemyError

from config.config import SQLALCHEMY_DATABASE_URI

# Create engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URI,
    echo=True,
    pool_size=10,  # Set connection pool size to 10
    max_overflow=20  # Maximum overflow connections: 20
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False,
                            autoflush=False,
                            bind=engine)

# Create Base class
Base = declarative_base()


# Get database session
def get_db():
    """
    1. When the function is called, it creates a database session db = SessionLocal().
    2. Program execution pauses, yield db returns the session object db to the caller, who can interact with the database through this object.
    3. After database interaction is complete, control returns to the finally block, calling db.close() to close the database session and release connection resources.
    """
    db = SessionLocal()
    try:
        yield db
    except SQLAlchemyError as e:
        print(f"Database error: {e}")
        db.rollback()  # If an error occurs, rollback the transaction
    finally:
        db.close()
