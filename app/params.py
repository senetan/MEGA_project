# === Colonnes numériques utilisées dans le modèle ===
NUMERICAL_FEATURES = [
    "feature_1",
    "feature_2",
    # Ajoute ici toutes les colonnes numériques pertinentes
]

# === Colonnes catégorielles ===
CATEGORICAL_FEATURES = [
    "feature_3",
    # Ajoute ici toutes les colonnes catégorielles pertinentes
]

# === Variables inutiles ou à supprimer ===
DROP_COLUMNS = [
    "id", "timestamp",
    # Ajoute ici les colonnes à ignorer
]

# === Nom de la variable cible ===
TARGET_COLUMN = "target"

# === Option : seuils, hyperparamètres simples, etc. ===
THRESHOLD = 0.5  # Exemple pour une classification binaire
