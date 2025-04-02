#!/bin/bash

# =============================
# 🚀 MEGA_project Deploy Script
# =============================

# Paramètres
PROJECT_ID=your-gcp-project-id
REGION=europe-west9
SERVICE_NAME=mega-api
IMAGE_NAME=gcr.io/$PROJECT_ID/$SERVICE_NAME
ENV_FILE=.env

# Authentification (si besoin)
#gcloud auth login
#gcloud config set project $PROJECT_ID

echo "🔧 Construction de l'image Docker..."
docker build -t $IMAGE_NAME .

echo "📤 Push de l'image vers Google Container Registry..."
docker push $IMAGE_NAME

echo "🚀 Déploiement sur Cloud Run..."
gcloud run deploy $SERVICE_NAME \
  --image $IMAGE_NAME \
  --platform managed \
  --region $REGION \
  --allow-unauthenticated \
  --port=8000 \
  --set-env-vars="$(cat $ENV_FILE | xargs)"

echo "✅ Déploiement terminé !"
