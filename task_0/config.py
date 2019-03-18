import os

DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")
DB_PORT = int(os.getenv("DB_PORT"))

DEST_DB_HOST = os.getenv("DEST_DB_HOST")
DEST_DB_USER = os.getenv("DEST_DB_USER")
DEST_DB_PASSWORD = os.getenv("DEST_DB_PASSWORD")
DEST_DB_NAME = os.getenv("DEST_DB_NAME")
DEST_DB_PORT = int(os.getenv("DEST_DB_PORT"))

SELECT_N_ROWS = "SELECT emp_no, title, CAST(from_date as CHAR(50)) as from_date, CAST(to_date AS CHAR(50)) as to_date FROM titles LIMIT {}, {};"  # noqa
INSERT_N_ROWS = "INSERT IGNORE INTO titles (emp_no, title, from_date, to_date) VALUES{};"  # noqa
GET_MAX_ALLOWED_PACKET = "SHOW VARIABLES LIKE 'max_allowed_packet';"
