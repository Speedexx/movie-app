# Movie App

Aplikacja webowa umożliwiająca przeglądanie filmów oraz dodawanie opinii i ocen przez użytkowników.

## Wymagania

Aby uruchomić aplikację, musisz mieć zainstalowane następujące narzędzia:

- Python 3.x
- Docker (opcjonalnie, jeśli chcesz uruchomić aplikację za pomocą Dockera)

## Instalacja lokalna

Aby uruchomić aplikację lokalnie, wykonaj następujące kroki:

Pierwszym krokiem jest sklonowanie repozytorium z GitHub:

```bash
git clone https://github.com/TwojeKonto/MovieApp.git
cd MovieApp
```

Utwórz i aktywuj wirtualne środowisko:

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

```bash
Zainstaluj wymagane zależności:  
pip install -r requirements.txt
```

```bash
Zainicjalizuj bazę danych:  
python
>>> from app import db, create_app
>>> app = create_app()
>>> app.app_context().push()
>>> db.create_all()
>>> exit()
```

```bash
Uruchom aplikację:  
flask run
```

Aplikacja będzie dostępna pod adresem http://127.0.0.1:5000.

## Uruchomienie za pomocą Dockera

Aby uruchomić aplikację za pomocą Dockera, wykonaj następujące kroki:

```bash
Sklonuj repozytorium z GitHub:  
git clone https://github.com/Speedexx/movie-app.git
cd MovieApp
```

```bash
Zbuduj obraz Dockera:  
docker build -t movieapp .
```

Uruchom kontener:

```bash
docker run -p 5000:5000 movieapp
```

Aplikacja będzie dostępna pod adresem http://127.0.0.1:5000.
