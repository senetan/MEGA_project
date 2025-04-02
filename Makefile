# === Variables ===
PROJECT_NAME=MEGA_project
API_PORT=8000
UI_PORT=8501

# === Docker ===

build:
	docker-compose build

up-api:
	APP_MODE=api docker-compose up -d api

up-ui:
	APP_MODE=streamlit docker-compose up -d streamlit

down:
	docker-compose down

logs-api:
	docker-compose logs -f api

logs-ui:
	docker-compose logs -f streamlit

# === Test et qualité ===

lint:
	black . && isort . && pylint app/ || true

test:
	pytest

# === Utilitaires ===

clean:
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -delete

rebuild:
	docker-compose down -v
	docker-compose build --no-cache
	docker-compose up -d

# === Help ===

help:
	@echo "Commandes disponibles :"
	@echo "  build         → Build des containers"
	@echo "  up-api        → Lancer l'API"
	@echo "  up-ui         → Lancer l'interface Streamlit"
	@echo "  down          → Stopper les services"
	@echo "  test          → Lancer les tests"
	@echo "  lint          → Formatter et analyser le code"
	@echo "  clean         → Nettoyer les fichiers inutiles"
	@echo "  rebuild       → Reconstruire l'environnement complet"
	@echo "  logs-api      → Logs de l'API"
	@echo "  logs-ui       → Logs de l'interface Streamlit"
