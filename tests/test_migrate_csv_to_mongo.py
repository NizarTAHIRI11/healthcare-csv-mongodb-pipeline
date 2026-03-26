import pandas as pd
from migrate_csv_to_mongo import *
from unittest.mock import MagicMock


# 1ère vérification que la fonction n'importe pas des données vides
def test_load_csv(tmp_path):
    chemin = tmp_path / "test.csv"
    chemin.write_text("col1,col2\n1,2\n3,4")
    df = load_csv(chemin)
    assert not df.empty

# 2ème : Test de la fonction check_data
# Cette fonction est censée :
# - nettoyer les données
# - supprimer les valeurs manquantes 
# - supprimer les doublons
# Ici, on vérifie spécifiquement que les doublons sont bien supprimés
def test_check_data():
    df = pd.DataFrame({
        "name": ["TAHIRI", "TAHIRI"],
        "age": [29, 29]
    })
    net = check_data(df)
    # doit supprimer doublons
    assert len(net) == 1

# Test de la fonction connect_mongo
# Objectif :
#    - Vérifier que la connexion à MongoDB fonctionne
#    - S'assurer qu'un client MongoDB est bien retourné 
def test_connect_mongo():
    client = connect_mongo("mongodb://localhost:27017")
    # Vérifie que le client a bien été créé
    assert client is not None

#test de la fonction get_collection
def test_get_collection():
    mock_client = MagicMock()
    collection = get_collection(mock_client, "TestDB", "TestCollection")
    assert collection is not None

#  transform_data
def test_transform_data():
    df = pd.DataFrame({"name": ["TAHIRI"], "age": [29]})
    result = transform_data(df)
    assert isinstance(result, list)
    assert isinstance(result[0], dict)
    # Vérifie le contenu
    assert result[0]["name"] == "TAHIRI"
    assert result[0]["age"] == 29

# fonction migrate_data
def test_migrate_data():
    mock_collection = MagicMock()
    data = [{"name": "TAHIRI"}]
    migrate_data(mock_collection, data)
    mock_collection.delete_many.assert_called_once_with({})
    mock_collection.insert_many.assert_called_once_with(data)

#  create_index
def test_create_index():
    mock_collection = MagicMock()
    create_index(mock_collection, "Name")
    mock_collection.create_index.assert_called_once_with("Name")

# crud_operations
def test_crud_operations():
    mock_collection = MagicMock()
    crud_operations(mock_collection)
    assert mock_collection.insert_one.called
    assert mock_collection.find_one.called
    assert mock_collection.update_one.called
    assert mock_collection.delete_one.called