from flask import g
from flask import request
from flask import session
from flask import redirect
from flask import url_for
from functools import wraps
from cart import Cart
from jdb_wrapper import json_wrapper


def common_vars_injector(incl_products=False):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            _cart = Cart.from_session(session)
            # for avoiding infinite redirects
            if not request.path.startswith('/cart?is_old') \
                    and _cart.how_old() > 3600 * 24:
                return redirect("/cart?is_old")
            kwargs = {
                "cat": request.args.get("cat"),
                "cart": _cart,
                "cats": json_wrapper.get_categories(),
                "product_code": request.args.get("product"),
            }
            if incl_products:
                kwargs["products"] = json_wrapper.get_products_by_cat(kwargs["cat"]) \
                    if kwargs["cat"] else json_wrapper.get_products()
            return f(*args, **kwargs)
        return wrapper
    return decorator


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.user is None:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function
