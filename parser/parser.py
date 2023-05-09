# OBTENER LOS DATOS DE MÚLTIPLES PAPERS EN UN SOLO REQUEST  

# Importa las librerías necesarias
import pandas as pd
import requests
import json
import os
import csv


def doi_to_json():

    """Convierte los DOIs de un archivo de texto a JSON y los guarda en una carpeta llamada /json"""

    # Lee el archivo corpus.txt como una serie
    df_dois = pd.read_csv("corpus.txt", header=None, names=["DOIs"])

    # Transforma la serie en una lista de DOIs
    dois = df_dois["DOIs"].tolist()
    # print(dois)

    # Si carpeta /json no existe, la crea
    if not os.path.exists('./json'):
        os.makedirs('./json')

    # Realiza una petición POST a la API de SemanticScholar
    r = requests.post(
        'https://api.semanticscholar.org/graph/v1/paper/batch',
        params={'fields': 'url,title,abstract,year,publicationDate,authors'},
        json={"ids": dois}
    )

    # Convierte la respuesta en un objeto JSON
    data = r.json()

    for i in data:

        # Comprueba si el paper existe
        if i is not None:
            output = json.dumps(i, indent=4)

            filename = i['paperId']

            # Guarda los datos en un archivo JSON
            with open(f'./json/{filename}.json', 'w') as f:
                f.write(output)


    
def json_to_csv(filename):
    """
    Convierte archivos JSON a CSV.
    
    :param filename: Nombre del archivo JSON en string sin el .json
    """
    
    # Cargar los datos JSON desde un archivo
    data = pd.read_json(f'./json/{filename}.json')

    # Conversión de sub-objectos a listas 
    author_ids = [author['authorId'] for author in data['authors']]
    author_names = [author['name'] for author in data['authors']]

    # Eliminar las filas con datos duplicados
    data = data.iloc[0]

    # Crear un DataFrame con los datos seleccionados
    df = pd.DataFrame({
        'paperId': data['paperId'],
        'title': data['title'],
        'abstract': data['abstract'],
        'year': data['year'],
        'publicationDate': data['publicationDate'],
        'authorId': [author_ids],
        'authorName': [author_names]
        })

    # Si carpeta /csv no existe, la crea
    if not os.path.exists('./csv'):
        os.makedirs('./csv')

    # Guardar el DataFrame en un archivo CSV
    df.to_csv(f'./csv/{filename}.csv', index=False)