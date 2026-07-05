# Healthcare CSV → MongoDB Pipeline

> Migration d'un dataset médical (CSV) vers MongoDB, avec nettoyage des données, indexation, tests CRUD et déploiement conteneurisé via Docker Compose.
> *A pipeline that migrates a healthcare CSV dataset into MongoDB, with data cleaning, indexing, CRUD tests, and Docker Compose deployment.*

![Python](https://img.shields.io/badge/Python-3.x-blue)
![MongoDB](https://img.shields.io/badge/MongoDB-latest-green)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED)
![Tests](https://img.shields.io/badge/tests-pytest-yellow)

## Sommaire
- [Contexte](#contexte)
- [Architecture](#architecture)
- [Démarche technique](#démarche-technique)
- [Structure MongoDB](#structure-mongodb)
- [Structure du projet](#structure-du-projet)
- [Installation et exécution](#installation-et-exécution)
- [Tests](#tests)
- [Sécurité / rôles utilisateurs](#authentification-et-rôles-utilisateurs)

## Contexte
Ce projet migre un dataset de données médicales depuis un fichier CSV vers une base de données MongoDB, afin de faciliter la gestion et l'analyse des données. Le pipeline est entièrement conteneurisé : une instance MongoDB et un script Python de migration tournent chacun dans leur propre conteneur, reliés par un réseau Docker dédié.

## Architecture

```
┌─────────────────┐        mongo_net (bridge)        ┌──────────────────┐
│   py_mig_csv     │ ───────────────────────────────► │    mongo_csv     │
│  (Python script) │                                   │  (MongoDB image) │
└─────────────────┘                                   └──────────────────┘
                                                              │
                                                              ▼
                                                     volume: mongo_data
                                                     (persistance des données)
```

- **`py_mig_csv`** : construit depuis le `Dockerfile`, exécute `src/migrate_csv_to_mongo.py`.
- **`mongo_csv`** : image officielle `mongo:latest`, données persistées via un volume nommé `mongo_data`.
- Les deux services communiquent via le réseau interne `mongo_net`.

## Démarche technique
Le script `src/migrate_csv_to_mongo.py` :
1. **Lecture du CSV** — chargement de `data/healthcare_dataset.csv` via pandas.
2. **Vérification et nettoyage** — dimensions, valeurs manquantes, suppression des doublons, contrôle des types.
3. **Transformation** — conversion du DataFrame en liste de dictionnaires JSON.
4. **Connexion MongoDB** — via `pymongo`, en ciblant le service `mongo_csv` sur le réseau Docker.
5. **Migration** — vidage de la collection puis insertion des nouveaux documents.
6. **Indexation** — création d'un index sur la colonne `Name` pour accélérer les recherches.
7. **CRUD de test** — insertion, lecture, mise à jour, suppression pour valider le pipeline de bout en bout.

## Structure MongoDB

**Base** : `Health` — **Collection** : `Healthcare`

```
Health (DB)
└─ Healthcare (Collection)
   ├─ Name              : String
   ├─ Age               : Integer
   ├─ Gender            : String
   ├─ Blood Type        : String
   ├─ Medical Condition : String
   ├─ Date of Admission : Date
   ├─ Doctor            : String
   ├─ Hospital          : String
   ├─ Insurance Provider: String
   ├─ Billing Amount    : Float
   ├─ Room Number       : Integer
   ├─ Admission Type    : String
   ├─ Discharge Date    : Date
   ├─ Medication        : String
   └─ Test Results      : String
```

Exemple de document :
```json
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
```

## Structure du projet

```
healthcare-csv-mongodb-pipeline/
│   docker-compose.yml
│   Dockerfile
│   README.md
│   requirements.txt
│
├───data
│       healthcare_dataset.csv
│
├───src
│       migrate_csv_to_mongo.py
│
└───tests
        test_migrate_csv_to_mongo.py
```

## Installation et exécution

### Option 1 — Avec Docker (recommandé)
```bash
docker compose up --build
```
Cela lance MongoDB (`mongo_csv`) et exécute automatiquement le script de migration (`py_mig_csv`).

### Option 2 — En local
```bash
pip install -r requirements.txt
python src/migrate_csv_to_mongo.py
```
> Nécessite une instance MongoDB locale accessible (adapter l'URL de connexion dans le script si besoin — `mongodb://mongo_csv:27017` cible le nom du service Docker, pas `localhost`).

## Tests
`tests/test_migrate_csv_to_mongo.py` couvre :
- Lecture du CSV et non-vacuité des données
- Nettoyage et suppression des doublons
- Connexion MongoDB et accès aux collections
- Transformation en JSON
- Migration (delete + insert), avec mocks
- Création d'index
- Opérations CRUD complètes

```bash
pytest tests/
```

## Authentification et rôles utilisateurs
En production, l'accès à MongoDB doit être sécurisé via des utilisateurs et des rôles :

| Rôle | Permissions |
|---|---|
| `read` | lecture seule |
| `readWrite` | lecture et écriture |
| `dbAdmin` | gestion complète de la base |
| `root` | super-admin |

Exemple de configuration :
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

> Pour cette mission, la migration utilise une connexion locale non authentifiée afin de simplifier le déploiement. L'authentification pourra être intégrée ultérieurement.

## Stack
`Python` · `pandas` · `pymongo` · `MongoDB` · `pytest` · `Docker` · `Docker Compose`
