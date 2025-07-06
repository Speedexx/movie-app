from .. import db

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    genre = db.Column(db.String(50), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    image = db.Column(db.String(120), nullable=True)  # Kolumna do przechowywania nazwy pliku zdjęcia
    description = db.Column(db.String(500))  # Opis filmu
    comments = db.relationship('Comment', backref='movie_comments', lazy=True)  # Zmieniona nazwa backref
    ratings = db.relationship('Rating', backref='movie_ratings', lazy=True)  # Nowa relacja

    def __repr__(self):
        return f"<Movie {self.title}>"

    def average_rating(self):
        if len(self.movie_ratings) > 0:
            total_ratings = sum([rating.rating for rating in self.movie_ratings])
            return total_ratings / len(self.movie_ratings)
        return 0
