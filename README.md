# QiYin AI Project

柒音AI服务仓库（推荐 & 离线识别 & 大模型服务）

### 设计文档和DEMO

文档地址和演示地址：https://eq2pyit41ih.feishu.cn/docx/M6L8dYYg6oq3cvxsBSpcoteLnuc

### 主要组件

##### Local Classification On Web

- onnxruntime web
- SqueezeNet
- Resnet18

##### LLM intergration with LangChain

- fastchat
- vicuna 7B
- milvus

##### Support Recommendation System

- TF-IDF(Basic Model)

### 运行（大模型 & 推荐）

##### Langchain & Milvus

1. 启动Milvus集群
```bash
cd deploy
docker-compose -f docker-compose.yml up -d
```

2. 更新配置文件
```bash
vi config.yaml
```

3. 安装依赖
```bash
pip install -r requirements.txt
```

5. 启动大模型服务Vicuna 7B
```bash
cd llm
python main.py
```

6. 启动API服务
```bash
# 根目录下面
python main.py 
```

##### 推荐

运行环境：Spark 2.x 

1. 启动Spark集群

2. 启动kafka集群，将数据导入kafka等待消费
```bash
cd kafka
docker-compose -f docker-compose.yml up -d
```
从Kafka消费写入HDFS。使用Kafka的消费者API从Kafka中读取消息。需要指定 Kafka服务器的地址、主题名称以及要消费的消息数量。读取到的消息可以写入HDFS 中。在消费过程中解析日志，并且写入parquet文件，保存到HDFS中。

> 使用python API完成生产者的命令，代码在`kafka/consumer.py`中

```bash
# config.ini是kafka的配置文件
python consumer.py config.ini
```

4. Spark处理HDFS数据并完成标记

通过Spark处理计算HDFS中数据，完成视频用户的标记。使用Spark的API读取HDFS中parquet文件，然后对每一天的数据进行计算，输出玩家等级标签。最后将结果写入csv文件中。

> 使用python API完成生产者的命令，代码在`spark/get_video_tags.py`中

```bash
python get_video_tags.py # 获取标签
python get_tf_idf_recommend.py # 通过TF-IDF推荐
```

5. 启动Hadoop，将数据推送HDFS中

6. 提交Spark实时计算任务(Python)
```bash
spark-submit --master spark://localhost:7077 --class com.qiyin.recommendation.Recommendation --executor-memory 4G --total-executor-cores 4 --executor-cores 2 --driver-memory 4G --jars /home/qiyin/llm/recommendation/target/scala-2.11/recommendation_2.11-0.1.jar /home/qiyin/llm/recommendation/target/scala-2.11/recommendation_2.11-0.1.jar
```

7. TODO:更新推荐结果，放入Redis队列中