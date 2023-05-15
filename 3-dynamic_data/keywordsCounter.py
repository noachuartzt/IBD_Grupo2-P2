from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql.functions import col, isnull

# Create the Spark session
spark = SparkSession.builder.appName("keywordCount").getOrCreate()

# Read the JSON file into a DataFrame
json_df = spark.read.json("datain/2ca14fe14f0bd2f1363f3b735e788d12c3f9f332.json")

# Add a new column 'is_null' indicating whether 'abstract' column is null or not
json_df_with_null = json_df.withColumn('is_null', col('abstract').isNull())

# Show the 'is_null' column
if json_df_with_null.select('is_null').first()[0] == False:
    
    # Seleccionar el campo text y convertirlo en un RDD
    words_rdd = json_df.select("abstract").rdd.flatMap(lambda x: x[0].split())

    # Lista de palabras
    words_to_count = ["science", "artificial", "intelligence", "the", "The"]

    # Contar las palabras
    counts_rdd = words_rdd.filter(lambda word: word in words_to_count).map(lambda word: (word, 1)).reduceByKey(lambda a, b: a + b)

    # Mostrar los resultados
    print(counts_rdd.collect())
    
else:
    raise ValueError("The 'abstract' section of the paper contains null values. Please select another section of the paper or instead another paper.")

# Cerrar la sesión de Spark
spark.stop()
