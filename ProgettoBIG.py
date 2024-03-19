from pyspark.sql import SparkSession
from pyspark.ml import Pipeline
from pyspark.ml.feature import VectorAssembler, StringIndexer, OneHotEncoder
from pyspark.ml.classification import RandomForestClassifier

# Creazione della sessione Spark
spark = SparkSession.builder \
    .appName("MushroomClassification") \
    .enableHiveSupport() \
    .getOrCreate()

# Caricamento del dataset da HDFS
hadoop_file_path = "hdfs://localhost:9000/user/mushrooms.csv"
df = spark.read.csv(hadoop_file_path, header=True, inferSchema=True)

# Definizione delle colonne selezionate
selected_columns = ['cap-shape', 'cap-surface', 'cap-color', 'bruises', 'odor', 'gill-attachment', 'gill-spacing', 'gill-size', 'gill-color', 'stalk-shape', 'stalk-root', 'stalk-surface-above-ring', 'stalk-surface-below-ring', 'stalk-color-above-ring', 'stalk-color-below-ring', 'veil-color', 'ring-number', 'ring-type', 'spore-print-color', 'population', 'habitat', 'class']

# Conversione delle colonne categoriche in forme numeriche
indexers = []
encoders_list = []

for col in selected_columns[:-1]:
    distinct_values = df.select(col).distinct().count()
    if distinct_values > 1:
        indexer = StringIndexer(inputCol=col, outputCol=col+"_index", handleInvalid="skip")
        encoder = OneHotEncoder(inputCol=col+"_index", outputCol=col+"_encoded")
        indexers.append(indexer)
        encoders_list.append(encoder)

# Indicizzazione della colonna 'class'
class_indexer = StringIndexer(inputCol='class', outputCol='class_index', handleInvalid="skip")
indexers.append(class_indexer)

# Assembler per creare la feature vector
assembler = VectorAssembler(inputCols=[col+"_encoded" for col in selected_columns[:-1]], outputCol="features")

# Addestramento del modello Random Forest
rf = RandomForestClassifier(labelCol="class_index", featuresCol="features", numTrees=10)

# Creazione della pipeline
pipeline = Pipeline(stages=indexers + encoders_list + [assembler, rf])

# Fit della pipeline al dataset
model = pipeline.fit(df)

# Valutazione del modello
predictions = model.transform(df)

# Salvataggio dei risultati in una tabella di Hive in un percorso HDFS specifico
hdfs_path = "hdfs://localhost:9000/user/hive/warehouse/mushroom_predictions_table"
predictions.write.mode("overwrite").saveAsTable("default.mushroom_predictions_table", path=hdfs_path)

# Mostrare i primi 20 risultati
predictions.select("prediction", "class_index").show()

# Chiusura della sessione Spark
spark.stop()
