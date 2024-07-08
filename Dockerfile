# Usa l'immagine base di Python
FROM python:3.12-slim

# Imposta la directory di lavoro
WORKDIR /app

# Copia i file requirements.txt e installa le dipendenze
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copia il resto del codice nell'immagine
COPY . .

# Esponi la porta che il servizio Flask utilizzerà
EXPOSE 5000

# Comando per eseguire l'app
CMD ["python", "app.py"]