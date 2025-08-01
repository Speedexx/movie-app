from .. import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(50), nullable=False, default="user")  # admin or user

    def __repr__(self):
        return f'<User {self.username}>'

    # Dodajemy możliwość dodawania ocen
    ratings = db.relationship('Rating', backref='user_ratings', lazy=True)
