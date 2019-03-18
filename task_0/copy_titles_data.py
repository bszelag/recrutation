import cProfile
import io
import pstats

import MySQLdb
from config import DEST_DB_NAME, DEST_DB_PASSWORD, DEST_DB_USER, DB_NAME, \
    DB_PASSWORD, DB_USER, DEST_DB_HOST, DB_HOST, SELECT_N_ROWS, \
    INSERT_N_ROWS, DEST_DB_PORT, DB_PORT, GET_MAX_ALLOWED_PACKET

QUERY_SIZE_WO_DATA = 82  # Length of query without passed data
MAX_SIZE_OF_DATA_FROM_ROW = 81  # 50(title) + 10(data) + 10(data) + 11(max int)


class DatabaseConnector:
    def __init__(self, host, user, password, db, port):
        self.connection = MySQLdb.connect(user=user, password=password,
                                          host=host, db=db, port=port)
        self.cursor = self.connection.cursor()

    def commit_changes(self):
        self.connection.commit()

    def copy_titles(self, dest_db):
        i = 0
        dest_db.cursor.execute(GET_MAX_ALLOWED_PACKET)
        n = (int(dest_db.cursor.fetchone()[1])
             - QUERY_SIZE_WO_DATA) // MAX_SIZE_OF_DATA_FROM_ROW
        n_rows = self.cursor.execute(SELECT_N_ROWS.format(i, n))
        while n_rows:
            titles = self.cursor.fetchall()
            prepared_titles_tuple = str(titles)[1:-1]
            my_cmd = INSERT_N_ROWS.format(prepared_titles_tuple)
            dest_db.cursor.execute(my_cmd)
            dest_db.commit_changes()
            n_rows = self.cursor.execute(SELECT_N_ROWS.format(i, n))
            i = i + n


def main():
    src_db = DatabaseConnector(DB_HOST, DB_USER, DB_PASSWORD, DB_NAME, DB_PORT)
    dest_db = DatabaseConnector(DEST_DB_HOST, DEST_DB_USER,
                                DEST_DB_PASSWORD, DEST_DB_NAME, DEST_DB_PORT)
    src_db.copy_titles(dest_db)


if __name__ == '__main__':
    profile = cProfile.Profile()
    profile.enable()
    main()
    profile.disable()
    s = io.StringIO()
    ps = pstats.Stats(profile, stream=s).sort_stats('cumulative')
    ps.print_stats()
    print(s.getvalue())
