#!/bin/bash

set -e  # Arrêter si une commande échoue

echo "🚀 Lancement de l'interface Streamlit..."

# Vérification du fichier .env
if [ ! -f .env ]; then
  echo "❌ Fichier .env introuvable !"
  exit 1
fi

# Démarrage du service Streamlit
APP_MODE=streamlit docker-compose up --build -d streamlit

echo "✅ Interface MEGA disponible sur http://localhost:8501"
