import falcon
import json
import uuid

from src.api.config import database_connector


def create_item(req, resp):
    if req.content_length:
        try:
            cart_id = get_card_id(req, resp)
        except:
            database_connector.connection.rollback()
            return falcon.HTTP_500

        data = json.load(req.stream)
        try:
            if database_connector.get_item(data['external_id'], cart_id):
                database_connector.update_item(data['external_id'], data['name'], data['value'],
                                               cart_id)
            else:
                database_connector.create_item(data['external_id'], data['name'], data['value'],
                                               cart_id)
        except:
            database_connector.connection.rollback()
            return falcon.HTTP_500

        database_connector.commit_changes()
        return falcon.HTTP_204
    else:
        return falcon.HTTP_400


def get_card_id(req, resp):
    cookies = req.cookies
    if 'cart_id' in cookies:
        return cookies['cart_id']
    cart_id = str(uuid.uuid4())
    database_connector.create_cart(cart_id)
    resp.set_cookie(name='cart_id', value=cart_id, max_age=259200)
    database_connector.commit_changes()
    return cart_id
