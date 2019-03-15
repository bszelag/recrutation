from src.database.database_connector import DatabaseConnector
import os

DB_NAME = os.getenv("POSTGRES_DB")
DB_USER = os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB_HOST = os.getenv("POSTGRES_HOST")

database_connector = DatabaseConnector(DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, False)
