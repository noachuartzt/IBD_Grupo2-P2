from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql.functions import col, isnull
import json_rdd

spark = SparkSession.builder.appName("keywordCount").getOrCreate()

# Leer el archivo JSON a un DataFrame
json_files = ["2ca14fe14f0bd2f1363f3b735e788d12c3f9f332.json", "7dee9f8f534df0cbb38b12d3bb7c84f86c704fd0.json"]
json_df = spark.read.json(f"datain/{json_files[0]}")

# JUNTAR LOS JSON_DF EN UN SOLO ?

# Analizar cada registro JSON
records_rdd = json_rdd.map(json.loads)

# Seleccionar el campo text y convertirlo en un RDD
words_rdd = json_df.select("abstract").rdd.flatMap(lambda x: x[0].split())

# Longitud de las palabras a contar
n = 5

# Filtrar palabras con longitud n y contar su frecuencia
counts_rdd = words_rdd.filter(lambda word: len(word) == n).map(lambda word: (word, 1)).reduceByKey(lambda a, b: a + b)

# Mostrar resultados
print(counts_rdd.collect())

# Detener SparkContext
spark.stop()

