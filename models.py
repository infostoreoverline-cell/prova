from flask_login import UserMixin
from extensions import db, login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    bookings = db.relationship('Booking', backref='customer', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(100), nullable=False)
    product_type = db.Column(db.String(50), nullable=False) # e.g., 'table', 'pulley'
    details = db.Column(db.String(200), nullable=True) # e.g., "Color: Matte Black, Frame: Portable"
    price = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Booking('{self.product_name}', '{self.price}')"
