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
    
    # Ruta al directorio que contiene los documentos JSON
    # Para el test
    json_dir = './json/'
    
    # Para la presentación
    #json_dir = './documents/demo/' 
    filepath = os.path.join(json_dir, filename + '.json')

    # Encabezados de las columnas del archivo CSV
    headers = ['paperId', 'title', 'abstract', 'year', 'publicationDate', 'authors']

    # Si carpeta /csv no existe, la crea
    if not os.path.exists('./csv'):
        os.makedirs('./csv')

    csv_file = './csv/'+ str(filename) + '.csv'

    # Abrir el archivo CSV en modo de escritura y crear un objeto writer para escribir en el archivo
    with open(csv_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
     
        # Abrir el archivo JSON
        with open(filepath, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)
            
            # Obtener los valores de las claves del JSON
            paperId = data['paperId']
            title = data['title']
            abstract = data['abstract']
            year = data['year']
            publicationDate = data['publicationDate']
            authors = data['authors']
            
            # Escribir la información en el archivo CSV
            writer.writerow([paperId, title, abstract, year, publicationDate, authors])