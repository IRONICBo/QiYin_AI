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

### 运行（大模型 & AI）

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