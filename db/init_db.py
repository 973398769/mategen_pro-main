# -*- coding: utf-8 -*-
"""
Author: MuYu_Cheney
"""

from sqlalchemy import create_engine, text
from config.config import username, password, hostname, database_name
from db.base import Base, engine, SessionLocal
from db.base_model import SecretModel, ThreadModel, KnowledgeBase, FileInfo, DbBase, MessageModel


# Check if database exists, and create database if needed
def create_database_if_not_exists(username: str, password: str, hostname: str, database_name: str):
    # Create an engine connection to the database (without specifying database name)
    engine_for_check = create_engine(f"mysql+pymysql://{username}:{password}@{hostname}?charset=utf8mb4")

    with engine_for_check.connect() as connection:
        # Execute SQL query to check if database exists
        result = connection.execute(text(f"SHOW DATABASES LIKE '{database_name}'"))
        if result.fetchone() is None:
            # Database doesn't exist, execute database creation
            connection.execute(
                text(f"CREATE DATABASE {database_name} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"))
            print(f"Database '{database_name}' created successfully.")
        else:
            print(f"Database '{database_name}' already exists.")


# Define database model initialization function
def initialize_database():
    try:
        # Check if database exists, if not, create it first
        create_database_if_not_exists(username, password, hostname, database_name)

        # Create all tables
        Base.metadata.create_all(engine)

    except Exception as e:
        print("Error occurred during database initialization:", e)
        return False


def delete_database():
    # Delete all tables
    Base.metadata.drop_all(engine)
    return True


if __name__ == '__main__':
    initialize_database()
    # delete_database()