from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql.functions import col, isnull

# Create the Spark session
spark = SparkSession.builder.appName("keywordCount").getOrCreate()

# Preprocesado
# =====================================================================

# Leer todos los archivos JSON del corpus (uniendolos en un mismo DataFrame)
corpus = ["2ca14fe14f0bd2f1363f3b735e788d12c3f9f332.json", "7dee9f8f534df0cbb38b12d3bb7c84f86c704fd0.json", "f8d9409606abc438537d3a249b56ec0ac8e62e91.json"]
json_df = spark.read.json(["datain/" + file for file in corpus])

# Eliminar registros con abstract nulo
json_df_filtered = json_df.filter(col('abstract').isNotNull())

# MAP-REDUCE
# =====================================================================

# Seleccionar el campo abstract y convertirlo en un RDD
words_rdd = json_df_filtered.select("abstract").rdd.flatMap(lambda x: x[0].split())

# Lista de palabras
words_to_count = ["science", "artificial", "intelligence", "the", "The"]

# Contar las palabras
counts_rdd = words_rdd.filter(lambda word: word in words_to_count).map(lambda word: (word, 1)).reduceByKey(lambda a, b: a + b)

# Mostrar los resultados
print(counts_rdd.collect())

# Cerrar la sesión de Spark
spark.stop()