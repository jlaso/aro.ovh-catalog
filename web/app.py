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
from jdb_wrapper import JdbWrapper
from models import db

app = Flask(__name__, static_folder="./static")
# cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
app.config.from_object(TheConfig)
json_wrapper = JdbWrapper()
mail = Mail(app)
db.init_app(app)


@app.route("/robots.txt")
def robots():
    return render_template("robots.txt")


@app.route('/new-cart', methods=['POST', 'GET'])
def new_cart():
    session['cart'] = Cart().serialized()
    return {"result": "OK"}


@app.route('/order', methods=['POST', 'GET'])
def order():
    c = Cart().from_session(session)
    cats = json_wrapper.get_categories()
    if request.method == "POST":
        msg = Message('Nuevo pedido desde catalog.muw.es', sender='catalog@muw.es',
                      recipients=[TheConfig.DEST_EMAIL_ORDERS])
        msg.body = ""
        msg.html = render_template('emails/order.html',
                                   name=TheConfig.DEST_EMAIL_ORDERS,
                                   reminder_number=len(c.items),
                                   items=c.items,
                                   author_name="Automático",
                                   author_title="catalog@muw.es",
                                   APP_NAME="CATALOG.MUW.ES",
                                   APP_URL="https://catalog.muw.es/",
                                   TITLE="Reminder Email")
        mail.send(msg)
    return render_template("thanks.html", **get_common_vars(cat="thanks"))


@app.route('/cart', methods=['POST', 'GET'])
def cart():
    if request.method == 'POST':
        if request.form.get('new_cart', ''):
            Cart().to_session(session)
        elif request.form.get('proceed', ''):
            return redirect('/order')
        elif request.form.get('update_cart', ''):
            c = Cart.from_session(session)
            for i, item in enumerate(c.items):
                item.custom = request.form.get(f"custom[{i}]")
            c.to_session(session)
    return render_template("cart.html", **get_common_vars(cat="cart"))


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
def product(product_id):
    _product = json_wrapper.get_product(product_id)
    return render_template("single-product.html", product=_product,
                           **get_common_vars(cat=_product.cat))


@app.route("/")
def index():
    return render_template("index.html", **get_common_vars(incl_products=True))


def get_common_vars(incl_products=False, cat=None):
    if cat is None:
        cat = request.args.get("cat")
    result = {
        "cart": Cart.from_session(session),
        "cats": json_wrapper.get_categories(),
        "cat": cat,
        "product_code": request.args.get("product"),
    }
    if incl_products:
        result["products"] = json_wrapper.get_products_by_cat(cat) if cat else json_wrapper.get_products()
    return result


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
