from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

from fastapi import HTTPException, Body
from sqlalchemy.exc import SQLAlchemyError
from pydantic import BaseModel
from sqlalchemy import create_engine, text
import logging
from db.base_model import DbBase

"""
Official documentation: https://docs.sqlalchemy.org/en/20/dialects/mysql.html
"""

# Used to create a base class that will provide the foundation for SQLAlchemy ORM functionality for all subsequently defined model classes.
Base = declarative_base()


class DBConfig(BaseModel):
    hostname: str
    port: str
    username: str
    password: str
    database_name: str


def get_engine(db_config: DBConfig):
    uri = f"mysql+pymysql://{db_config.username}:{db_config.password}@{db_config.hostname}:{db_config.port}/{db_config.database_name}?charset=utf8mb4"
    engine = create_engine(uri, echo=True)
    return engine


SessionLocal = sessionmaker(autocommit=False, autoflush=False)


def test_database_connection(db_config: DBConfig):
    """
    Create a database connection. If connection is successful, return all database names and corresponding table names under this connection (excluding system preset databases)
    :param db_config:
    :return:
    """

    uri = f"mysql+pymysql://{db_config.username}:{db_config.password}@{db_config.hostname}:{db_config.port}/{db_config.database_name}?charset=utf8mb4"
    engine = create_engine(uri, echo=True)

    SessionLocal.configure(bind=engine)
    session = SessionLocal()

    try:
        with engine.connect() as conn:
            conn.execute(text(f"USE `{db_config.database_name}`;"))
            tables = conn.execute(text("SHOW TABLES;"))
            table_list = [table[0] for table in tables]
        session.close()
        return table_list  # Directly return table list
    except SQLAlchemyError as e:
        session.close()
        raise HTTPException(status_code=400, detail=f"Database connection failed: {str(e)}")
    except Exception as e:
        session.close()
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")



def insert_db_config(db_config: DBConfig):
    """
    Insert a new database connection configuration record into the database and return the generated UUID.
    :param session: SQLAlchemy Session object for database operations
    :param hostname: Database server hostname
    :param port: Database server port
    :param username: Username for connecting to the database
    :param password: Password for connecting to the database
    :param database_name: Name of the database to connect to
    :return: UUID of successfully inserted configuration, or None if an error occurs
    """
    from config.config import SQLALCHEMY_DATABASE_URI
    engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=True)
    SessionLocal.configure(bind=engine)
    session = SessionLocal()

    try:
        # Test database connection
        test_database_connection(db_config)  # If connection fails, will throw an exception

        # Check if the same configuration already exists in the database
        existing_config = session.query(DbBase).filter(
            DbBase.hostname == db_config.hostname,
            DbBase.port == db_config.port,
            DbBase.username == db_config.username,
            DbBase.password == db_config.password,
            DbBase.database_name == db_config.database_name
        ).first()

        if existing_config:
            # If existing configuration is found, do not perform insert operation
            session.close()
            raise HTTPException(status_code=400, detail="Identical database configuration already exists, insertion rejected")

        new_db_config = DbBase(
            hostname=db_config.hostname,
            port=db_config.port,
            username=db_config.username,
            password=db_config.password,
            database_name=db_config.database_name
        )
        session.add(new_db_config)
        session.commit()
        return str(new_db_config.id)  # Return UUID string
    except HTTPException as http_ex:
        session.rollback()
        session.close()
        raise http_ex  # Re-raise the captured HTTPException
    except Exception as e:
        session.rollback()
        session.close()
        raise HTTPException(status_code=500, detail=f"Data insertion failed: {str(e)}")


def update_db_config(db_info_id: str, new_config: DBConfig):
    from config.config import SQLALCHEMY_DATABASE_URI
    engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=True)

    SessionLocal.configure(bind=engine)
    session = SessionLocal()

    try:
        # Test new database connection
        test_database_connection(new_config)  # If connection fails, will throw an exception

        # Find existing configuration record
        db_config = session.query(DbBase).filter(DbBase.id == db_info_id).first()
        if db_config:
            # Update configuration
            db_config.hostname = new_config.hostname
            db_config.port = new_config.port
            db_config.username = new_config.username
            db_config.password = new_config.password
            db_config.database_name = new_config.database_name

            session.commit()  # Commit changes
            return True
        else:
            return False
    except HTTPException as http_ex:
        session.rollback()
        raise http_ex  # Re-throw HTTPException, handled by upper layer
    except Exception as e:
        session.rollback()  # Rollback all changes in case of exception
        raise HTTPException(status_code=500, detail=f"Database operation failed: {str(e)}")
    finally:
        session.close()


def get_all_databases():
    from config.config import SQLALCHEMY_DATABASE_URI
    engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=True)

    SessionLocal.configure(bind=engine)
    session = SessionLocal()
    try:
        # Query all database configurations, selecting only id and database_name
        db_configs = session.query(DbBase.id, DbBase.database_name).order_by(DbBase.created_at.desc()).all()
        # Format query results into a list of dictionaries
        result = [{"id": config.id, "database_name": config.database_name} for config in db_configs]
        session.close()
        return result
    except Exception as e:
        session.close()
        raise Exception(f"Failed to retrieve database configurations: {str(e)}")

def delete_db_config(db_info_id: str):
    from config.config import SQLALCHEMY_DATABASE_URI
    engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=True)

    SessionLocal.configure(bind=engine)
    session = SessionLocal()
    try:
        # Find the database configuration object to delete
        db_config = session.query(DbBase).filter(DbBase.id == db_info_id).first()
        if db_config is None:
            session.close()
            return False  # If object not found, return False indicating unable to delete

        # Delete the found object and commit changes
        session.delete(db_config)
        session.commit()
        return True  # Return True indicating successful deletion
    except Exception as e:
        session.rollback()  # Rollback on error
        raise Exception(f"Failed to delete database configuration: {str(e)}")
    finally:
        session.close()


def get_db_config_by_id(db_info_id: str):
    """
    Get configuration information from the database by ID and return as DBConfig model.
    """

    from config.config import SQLALCHEMY_DATABASE_URI
    engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=True)

    SessionLocal.configure(bind=engine)
    session = SessionLocal()

    db_info = session.query(DbBase).filter(DbBase.id == db_info_id).first()

    if db_info:
        return {key: value for key, value in db_info.__dict__.items() if not key.startswith('_')}
    else:
        return None
