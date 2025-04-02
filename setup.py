from setuptools import setup, find_packages

setup(
    name="mega_project",
    version="0.1.0",
    author="Ton Nom",
    description="Projet MEGA : API et interface Streamlit pour prédiction ML",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "numpy",
        "pandas",
        "scikit-learn",
        "joblib",
        "tensorflow",
        "keras",
        "scikeras",
        "fastapi",
        "uvicorn",
        "streamlit",
        "matplotlib",
        "seaborn",
        "python-dotenv",
        "google-cloud-storage",
        "google-cloud-bigquery",
        "google-auth",
        "google-auth-oauthlib",
        "google-api-core"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            # Ajoute ici des commandes CLI personnalisées si besoin
            # ex : mega-run = app.cli:main
        ]
    },
)
