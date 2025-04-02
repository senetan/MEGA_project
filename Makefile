# === Variables ===
PROJECT_NAME=MEGA_project
API_PORT=8000
UI_PORT=8501
ENV_FILE=.env

# === Docker ===

build:
	docker compose build

up-api:
	docker compose --env-file $(ENV_FILE) up -d api

up-ui:
	docker compose --env-file $(ENV_FILE) up -d streamlit

down:
	docker compose down

logs-api:
	docker compose logs -f api

logs-ui:
	docker compose logs -f streamlit

# === Tests et Qualité ===

lint:
	black . && isort . && pylint app/ || true

test:
	pytest

# === Utilitaires ===

clean:
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -delete

rebuild:
	docker compose down -v
	docker compose build --no-cache
	docker compose --env-file $(ENV_FILE) up -d

# === Déploiement GCP ===

gcp-login:
	gcloud auth login

gcp-set-project:
	gcloud config set project $(shell grep GCP_PROJECT $(ENV_FILE) | cut -d '=' -f2)

gcp-build-api:
	gcloud builds submit --tag europe-west9-docker.pkg.dev/$(shell grep GCP_PROJECT $(ENV_FILE) | cut -d '=' -f2)/$(shell grep GAR_IMAGE $(ENV_FILE) | cut -d '=' -f2)

gcp-deploy-api:
	gcloud run deploy $(shell grep GAR_IMAGE $(ENV_FILE) | cut -d '=' -f2) \
		--image=europe-west9-docker.pkg.dev/$(shell grep GCP_PROJECT $(ENV_FILE) | cut -d '=' -f2)/$(shell grep GAR_IMAGE $(ENV_FILE) | cut -d '=' -f2) \
		--platform=managed \
		--region=$(shell grep GCP_REGION $(ENV_FILE) | cut -d '=' -f2) \
		--allow-unauthenticated

# === Aide ===

help:
	@echo "Commandes disponibles :"
	@echo "  build             → Build des containers"
	@echo "  up-api            → Lancer l'API localement"
	@echo "  up-ui             → Lancer Streamlit localement"
	@echo "  down              → Stopper les services"
	@echo "  test              → Lancer les tests"
	@echo "  lint              → Formatter et analyser le code"
	@echo "  clean             → Nettoyer les fichiers inutiles"
	@echo "  rebuild           → Rebuild complet"
	@echo "  logs-api          → Logs API"
	@echo "  logs-ui           → Logs UI"
	@echo "  gcp-login         → Connexion à GCP"
	@echo "  gcp-set-project   → Définir le projet GCP"
	@echo "  gcp-build-api     → Build et push vers Google Artifact Registry"
	@echo "  gcp-deploy-api    → Déploiement sur Cloud Run"
