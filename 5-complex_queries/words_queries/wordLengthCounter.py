from pyspark import SparkConf, SparkContext
import json

spark = SparkSession.builder.appName("keywordCount").getOrCreate()

# Leer el archivo JSON a un DataFrame
json_df = spark.read.json("path/to/json/file.json")

# Analizar cada registro JSON
records_rdd = json_rdd.map(json.loads)

# Seleccionar el campo text y convertirlo en un RDD
words_rdd = json_df.select("text").rdd.flatMap(lambda x: x[0].split())

# Longitud de las palabras a contar
n = 5

# Filtrar palabras con longitud n y contar su frecuencia
counts_rdd = words_rdd.filter(lambda word: len(word) == n).map(lambda word: (word, 1)).reduceByKey(lambda a, b: a + b)

# Mostrar resultados
print(counts_rdd.collect())

# Detener SparkContext
spark.stop()

