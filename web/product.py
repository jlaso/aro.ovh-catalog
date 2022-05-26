import json


class Product:

    def __init__(self, code: str, cat: str, custom: str = "", name: str = ""):
        self.code = code
        self.cat = cat
        self.custom = custom
        self.name = name

    @staticmethod
    def from_db(p: dict):
        try:
            prod = Product(p['code'], p['cat'], p.get('custom', ''))
        except KeyError:
            prod = None
        return prod

    def serialized(self):
        return {
            "code": self.code,
            "custom": self.custom,
            "cat": self.cat,
            "name": self.name
        }

    @staticmethod    
    def unserialize(p: dict):
        code = p.get('code','')
        cat = p.get('cat','')
        name = p.get('name','')
        custom = p.get('custom','')
        return Product(code, cat, custom, name)
