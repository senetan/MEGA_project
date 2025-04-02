# Utilise une image légère compatible ARM64
FROM python:3.10-slim

# Empêche Python de bufferiser stdout/stderr
ENV PYTHONUNBUFFERED=1

# Définir le répertoire de travail
WORKDIR /app

# Installer les dépendances système nécessaires
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copier et installer les dépendances Python
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir --default-timeout=300 -r requirements.txt

# Copier l’ensemble de l’app dans l’image
COPY . .

# Commande par défaut — sera écrasée par docker-compose
CMD ["streamlit", "run", "app/streamlit_app.py"]
