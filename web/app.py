from functools import wraps
from flask import g
from flask import url_for
from flask import Flask
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask_mail import Mail
from flask_mail import Message
from flask_sqlalchemy import SQLAlchemy

from cart import Cart
from config import ENV
from config import TheConfig
from jdb_wrapper import json_wrapper
from models import db

app = Flask(__name__, static_folder="./static")
# cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
app.config.from_object(TheConfig)
mail = Mail(app)
db.init_app(app)


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.user is None:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function


def common_vars_injector(incl_products=False):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            _cart = Cart.from_session(session)
            if _cart.how_old() > 3600:
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


@app.route("/robots.txt")
def robots():
    return render_template("robots.txt")


@app.route('/new-cart', methods=['POST', 'GET'])
def new_cart():
    session['cart'] = Cart().serialized()
    return {"result": "OK"}


@app.route('/order', methods=['POST', 'GET'])
@common_vars_injector()
def order(cart, **kwargs):
    if request.method == "POST":
        msg = Message('Nuevo pedido desde catalog.muw.es', sender='catalog@muw.es',
                      recipients=[TheConfig.DEST_EMAIL_ORDERS])
        msg.body = ""
        msg.html = render_template('emails/order.html',
                                   name=TheConfig.DEST_EMAIL_ORDERS,
                                   reminder_number=len(cart.items),
                                   items=cart.items,
                                   author_name="Automático",
                                   author_title="catalog@muw.es",
                                   APP_NAME="CATALOG.MUW.ES",
                                   APP_URL="https://catalog.muw.es/",
                                   TITLE="Reminder Email")
        mail.send(msg)
    kwargs["cat"] = "thanks"
    return render_template("thanks.html", cart=cart, **kwargs)


@app.route('/cart', methods=['POST', 'GET'])
@common_vars_injector()
def cart(**kwargs):
    if request.method == 'POST':
        if request.form.get('new_cart'):
            Cart().to_session(session)
        elif request.form.get('proceed'):
            return redirect('/order')
        elif request.form.get('update_cart'):
            c = kwargs["cart"]
            for i, item in enumerate(c.items):
                item.custom = request.form.get(f"custom[{i}]")
            c.to_session(session)
            return redirect("/cart")
    kwargs["cat"] = "cart"
    return render_template("cart.html", is_old="is_old" in request.args, **kwargs)


@app.route('/add-to-cart/<string:product_id>', methods=['POST', 'GET'])
def add_to_cart(product_id):
    _redirect = request.args.get('redirect')
    _product = json_wrapper.get_product(product_id)
    c = Cart.from_session(session)
    if product:
        c.add_item(_product)
        c.to_session(session)
    return redirect(_redirect) if _redirect else {"result": bool(_product), "count": len(c.items)}


@app.route('/product/<string:product_id>', methods=['GET'])
@common_vars_injector()
def product(product_id, **kwargs):
    _product = json_wrapper.get_product(product_id)
    kwargs["cat"] = _product.cat
    return render_template("single-product.html", product=_product, **kwargs)


@app.route("/")
@common_vars_injector(incl_products=True)
def index(**kwargs):
    return render_template("index.html", **kwargs)

# def get_common_vars(incl_products=False, cat=None):
#     if cat is None:
#         cat = request.args.get("cat")
#     result = {
#         "cart": Cart.from_session(session),
#         "cats": json_wrapper.get_categories(),
#         "cat": cat,
#         "product_code": request.args.get("product"),
#     }
#     if incl_products:
#         result["products"] = json_wrapper.get_products_by_cat(cat) if cat else json_wrapper.get_products()
#     return result
#


def __create_db():
    app.app_context().push()
    db.init_app(app)
    db.create_all()
    from models import Order
    from datetime import datetime
    db.session.add(Order(id=1, name="uno", date=datetime.now(), email="uno@gmail.com"))
    db.session.commit()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5080)
