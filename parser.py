import os
import json
import csv
import pandas as pd


def json_to_csv(filename):
    """
    Convierte archivos JSON a CSV.
    
    :param filename: Nombre del archivo JSON en string sin el .json
    """
    
    # Ruta al directorio que contiene los documentos JSON
    # Para el test
    json_dir = './documents/test/'
    # Para la presentación
    #json_dir = './documents/demo/' 
    filepath = os.path.join(json_dir, filename + '.json')

    # Encabezados de las columnas del archivo CSV
    headers = ['title', 'num_pages', 'creation_date', 'modification_date']

    csv_file = './documents/output/'+ str(filename) + '.csv'

    # Abrir el archivo CSV en modo de escritura y crear un objeto writer para escribir en el archivo
    with open(csv_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
     
        # Abrir el archivo JSON
        with open(filepath, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)
            # Obtener los valores de las claves del JSON
            title = data['title']
            num_pages = data['num_pages']
            creation_date = data['creation_date']
            modification_date = data['modification_date']
            
            # Escribir la información en el archivo CSV
            writer.writerow([title, num_pages, creation_date, modification_date])
