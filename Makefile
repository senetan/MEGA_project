# Install dependencies in the pyenv-managed virtual environment
install:
	@echo "Installing dependencies..."
	pyenv activate MEGA_project
	pip install -r requirements.txt

# Clean temporary files
clean:
	@echo "Cleaning temporary files..."
	rm -rf __pycache__
	rm -rf .pytest_cache
	rm -rf *.log

# Built a container
build_container_local:
	docker build --tag=${IMAGE}:dev .

run_container_local:
	docker run -it -e PORT=8000 -p 8080:8000 ${IMAGE}:dev
