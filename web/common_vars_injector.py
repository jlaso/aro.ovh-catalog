from flask import session
from cart import Cart
from jdb_wrapper import json_wrapper


def common_vars_injector(request, **kwargs):
    def wrapper(func):
        data = {
            "cat": request.args.get("cat"),
            "cart": Cart.from_session(session),
            "cats": json_wrapper.get_categories(),
            "product_code": request.args.get("product"),
        }
        if kwargs.get("incl_products", ""):
            data["products"] = json_wrapper.get_products_by_cat(data["cat"]) \
                if data["cat"] else json_wrapper.get_products()
        return func(**data)
    return wrapper

