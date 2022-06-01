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
from db_wrapper import DbWrapper
from models import db

app = Flask(__name__, static_folder="./static")
# cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
app.config.from_object(TheConfig)
db_wrapper = DbWrapper()
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
    msg = Message('Hello there', sender='catalog@muw.es', recipients=['wld1373@gmail.com'])
    msg.body = ""
    msg.html = render_template('emails/order.html',
                               name="Desmond",
                               reminder_number=len(c.items),
                               items=c.items,
                               author_name="Test Machine",
                               author_title="Tester",
                               APP_NAME="WhatIDoNow",
                               APP_URL="https://www.whatidonow.com/",
                               unsubscribe_url="https://www.whatidonow.com/unsubsribe/xxx",
                               TITLE="Reminder Email")
    mail.send(msg)
    return render_template("thanks.html", cart=c)


@app.route('/cart', methods=['POST', 'GET'])
def cart():
    cats = db_wrapper.get_categories()
    if request.method == 'POST':
        if request.form.get('new_cart', '') == 'Borrar':
            Cart().to_session(session)
        if request.form.get('proceed', '') == 'Pedir':
            return redirect('/order')
    c = Cart.from_session(session)
    return render_template("cart.html", cart=c, cats=cats, cat="cart")


@app.route('/add-to-cart/<string:product_id>', methods=['POST', 'GET'])
def add_to_cart(product_id):
    _redirect = request.args.get('redirect')
    _product = db_wrapper.get_product(product_id)
    c = Cart.from_session(session)
    if product:
        c.add_item(_product)
        c.to_session(session)
    return redirect(_redirect) if _redirect else {"result": bool(_product), "count": len(c.items)}


@app.route('/product/<string:product_id>', methods=['GET'])
def product(product_id):
    cats = db_wrapper.get_categories()
    c = Cart.from_session(session)
    _product = db_wrapper.get_product(product_id)
    return render_template("single-product.html", product=_product, cart=c, cats=cats, cat=product.cat)


@app.route("/")
def index():
    c = Cart.from_session(session)
    cats = db_wrapper.get_categories()
    cat = request.args.get("cat")
    products = db_wrapper.get_products_by_cat(cat) if cat else db_wrapper.get_products()
    return render_template("index.html", cats=cats, cat=cat, keyrings=products, cart=c)


def __create_db():
    app.app_context().push()
    db.init_app(app)
    db.create_all()
    from models import Order
    from datetime import datetime
    db.session.add(Order(id=1, name="uno", date=datetime.now(), email="uno@gmail.com"))
    db.session.commit()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
