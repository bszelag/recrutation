import falcon

from .api.items.item import Item

api = application = falcon.API()
api.add_route('/item', Item())
