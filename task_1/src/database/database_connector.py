import psycopg2
from src.database.database_queries import create_cart_table, create_item_table, create_cart, \
    create_item, update_item, get_item


class DatabaseConnector:
    def __init__(self, db_name, db_user, password, host, init_db=True):
        self.connection = psycopg2.connect("dbname={} user={} password={} host={}".format(db_name, db_user, password, host))
        self.cursor = self.connection.cursor()
        if init_db:
            self.initialize_database()

    def close_connection(self):
        self.cursor.close()
        self.connection.close()

    def initialize_database(self):
        self.cursor.execute(create_cart_table)
        self.cursor.execute(create_item_table)
        self.commit_changes()

    def create_cart(self, cart_id):
        self.cursor.execute(create_cart.format(cart_id))

    def create_item(self, external_id, name, value, cart_id):
        self.cursor.execute(create_item.format(external_id, name, value, cart_id))

    def update_item(self, external_id, name, value, cart_id):
        self.cursor.execute(update_item.format(name, value, external_id, cart_id))

    def get_item(self, external_id, cart_id):
        self.cursor.execute(get_item.format(external_id, cart_id))
        return self.cursor.fetchone()

    def commit_changes(self):
        self.connection.commit()
