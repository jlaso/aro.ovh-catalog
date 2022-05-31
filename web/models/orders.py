from flask_sqlalchemy import SQLAlchemy as db


class Order(db):
    id = db.Column(db.Integer, primary_key=True)
    order_name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return '<Order %r>' % self.id
