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

# Run the main script
run:
	@echo "Running the main script..."
	pyenv activate MEGA_project
	python MEGA_project/MEGA_project_folder/api_file.py
