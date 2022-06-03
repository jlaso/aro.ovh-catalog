import json
import time
from product import Product


class Cart:

    def __init__(self):
        self.items = []
        self.updated_at = int(time.time())

    @staticmethod
    def from_session(s):
        c = Cart()
        # print(json.loads(s.get("cart", "[]")))
        c.items = [Product.unserialize(p) for p in json.loads(s.get("cart", "[]"))]
        c.updated_at = int(s.get("cart.updated_at", "0"))
        # print(c.items)
        return c

    def to_session(self, s):
        s["cart"] = json.dumps([i.serialized() for i in self.items])
        self.updated_at = int(time.time())
        s["cart.updated_at"] = str(self.updated_at)

    def how_old(self):
        return int(time.time()) - self.updated_at

    def add_item(self, item: Product):
        self.items.append(item)

    def serialized(self):
        return json.dumps([i.serialized() for i in self.items])
