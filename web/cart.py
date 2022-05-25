import json
from product import Product


class Cart:

    def __init__(self):
        self.items = []

    @staticmethod
    def from_session(s):
        c = Cart()
        print(json.loads(s.get("cart", "[]")))
        c.items = [Product.from_db(p) for p in json.loads(s.get("cart", "[]"))]
        return c

    def to_session(self, s):
        s["cart"] = json.dumps(self.items)

    def add_item(self, item: Product):
        self.items.append(item)

    def serialized(self):
        return json.dumps([i.serialized() for i in self.items])
