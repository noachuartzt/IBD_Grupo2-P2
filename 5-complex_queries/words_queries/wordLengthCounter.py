from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql.functions import col, isnull

# Create the Spark session
spark = SparkSession.builder.appName("lengthwordCount").getOrCreate()

# Preprocesado
# =====================================================================
# Leer todos los archivos JSON del corpus (uniéndolos en un mismo DataFrame)
corpus = ["2ca14fe14f0bd2f1363f3b735e788d12c3f9f332.json","7dee9f8f534df0cbb38b12d3bb7c84f86c704fd0.json",
          "9e2501b8e5da6e1627508c4eb321bf66eb41020e.json","80313ba1f12e4525b941ba29f8e020cf5ae8b835.json",
          "2038383fedccdf0b8c1efcb0832ecd18b481b3c1.json","f8d9409606abc438537d3a249b56ec0ac8e62e91.json"]
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
