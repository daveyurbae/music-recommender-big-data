from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from pyspark.sql.types import StructType, StringType
from pyspark.sql.streaming import DataStreamWriter

# 1. Inisialisasi SparkSession
spark = SparkSession.builder \
    .appName("SongRecommender") \
    .config("spark.sql.shuffle.partitions", "2") \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")

# 2. Load Data Lagu dari MinIO (CSV)
song_df = spark.read.csv(
    "s3a://music-data/Music Info.csv",  # nama bucket & file di MinIO
    header=True,
    inferSchema=True
).select("track_id", "track_name", "artist_name", "genre", "language")

# 3. Konfigurasi koneksi ke MinIO
hadoop_conf = spark._jsc.hadoopConfiguration()
hadoop_conf.set("fs.s3a.access.key", "minioadmin")
hadoop_conf.set("fs.s3a.secret.key", "minioadmin")
hadoop_conf.set("fs.s3a.endpoint", "http://minio:9000")
hadoop_conf.set("fs.s3a.path.style.access", "true")
hadoop_conf.set("fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")

# 4. Baca data preferensi user dari Kafka
kafka_df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:9092") \
    .option("subscribe", "user-preference") \
    .load()

# 5. Parse nilai JSON dari Kafka
json_schema = StructType() \
    .add("user_id", StringType()) \
    .add("genre", StringType()) \
    .add("artist", StringType()) \
    .add("language", StringType()) \
    .add("timestamp", StringType())

from pyspark.sql.functions import from_json

user_pref_df = kafka_df.selectExpr("CAST(value AS STRING)") \
    .select(from_json(col("value"), json_schema).alias("data")) \
    .select("data.*")

# 6. Join preferensi user dengan data lagu
def generate_recommendation(batch_df, batch_id):
    print(f"Processing batch {batch_id}...")
    batch_df.createOrReplaceTempView("user_pref")

    for row in batch_df.collect():
        genre = row['genre']
        artist = row['artist']
        language = row['language']
        user_id = row['user_id']

        # Filter lagu berdasarkan preferensi
        filtered = song_df.filter(
            (col("genre") == genre) &
            (col("artist_name") == artist) &
            (col("language") == language)
        )

        print(f"User {user_id} Preference: {genre}, {artist}, {language}")
        filtered.show(5, truncate=False)

# 7. Jalankan streaming
query = user_pref_df.writeStream \
    .foreachBatch(generate_recommendation) \
    .outputMode("append") \
    .start()

query.awaitTermination()
