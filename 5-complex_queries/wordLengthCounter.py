from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql.functions import col, isnull
import os

# Crear la sesión Spark
spark = SparkSession.\
        builder.\
        appName("lengthwordCount").\
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

# Longitud de las palabras a contar
n = 6

# Filtrar palabras con longitud n y contar su frecuencia
counts_rdd = words_rdd.filter(lambda word: len(word) == n).map(lambda word: (n, 1)).reduceByKey(lambda a, b: a + b)
# counts_rdd = words_rdd.filter(lambda word: len(word) == n).map(lambda word: (word, 1)).reduceByKey(lambda a, b: a + b) # si se quieren saber cuales son las palabras de longitud n

# Mostrar resultados
print(counts_rdd.collect())

# Cerrar la sesión de Spark
spark.stop()