
# Migration CSV vers MongoDB (Étape 1)
## Contexte
Ce projet consiste à migrer un dataset de données médicales depuis un fichier CSV vers une base de données MongoDB locale, afin de faciliter la gestion et l’analyse des données.

## Démarche technique

Le script src/migrate_csv_to_mongo.py suit les étapes suivantes :

Lecture du CSV : utilisation de pandas pour charger le fichier healthcare_dataset.csv.
Vérification et nettoyage des données : suppression des doublons, détection des valeurs manquantes, vérification des types et dimensions des colonnes.
Transformation : conversion du DataFrame en liste de dictionnaires JSON pour l’insertion dans MongoDB.
Connexion à MongoDB : via pymongo sur une instance locale.
Insertion et migration : suppression des documents existants et insertion des nouveaux.
Création d’un index : pour accélérer les recherches sur la colonne Name.
CRUD de test : insertion, lecture, mise à jour et suppression d’un document pour vérifier le fonctionnement.

## Structure MongoDB
Base de données : Health
Collection : Healthcare
Document type : un patient (exemple réel extrait du dataset)
{
  "Name": "Bobby JacksOn",
  "Age": 30,
  "Gender": "Male",
  "Blood Type": "B-",
  "Medical Condition": "Cancer",
  "Date of Admission": "2024-01-31",
  "Doctor": "Matthew Smith",
  "Hospital": "Sons and Miller",
  "Insurance Provider": "Blue Cross",
  "Billing Amount": 18856.28,
  "Room Number": 328,
  "Admission Type": "Urgent",
  "Discharge Date": "2024-02-02",
  "Medication": "Paracetamol",
  "Test Results": "Normal"
}
## Tests
Les tests unitaires sont dans tests/test_migrate_csv_to_mongo.py et vérifient :

La lecture CSV et que les données ne sont pas vides.
Le nettoyage et suppression des doublons.
La connexion MongoDB et l’accès aux collections.
La transformation en JSON et la migration vers MongoDB.
La création d’index.
Les opérations CRUD (Create, Read, Update, Delete).

## Installation et exécution
### Installer les dépendances :
pip install -r requirements.txt
### Lancer le script :
python src/migrate_csv_to_mongo.py
### Lancer les tests :
pytest tests/


# Conteneurisation avec Docker (Étape 2)
## Schéma visuel
Health (DB)
 └─ Healthcare (Collection)
     ├─ Name : String
     ├─ Age : Integer
     ├─ Gender : String
     ├─ Blood Type : String
     ├─ Medical Condition : String
     ├─ Date of Admission : Date
     ├─ Doctor : String
     ├─ Hospital : String
     ├─ Insurance Provider : String
     ├─ Billing Amount : Float
     ├─ Room Number : Integer
     ├─ Admission Type : String
     ├─ Discharge Date : Date
     ├─ Medication : String
     └─ Test Results : String

## Authentification et rôles utilisateurs

Dans un contexte réel de production, il est recommandé de sécuriser l’accès à la base de données. MongoDB permet de définir :
## Authentification et rôles utilisateurs

Dans un contexte réel de production, il est recommandé de sécuriser l’accès à la base de données. MongoDB permet de définir :

- **Utilisateurs** : chaque personne ou service qui accède à la base a un nom d’utilisateur et un mot de passe.
- **Rôles** : déterminent les permissions d’accès. Exemples :
  - `read` : lecture seule
  - `readWrite` : lecture et écriture
  - `dbAdmin` : gestion complète de la base
  - `root` : super-admin

Exemple d’usage :

- Un utilisateur `analyste` avec rôle `read` peut uniquement lire les documents de la collection Healthcare.  
- Un utilisateur `gestionnaire` avec rôle `readWrite` peut ajouter ou modifier des documents.  
- Un utilisateur `admin` avec rôle `dbAdmin` peut gérer les index, supprimer ou créer des collections, et gérer les utilisateurs.

Comment cela se configure :

```javascript
use admin
db.createUser({
  user: "analyste",
  pwd: "MotDePasseSecurise",
  roles: [{ role: "read", db: "Health" }]
})

db.createUser({
  user: "gestionnaire",
  pwd: "MotDePasseSecurise",
  roles: [{ role: "readWrite", db: "Health" }]
})
```
Pour cette mission, la migration utilise une connexion locale non authentifiée pour simplifier le déploiement. L’authentification pourra être intégrée ultérieurement si nécessaire.