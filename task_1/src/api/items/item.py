from .items_utils import create_item


class Item(object):

    def on_post(self, req, resp):
        resp.status = create_item(req, resp)
