# 1️ Choisir l'image Python officielle
FROM python:latest

# 2️ Définir le dossier de travail dans le conteneur
WORKDIR /app

#3 Copier uniquement les fichiers nécessaires
COPY requirements.txt .
COPY src/ ./src
COPY data/ ./data

# 4️ Installer les dépendances Python nécessaires
RUN pip install --no-cache-dir -r requirements.txt


# 5️ Définir la commande à exécuter quand le conteneur démarre
CMD ["python", "src/migrate_csv_to_mongo.py"]
