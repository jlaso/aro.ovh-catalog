import json


class Product:

    def __init__(self, product_id: str, cat: str, custom: str = ""):
        self.product_id = product_id
        self.cat = cat
        self.custom = custom

    @staticmethod
    def from_db(p: dict):
        try:
            prod = Product(p['code'], p['cat'], p.get('custom', ''))
        except KeyError:
            prod = None
        return prod

    def serialized(self):
        return {
            "code": self.product_id,
            "custom": self.custom,
            "cat": self.cat
        }
