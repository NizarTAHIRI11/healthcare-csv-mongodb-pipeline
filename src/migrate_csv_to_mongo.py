import pandas as pd  # Pour manipuler le CSV
import pymongo as pm  # Pour interagir avec MongoDB


# ----------- FONCTIONS -----------
# création des fonctions nécessaires 

# 1ere fonction pour lire et envoyer une dataframe propre 
def load_csv(chemin):
    df = pd.read_csv(chemin)
    return df

# 2ème fonction pour vérifier l'intégrité des données, existence des doublons
# des valeurs manquantes, ainsi que les dimensions et les types de colonnes
def check_data(df):
    print("===## Vérification des données ##===")
    print("Dimensions :", df.shape)
    print("Valeurs manquantes :\n", df.isnull().sum())
    if df.isnull().sum().any():
        print("Attention : certaines colonnes contiennent des valeurs manquantes. " \
        "Veuillez corriger avant d'envoyer.")
    print("recherche des Doublons :")
    if df.duplicated().sum() > 0:
        df = df.drop_duplicates()
        print("Les doublons ont été éliminés") # Si des doublons existent, les supprimer
    else:
        print("Aucun doublon trouvé")
    print("Re-vérification des dimensions après suppression des doublons :", df.shape)
    print("Types des colonnes :\n", df.dtypes)
    print("Aperçu :\n", df.head())
    
    return df  # permet de récupérer le DataFrame nettoyage

# 3ème fonction pour assurer la connexion à MongoDB
def connect_mongo(url_mongo):
    client = pm.MongoClient(url_mongo)
    return client

# 4ème fonction pour accéder à la base de données et aux collections
def get_collection(client, db_name, collection_name):
    db = client[db_name]
    collection = db[collection_name]
    return collection 

# 5ème fonction sert à transformer un dataframe en liste de dictionnaires JSON
def transform_data(df):
    return df.to_dict(orient="records")

# 6ème fonction sert à migrer les données et les insérer dans la collection en la vidant avant
def migrate_data(collection, data):
    collection.delete_many({})  # Supprime toutes les données existantes
    if data:
        collection.insert_many(data)  # Insère les données

# 7ème fonction sert à créer un index sur une colonne afin d’optimiser et accélérer les 
# opérations de recherche et de filtrage dans MongoDB
def create_index(collection, col):
      if col:
          collection.create_index(col)

# 8ème fonction sert à utiliser les commandes de base CRUD pour MongoDB
def crud_operations(collection):
    print("===## Début des opérations CRUD ##===")
    # CREATE
    print("CREATE :: Document inséré :", collection.insert_one({"test": "valeur"}))
    # READ
    print("READ :: Document trouvé :", collection.find_one({"test": "valeur"}))
    # UPDATE
    collection.update_one({"test": "valeur"}, {"$set": {"test": "valeur_MAJ"}})
    print("UPDATE :: Document MAJ :", collection.find_one({"test": "valeur_MAJ"}))
    # DELETE
    collection.delete_one({"test": "valeur_MAJ"})
    print("DELETE :: Document supprimé :", collection.find_one({"test": "valeur_MAJ"}))
    print("===## CRUD terminé ##===")


# ----------- SCRIPT PRINCIPAL -----------

if __name__ == "__main__":
    # 1- Lecture du CSV
    data = load_csv("data/healthcare_dataset.csv")

    # 2- Vérification des données
    data=check_data(data)

    # 3- Connexion à MongoDB
    client = connect_mongo("mongodb://mongo_csv:27017")
    collection = get_collection(client,db_name="Health",collection_name="Healthcare")

    # 4- Transformation des données
    data_h = transform_data(data)

    # 5- Migration vers MongoDB
    migrate_data(collection, data_h)

    # 6- Création d'un index
    create_index(collection, col="Name")

    # 7- Exemple CRUD
    crud_operations(collection)

    print("Migration terminée avec succès !")