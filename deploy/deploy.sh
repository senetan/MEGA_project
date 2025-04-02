#!/bin/bash

set -e  # Stoppe le script en cas d'erreur

echo "🚀 Lancement de l'API MEGA..."

# Vérification du fichier .env
if [ ! -f .env ]; then
  echo "❌ Fichier .env manquant !"
  exit 1
fi

# Démarrage du service API
APP_MODE=api docker-compose up --build -d api

echo "✅ API MEGA disponible sur http://localhost:8000"
