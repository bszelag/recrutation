import pytest
import requests
import psycopg2

from .config import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, \
    ITEM_ENDPOINT_URL, HEADERS, ADD_NEW_CART_BODY


@pytest.fixture("session")
def cart_id():
    resp = requests.post(ITEM_ENDPOINT_URL,
                         data=ADD_NEW_CART_BODY,
                         headers=HEADERS)
    cookie = resp.cookies['cart_id']
    return cookie


@pytest.fixture(scope="session")
def database_connection():
    database_connection = psycopg2.connect(
        "dbname={} user={} password={} host={}"
        .format(DB_NAME, DB_USER, DB_PASSWORD, DB_HOST))
    return database_connection.cursor()
