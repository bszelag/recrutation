from tests.config import GET_ALL_TITLES_QUERY


def test_copied_titles(src_database_connector, dest_database_connector):
    titles_from_first_db = src_database_connector.cursor.execute(
        GET_ALL_TITLES_QUERY)
    titles_from_second_db = dest_database_connector.cursor.execute(
        GET_ALL_TITLES_QUERY)
    assert titles_from_first_db == titles_from_second_db
