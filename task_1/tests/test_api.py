import json
import pytest
import requests
from .config import ITEM_ENDPOINT_URL, HEADERS, GET_CART, \
    GET_CART_ITEM, ADD_NEW_CART_BODY, ITEM_ID_NEW_CART, \
    ADD_NEW_ITEM_WO_ID_BODY, ADD_ITEM_PARAMS


def test_creating_new_cart_and_adding_item(database_connection):
    resp = requests.post(ITEM_ENDPOINT_URL,
                         data=ADD_NEW_CART_BODY,
                         headers=HEADERS)
    cart_id = resp.cookies['cart_id']
    assert resp.status_code == 204
    assert cart_id
    database_connection.execute(GET_CART.format(cart_id))
    assert database_connection.fetchone()
    database_connection.execute(GET_CART_ITEM
                                .format(cart_id, ITEM_ID_NEW_CART))
    assert database_connection.fetchone()


@pytest.mark.parametrize("query", ADD_ITEM_PARAMS)
def test_adding_new_item_to_existing_cart(query,
                                          cart_id,
                                          database_connection):
    item_id = json.loads(query)['external_id']
    cookies = dict(cart_id=cart_id)
    resp = requests.post(ITEM_ENDPOINT_URL,
                         data=query,
                         headers=HEADERS,
                         cookies=cookies)
    assert resp.status_code == 204
    database_connection.execute(GET_CART.format(cart_id))
    assert database_connection.fetchone()
    database_connection.execute(GET_CART_ITEM.format(cart_id, item_id))
    assert item_id in database_connection.fetchone()


def test_fail_adding_item_without_external_id(cart_id):
    cookies = dict(cart_id=cart_id)
    resp = requests.post(ITEM_ENDPOINT_URL,
                         data=ADD_NEW_ITEM_WO_ID_BODY,
                         headers=HEADERS,
                         cookies=cookies)
    assert resp.status_code == 400
