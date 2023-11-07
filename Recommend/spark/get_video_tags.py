from pyspark.sql import SparkSession
from pyspark.sql.functions import when

# 创建SparkSession
spark = SparkSession.builder.appName("LevelUpTags").getOrCreate()

# 读取Parquet
df = spark.read.parquet("hdfs://172.22.0.2/level-up-logs.parquet")
# df = spark.read.parquet("./level-up-logs.parquet")

# 获取视频比例
df = df.withColumn("video", when(df.click <= 10, "0").when(df.ratio <= 0.5, "1").otherwise("2"))

# 排序
df = df.groupBy("date", "id", "ratio").count()
df = df.drop("count").sort("date")
df.show(1000)

# 写入EachDayTags文件夹中
df.write.csv("../EachDayTags")