from pyspark.sql import SparkSession
from pyspark.sql.functions import explode, split

# Crear la sesión de Spark
spark = SparkSession.builder.appName("keywordCount").getOrCreate()

# Leer el archivo JSON a un DataFrame
json_df = spark.read.json("path/to/json/file.json")

# Seleccionar el campo text y convertirlo en un RDD
words_rdd = json_df.select("text").rdd.flatMap(lambda x: x[0].split())

# Lista de palabras
words_to_count = ["a", "b", "c", "d", "e]

# Contar las palabras
counts_rdd = words_rdd.filter(lambda word: word in words_to_count).map(lambda word: (word, 1)).reduceByKey(lambda a, b: a + b)

# Mostrar los resultados
print(counts_rdd.collect())

# Cerrar la sesión de Spark
spark.stop()
