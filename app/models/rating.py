from .. import db
from datetime import datetime

class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)  # Ocena w skali 1-5
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'), nullable=False)

    user = db.relationship('User', backref='user_ratings')  # Relacja z użytkownikiem
    movie = db.relationship('Movie', backref='movie_ratings')  # Relacja z filmem

    def __repr__(self):
        return f"<Rating {self.rating} for Movie {self.movie_id} by User {self.user_id}>"
