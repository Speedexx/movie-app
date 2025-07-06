from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
import os
from app import db
from app.models.movie import Movie
from flask_login import login_required, current_user
from app.forms import MovieForm

# Utworzenie Blueprint dla zarządzania filmami
movie_bp = Blueprint('movie', __name__)

# Ścieżka do zapisywania zdjęć
UPLOAD_FOLDER = 'app/static/img'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Dodawanie nowego filmu
@movie_bp.route('/add_movie', methods=['GET', 'POST'])
@login_required
def add_movie():
    form = MovieForm()

    if form.validate_on_submit():
        title = form.title.data
        genre = form.genre.data
        year = form.year.data
        description = form.description.data

        # Sprawdzanie, czy obrazek jest w formularzu
        if 'image' in request.files:
            image_file = request.files['image']
            if image_file and allowed_file(image_file.filename):
                filename = secure_filename(image_file.filename)
                image_file.save(os.path.join(UPLOAD_FOLDER, filename))
            else:
                filename = None
        else:
            filename = None

        # Dodanie filmu do bazy danych
        new_movie = Movie(
            title=title,
            genre=genre,
            year=year,
            image=filename,
            description=description
        )
        db.session.add(new_movie)
        db.session.commit()

        flash('Movie added successfully!', 'success')
        return redirect(url_for('main.movies'))

    return render_template('add_movie.html', form=form)


# Edytowanie filmu
@movie_bp.route('/edit_movie/<int:movie_id>', methods=['GET', 'POST'])
@login_required
def edit_movie(movie_id):
    movie = Movie.query.get_or_404(movie_id)

    form = MovieForm(request.form, obj=movie)

    if form.validate_on_submit():
        movie.title = form.title.data
        movie.genre = form.genre.data
        movie.year = form.year.data
        movie.description = form.description.data

        # Sprawdzanie, czy obrazek jest w formularzu
        if 'image' in request.files:
            image_file = request.files['image']
            if image_file and allowed_file(image_file.filename):
                filename = secure_filename(image_file.filename)
                image_file.save(os.path.join(UPLOAD_FOLDER, filename))
                movie.image = filename

        db.session.commit()
        flash('Movie updated successfully!', 'success')
        return redirect(url_for('main.movies'))

    return render_template('edit_movie.html', movie=movie, form=form)

# Usuwanie filmu
@movie_bp.route('/delete_movie/<int:movie_id>', methods=['POST'])
@login_required
def delete_movie(movie_id):
    movie = Movie.query.get_or_404(movie_id)

    # Usunięcie pliku z folderu statycznego
    if movie.image:
        os.remove(os.path.join(UPLOAD_FOLDER, movie.image))

    db.session.delete(movie)
    db.session.commit()

    flash('Movie deleted successfully!', 'success')
    return redirect(url_for('main.movies'))
