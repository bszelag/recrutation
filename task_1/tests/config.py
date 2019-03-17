import os

DB_NAME = os.getenv("POSTGRES_DB")
DB_USER = os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB_HOST = os.getenv("POSTGRES_HOST_ADDRESS", "127.0.0.1")

ITEM_ENDPOINT_URL = os.getenv("ITEM_ENDPOINT_URL",
                              "http://localhost:5000/item")
HEADERS = {"content-type": "application/json"}

ADD_NEW_CART_BODY = "{\"name\":\"item\",\"value\":22," \
                    "\"external_id\":\"item_id\"}"
ADD_NEW_ITEM_BODY = "{\"name\":\"new_item\",\"value\":150," \
                    "\"external_id\":\"new_item_id\"}"
UPDATE_ITEM_BODY = "{\"name\":\"new_item\",\"value\":180," \
                   "\"external_id\":\"new_item_id\"}"
ADD_NEW_ITEM_WO_VALUE_BODY = "{\"name\":\"item_wo_value\"," \
                             "\"external_id\":\"item_wo_value_id\"}"
ADD_NEW_ITEM_WO_ID_BODY = "{\"name\":\"item\",\"value\":22}"

ADD_ITEM_PARAMS = [ADD_NEW_ITEM_BODY,
                   UPDATE_ITEM_BODY,
                   ADD_NEW_ITEM_WO_VALUE_BODY]

ITEM_ID_NEW_CART = "item_id"
ITEM_ID_EXISTING_CART = "new_item_id"

GET_CART = "SELECT id FROM cart WHERE id=\'{}\';"
GET_CART_ITEM = "SELECT external_id, name, value " \
                "FROM item WHERE cart_id=\'{}\' AND external_id=\'{}\';"
