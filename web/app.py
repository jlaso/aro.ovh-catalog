import logging
import json
from flask import Flask, jsonify
from flask import request
from flask import render_template
from flask_cors import CORS, cross_origin

app = Flask(__name__, static_folder="./static")
# cors = CORS(app, resources={r"/api/*": {"origins": "*"}})


@app.route("/robots.txt")
def robots():
    return render_template("robots.txt")


@app.route("/")
def index():
    with open("./db/categories.json") as c:
        cats = json.loads(c.read())
    cat = request.args.get("cat")
    keyrings = []
    with open(f"./db/keyrings.json") as k:
        keyrings = json.loads(k.read())
        if cat:
            keyrings = [k for k in keyrings if k['cat'] == cat]
    return render_template("index.html", cats=cats, cat=cat, keyrings=keyrings)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
