import cProfile
import io
import pstats

import MySQLdb
from config import DEST_DB_NAME, DEST_DB_PASSWORD, DEST_DB_USER, DB_NAME, \
    DB_PASSWORD, DB_USER, DEST_DB_HOST, DB_HOST, SAVE_TITLES_TO_CSV, \
    LOAD_TITLES_FROM_CSV


class DatabaseConnector:
    def __init__(self, host, user, password, db):
        self.connection = MySQLdb.connect(user=user, password=password,
                                          host=host, db=db)
        self.cursor = self.connection.cursor()

    def commit_changes(self):
        self.connection.commit()

    def copy_titles(self, dest_db):
        self.cursor.execute(SAVE_TITLES_TO_CSV)
        self.commit_changes()
        dest_db.cursor.execute(LOAD_TITLES_FROM_CSV)
        dest_db.commit_changes()


def main():
    src_db = DatabaseConnector(DB_HOST, DB_USER, DB_PASSWORD, DB_NAME)
    dest_db = DatabaseConnector(DEST_DB_HOST, DEST_DB_USER,
                                DEST_DB_PASSWORD, DEST_DB_NAME)

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
