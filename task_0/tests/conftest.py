import pytest

from config import DEST_DB_NAME, DEST_DB_PASSWORD, DEST_DB_USER, DB_NAME, \
    DB_PASSWORD, DB_USER, DEST_DB_HOST, DB_HOST
from copy_titles_data import DatabaseConnector


@pytest.fixture(scope="function")
def src_database_connector():
    dbc = DatabaseConnector(DB_HOST, DB_USER, DB_PASSWORD, DB_NAME)
    return dbc


@pytest.fixture(scope="function")
def dest_database_connector():
    dbc = DatabaseConnector(DEST_DB_HOST, DEST_DB_USER, DEST_DB_PASSWORD,
                            DEST_DB_NAME)
    return dbc
