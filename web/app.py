import logging
import json
from flask import Flask
from flask import redirect
from flask import jsonify
from flask import session
from flask import request
from flask import render_template
from flask_cors import CORS
from flask_cors import cross_origin
from flask_mail import Mail
from flask_mail import Message
from db_wrapper import DbWrapper
from cart import Cart

app = Flask(__name__, static_folder="./static")
# cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
# SESSION_TYPE = 'filesystem'
# Session(app)
app.secret_key = "jkas90d3jw2e9qwndjklaq09wdasjlnkdasidadASKDASD321"

db_wrapper = DbWrapper()

app.config['MAIL_SERVER'] = 'email-smtp.eu-west-3.amazonaws.com'
app.config['MAIL_PORT'] = 25
app.config['MAIL_USERNAME'] = 'AKIA2ZANDEU6ONU4N6UU'
app.config['MAIL_PASSWORD'] = 'BJ6H1y3Dcmn75SjIVL+f2c9nFtWAVWDu7QolwVuJj8ns'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

mail = Mail(app)


@app.route("/robots.txt")
def robots():
    msg = Message('Hello there', sender = 'info@muw.es', recipients = ['wld1373@gmail.com'])
    msg.body = "This is the email body"
    mail.send(msg)
    return render_template("robots.txt")


@app.route('/new-cart', methods=['POST', 'GET'])
def new_cart():
    session['cart'] = Cart().serialized()
    return {"result": "OK"}


@app.route('/cart', methods=['POST', 'GET'])
def cart():
    cats = db_wrapper.get_categories()
    if request.method == 'POST':
        if request.form.get('new_cart','') == 'Borrar':
            Cart().to_session(session)
    c = Cart.from_session(session)      
    return render_template("cart.html", cart=c, cats=cats, cat="cart")


@app.route('/add-to-cart/<string:product_id>', methods=['POST', 'GET'])
def add_to_cart(product_id):
    _redirect = request.args.get('redirect')
    product = db_wrapper.get_product(product_id)
    c = Cart.from_session(session)
    if product:
        c.add_item(product)
        c.to_session(session)
    return redirect(_redirect) if _redirect else {"result": bool(product), "count": len(c.items)}


@app.route('/product/<string:product_id>', methods=['GET'])
def product(product_id):
    cats = db_wrapper.get_categories()
    c = Cart.from_session(session)      
    product = db_wrapper.get_product(product_id)
    return render_template("single-product.html", product=product, cart=c, cats=cats, cat=product.cat)


@app.route("/")
def index():
    c = Cart.from_session(session)
    cats = db_wrapper.get_categories()
    cat = request.args.get("cat")
    products = db_wrapper.get_products_by_cat(cat) if cat else db_wrapper.get_products()
    return render_template("index.html", cats=cats, cat=cat, keyrings=products, cart=c)


if __name__ == "__main__":       
    app.run(host="0.0.0.0", port=5000)
