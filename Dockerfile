# Wybieramy lekką wersję Pythona
FROM python:3.11-slim

# Ustawiamy katalog roboczy w kontenerze
WORKDIR /app

# Kopiujemy plik requirements.txt do kontenera
COPY requirements.txt /app/

# Instalujemy zależności
RUN pip install --no-cache-dir -r requirements.txt

# Kopiujemy cały kod aplikacji (pozostałe pliki i foldery)
COPY . /app

# Ustawiamy zmienną środowiskową Flask
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Otwieramy port (Flask domyślnie działa na 5000)
EXPOSE 5000

# Komenda uruchamiająca aplikację
CMD ["flask", "run"]
