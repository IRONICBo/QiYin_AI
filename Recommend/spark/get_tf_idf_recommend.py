from pyspark.ml.feature import HashingTF, IDF, Tokenizer
from pyspark.sql import SparkSession

# 创建 SparkSession
spark = SparkSession.builder.getOrCreate()

df = spark.read.parquet("hdfs://172.22.0.2/video-recommend.parquet")

tokenizer = Tokenizer(inputCol="video", outputCol="list")
wordsData = tokenizer.transform(df)
hashingTF = HashingTF(inputCol="list", outputCol="rawFeatures", numFeatures=20)
featurizedData = hashingTF.transform(wordsData)

# 计算点击频率
idf = IDF(inputCol="rawFeatures", outputCol="features")
idfModel = idf.fit(featurizedData)
rescaledData = idfModel.transform(featurizedData)

# 显示结果
rescaledData.select("id", "video").show(truncate=False)

# TODO: 写入redis队列中