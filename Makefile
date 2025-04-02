# === MEGA_project Makefile ===

# Build les images Docker
build:
	@echo "🔧 Build des images Docker..."
	docker-compose build

# Lancer les services (API + Streamlit)
up:
	@echo "🚀 Lancement de l'API et de Streamlit..."
	docker-compose up

# Lancer en arrière-plan
up-detached:
	@echo "🚀 Lancement en arrière-plan..."
	docker-compose up -d

# Arrêter les services
down:
	@echo "🛑 Arrêt des services..."
	docker-compose down

# Rebuild + restart complet
rebuild:
	@echo "🔁 Rebuild complet..."
	docker-compose down
	docker-compose up --build

# Logs
logs:
	docker-compose logs -f

# Shell dans le conteneur API
shell-api:
	docker exec -it mega_api /bin/bash

# Shell dans le conteneur Streamlit
shell-streamlit:
	docker exec -it mega_streamlit /bin/bash

# Nettoyage complet (dangling images, containers, etc.)
clean:
	@echo "🧹 Nettoyage Docker..."
	docker system prune -af --volumes
