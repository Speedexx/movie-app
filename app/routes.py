from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, login_required, logout_user, current_user
from . import db
from app.models.movie import Movie
from app.models.user import User
from app.models.comment import Comment
from app.models.rating import Rating
from .forms import RegisterForm, LoginForm, CommentForm, RatingForm
from werkzeug.security import generate_password_hash, check_password_hash
import logging

main = Blueprint('main', __name__)
logging.basicConfig(level=logging.DEBUG)

# Logowanie
@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('main.index'))
        else:
            flash('Invalid username or password.', 'danger')
    return render_template('login_register.html',
                           title='Login',
                           form=form,
                           button_text='Login',
                           link_text="Don't have an account?",
                           link_url=url_for('main.register'),
                           link_label="Register here")

# Rejestracja
@main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(username=form.username.data).first()
        if existing_user:
            flash('Username already exists.', 'danger')
        else:
            hashed_password = generate_password_hash(form.password.data)
            new_user = User(
                username=form.username.data,
                email=form.email.data,
                password=hashed_password,
                role='user'
            )
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            flash('Account created and logged in successfully!', 'success')
            return redirect(url_for('main.index'))

    return render_template('login_register.html',
                           title='Register',
                           form=form,
                           button_text='Register',
                           link_text="Already have an account?",
                           link_url=url_for('main.login'),
                           link_label="Login here")


# Wylogowanie
@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out successfully.', 'info')  # Dodanie komunikatu
    return redirect(url_for('main.index'))


# Strona główna
@main.route('/')
@login_required  # Tylko dla zalogowanych użytkowników
def index():
    # Pobieramy wszystkie filmy z bazy
    movies = Movie.query.all()
    return render_template('index.html', movies=movies)


@main.route('/movies')
@login_required  # Tylko dla zalogowanych użytkowników
def movies():
    # Pobieranie wszystkich filmów z bazy danych
    movies = Movie.query.all()

    # Przekazywanie filmów do szablonu
    return render_template('movies.html', movies=movies)


@main.route('/manage_movies')
@login_required
def manage_movies():
    if current_user.role != 'admin':
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('main.index'))

    # Pobieranie wszystkich filmów z bazy
    movies = Movie.query.all()
    return render_template('manage_movies.html', movies=movies)


@main.route('/movie/<int:movie_id>', methods=['GET', 'POST'])
@login_required
def movie_details(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    comments = movie.movie_comments

    rating_form = RatingForm()
    comment_form = CommentForm()

    existing_rating = Rating.query.filter_by(user_id=current_user.id, movie_id=movie.id).first()

    # Obsługa formularza oceny
    if rating_form.submit_rating.data and rating_form.validate_on_submit():
        logging.debug(f"Formularz oceny przeszedł: {rating_form.rating.data}")

        if existing_rating:
            existing_rating.rating = rating_form.rating.data
            flash('Rating updated successfully!', 'success')
        else:
            new_rating = Rating(
                rating=rating_form.rating.data,
                user_id=current_user.id,
                movie_id=movie.id
            )
            db.session.add(new_rating)
            flash('Rating added successfully!', 'success')

        db.session.commit()
        return redirect(url_for('main.movie_details', movie_id=movie.id))

    # Obsługa formularza komentarza
    if comment_form.submit_comment.data and comment_form.validate_on_submit():
        logging.debug(f"Formularz komentarza przeszedł: {comment_form.content.data}")

        new_comment = Comment(
            content=comment_form.content.data,
            user_id=current_user.id,
            movie_id=movie.id
        )
        db.session.add(new_comment)
        db.session.commit()

        flash('Comment added successfully!', 'success')
        return redirect(url_for('main.movie_details', movie_id=movie.id))

    return render_template(
        'movie_details.html',
        movie=movie,
        comments=comments,
        form=comment_form,
        rating_form=rating_form,
        existing_rating=existing_rating
    )

@main.route('/my_activity')
@login_required
def my_activity():
    user_comments = Comment.query.filter_by(user_id=current_user.id).order_by(Comment.created_at.desc()).all()
    user_ratings = Rating.query.filter_by(user_id=current_user.id).order_by(Rating.created_at.desc()).all()

    return render_template(
        'my_activity.html',
        comments=user_comments,
        ratings=user_ratings
    )
