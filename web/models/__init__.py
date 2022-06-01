from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    date = db.Column(db.DateTime(), nullable=False)

    def __repr__(self):
        return '<Order %r>' % self.id


class OrderLine(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    order = db.relationship('Order', backref=db.backref('lines', lazy=True))
    product_code = db.Column(db.String(4), nullable=False)
    quantity = db.Column(db.Integer)
    custom = db.Column(db.String(180), nullable=True)

    def __repr__(self):
        return '<OrderLine %r>' % self.id
