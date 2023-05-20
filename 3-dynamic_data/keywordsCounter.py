from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql.functions import col, isnull
import shutil
import glob
import csv

# Crear la sesión Spark
spark = SparkSession.\
        builder.\
        appName("keywordCount").\
        master("spark://spark-master:7077").\
        config("spark.executor.memory", "5g").\
        config("spark.eventLog.enabled", "true").\
        config("spark.eventLog.dir", "file:///opt/workspace/events").\
        getOrCreate()

# Preprocesado
# =====================================================================
# Leer todos los archivos JSON del corpus (uniéndolos en un mismo DataFrame)
directory = './datain'

# Lista de archivos en el directorio
corpus = os.listdir(directory)

json_df = spark.read.json(["datain/" + file for file in corpus])

# Eliminar registros con abstract nulo
json_df_filtered = json_df.filter(col('abstract').isNotNull())

# MAP-REDUCE
# =====================================================================
# Seleccionar el campo abstract y convertirlo en un RDD
words_rdd = json_df_filtered.select("abstract").rdd.flatMap(lambda x: x[0].split())

# Lista de palabras
words_to_count = ["Science", "artificial", "intelligence", "The"]
words_to_count = [word.lower() for word in words_to_count]

# Contar las palabras
counts_rdd = words_rdd.filter(lambda word: word.lower() in words_to_count).map(lambda word: (word.lower(), 1)).reduceByKey(lambda a, b: a + b)

# Mostrar los resultados
print(counts_rdd.collect())

# Keywords.csv
# =====================================================================
# Guardar en CSV
counts_df = counts_rdd.toDF() # convertir a DataFrame la lista resultado
counts_df.write.csv("dataout/temp", mode="overwrite") # guardamos los resultados de cada worker

# Obtener todos los archivos CSV generados en el directorio temporal
csv_files = glob.glob("dataout/temp/*.csv")

# Fusionar los archivos CSV en uno solo
with open("dataout/Keywords.csv", "w", newline="") as outfile:
    writer = csv.writer(outfile)
    writer.writerow(["word", "frequency"]) # Escribir los nuevos nombres de las columnas

    # Leer cada archivo CSV y copiar sus contenidos al archivo de salida
    for csv_file in csv_files:
        with open(csv_file, "r", newline="") as infile:
            reader = csv.reader(infile)
            for row in reader:
                writer.writerow(row)
                
# Borramos el fichero temp
folder_path = "dataout/temp"
shutil.rmtree(folder_path) # borramos la carpeta y su contenido

# Cerrar la sesión de Spark
spark.stop()
