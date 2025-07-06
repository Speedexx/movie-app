from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
import secrets
from flask_assets import Environment, Bundle

db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = secrets.token_hex(16)  # Generowanie losowego klucza sekretnego
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movies.db'  # Ścieżka do bazy danych
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Wyłączenie dodatkowych powiadomień

    # Assets (SCSS kompilacja)
    assets = Environment(app)
    scss = Bundle('scss/main.scss',
                  filters='libsass',
                  output='css/main.css')
    assets.register('scss_all', scss)
    scss.build()

    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    login_manager.login_message = None

    from app.models.user import User

    login_manager.login_view = "main.login"

    # Funkcja ładowania użytkownika
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Rejestracja blueprintu
    from .routes import main
    app.register_blueprint(main)

    from app.movie_management import movie_bp
    app.register_blueprint(movie_bp)

    return app
