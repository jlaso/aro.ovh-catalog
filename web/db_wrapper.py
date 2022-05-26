import json
from time import time
from product import Product

MAX_CACHE_TIME_SEC = 3600


class DbWrapper:

    def __init__(self):
        self.products = None
        self.last_read_products = None
        self.categories = None
        self.last_read_categories = None

    def get_categories(self):
        if self.categories is None or self.last_read_categories is None\
                or self.last_read_categories > time() + MAX_CACHE_TIME_SEC:
            with open("./db/categories.json") as c:
                self.categories = json.loads(c.read())
                self.last_read_categories = time()
        return self.categories

    def get_products(self):
        if self.products is None or self.last_read_products is None \
                or self.last_read_products > time() + MAX_CACHE_TIME_SEC:
            with open(f"./db/keyrings.json") as k:
                self.products = [p for p in json.loads(k.read()) if p.get('enabled', 1) > 0]
                self.last_read_products = time()
        return self.products

    def get_product(self, code: str):
        for p in self.get_products():
            if p['code'] == code:
                return Product.unserialize(p)

    def get_products_by_cat(self, cat: str):
        return [p for p in self.get_products() if p['cat'] == cat]
