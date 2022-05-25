import logging
import json
from flask import Flask
from flask import jsonify
from flask import session
from flask import request
from flask import render_template
from flask_cors import CORS
from flask_cors import cross_origin
# from flask.ext.session import Session
from db_wrapper import DbWrapper
from cart import Cart

app = Flask(__name__, static_folder="./static")
# cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
# SESSION_TYPE = 'filesystem'
# Session(app)
app.secret_key = "jkas90d3jw2e9qwndjklaq09wdasjlnkdasidadASKDASD321"

db_wrapper = DbWrapper()


@app.route("/robots.txt")
def robots():
    return render_template("robots.txt")


@app.route('/new-cart', methods=['POST', 'GET'])
def new_cart():
    session['cart'] = Cart().serialized()
    return {"result": "OK"}


@app.route('/cart', methods=['POST', 'GET'])
def cart():
    c = Cart.from_session(session)
    # return jsonify([i.serialized() for i in Cart().from_session(session).items])
    return render_template("cart.html", cart=c)


@app.route('/add-to-cart/<string:product_id>', methods=['POST', 'GET'])
def add_to_cart(product_id):
    product = db_wrapper.get_product(product_id)
    if not product:
        return {"result": "KO"}
    c = Cart.from_session(session)
    c.add_item(product)
    session['cart'] = c.serialized()
    return {"result": "OK"}


@app.route("/")
def index():
    c = Cart.from_session(session)
    cats = db_wrapper.get_categories()
    cat = request.args.get("cat")
    products = db_wrapper.get_products_by_cat(cat) if cat else db_wrapper.get_products()
    return render_template("index.html", cats=cats, cat=cat, keyrings=products, cart=c)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
