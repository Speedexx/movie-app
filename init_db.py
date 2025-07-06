from app import create_app, db
from app.models import User

app = create_app()

with app.app_context():
    # Tworzenie wszystkich tabel w bazie danych
    db.create_all()
    print("Wszystkie tabele zostały utworzone!")

    # Opcjonalnie: Możesz dodać domyślnego admina, jeśli chcesz to zrobić od razu
    from werkzeug.security import generate_password_hash

    admin = User.query.filter_by(role='admin').first()
    if not admin:
        print("Admin nie istnieje, tworzymy go...")
        admin = User(username='admin', email='admin@admin.com', password=generate_password_hash('admin123'), role='admin')
        db.session.add(admin)
        db.session.commit()
        print("Admin user created!")
    else:
        print("Admin już istnieje!")
