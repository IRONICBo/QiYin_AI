from argparse import ArgumentParser, FileType
from configparser import ConfigParser
from confluent_kafka import Consumer, OFFSET_BEGINNING
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import re

# 运行脚本
# python consumer.py config.ini

# PS: HDFS 的版本对于 pyarrow 库的使用是有要求的，
# 不同版本的 HDFS 可能需要使用不同版本的 pyarrow 库才能正常工作

# 解析日志
def decode_log(log):
    print("---", log)
    res = log.strip().split(" ")
    date, data = res[0], log.split(", ", maxsplit=1)[1] # 只分割一次
    date = date[1:]

    print(date, data)

    m = re.search(r"\{\"video\":(\d+), \"ratio\": (\d+)\}", data)
    role_id = str(m.group(1))
    level = str(m.group(2))

    print("---", date, role_id, level)
    return date, role_id, level

# 将日志写入HDFS
def write_to_hdfs(messages):
    records = [message.key().decode('utf-8') for message in messages]

    print(messages)
    print(records)

    df = pd.DataFrame([decode_log(record) for record in records], columns=["date", "role_id", "level"])

    table = pa.Table.from_pandas(df)
    print(table)
    # 写入HDFS
    pq.write_table(table, "hdfs://172.22.0.2/level-up-logs.parquet")
    # pq.write_table(table, "level-up-logs.parquet")

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('config_file', type=FileType('r'))
    parser.add_argument('--reset', action='store_true')
    args = parser.parse_args()

    config_parser = ConfigParser()
    config_parser.read_file(args.config_file)
    config = dict(config_parser['default'])
    config.update(config_parser['consumer'])

    consumer = Consumer(config)

    def reset_offset(consumer, partitions):
        if args.reset:
            for p in partitions:
                p.offset = OFFSET_BEGINNING
            consumer.assign(partitions)

    # 定义Topic
    topic = "level_up_logs"
    consumer.subscribe([topic], on_assign=reset_offset)

    msgs = []
    count_wait = 0

    # 从Kafka中获取数据
    try:
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                # 等待数据获取
                print("Waiting...")
                count_wait += 1
                if count_wait >= 10:
                    print("timeout ---, save to HDFS")
                    break   
            elif msg.error():
                print("ERROR: %s".format(msg.error()))
            else:
                print("Consumed event from topic {topic}: key = {key:12} value = {value:12}".format(
                    topic=msg.topic(), key=msg.key().decode('utf-8'), value=msg.value().decode('utf-8')))
                msgs.append(msg) # 收集数据
    except KeyboardInterrupt:
        pass
    finally:
        # 收集结束后写入HDFS
        write_to_hdfs(msgs)
        consumer.close()