# build_vector_db.py
from pymilvus import connections, CollectionSchema, FieldSchema, DataType, Collection
from sentence_transformers import SentenceTransformer
import pandas as pd
import numpy as np
import random

# 连接 Milvus
connections.connect("default", host="192.168.1.112", port="19530")

# 创建 Collection Schema
song_id = FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=False)
song_name = FieldSchema(name="title", dtype=DataType.VARCHAR, max_length=100)
embedding = FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=768)
schema = CollectionSchema(fields=[song_id, song_name, embedding], description="歌曲搜索")

# 创建集合（如果不存在）
collection_name = "songs"
if collection_name in Collection.list():
    collection = Collection(collection_name)
    collection.drop()
collection = Collection(name=collection_name, schema=schema)

# 初始化 embedding 模型（bge-base-zh）
model = SentenceTransformer("moka-ai/bge-base-zh-v1.5")

# 构建假数据（你也可替换为真实 CSV 加载）
sample_songs = [
    {"id": i, "title": title, "text": f"{title} 是一首{random.choice(['动感', '青春', '舒缓', '经典'])}的歌曲，{random.choice(['歌词深情', '旋律悠扬', '节奏强烈'])}。"}
    for i, title in enumerate([
        "稻香", "夜曲", "龙卷风", "青花瓷", "听妈妈的话", "双截棍", "晴天", "以父之名", "安静", "爱在西元前",
        "说好的幸福呢", "蒲公英的约定", "千里之外", "发如雪", "简单爱", "黑色毛衣", "东风破", "彩虹",
        "给我一首歌的时间", "止战之殇", "迷迭香", "珊瑚海", "一路向北", "搁浅", "她的睫毛",
        "七里香", "借口", "开不了口", "回到过去", "爷爷泡的茶", "威廉古堡", "轨迹", "霍元甲", "园游会",
        "兰亭序", "牛仔很忙", "菊花台", "阳光宅男", "烟花易冷", "跨时代", "大笨钟", "红尘客栈", "手写的从前",
        "明明就", "听见下雨的声音", "告白气球", "说好不哭", "我是如此相信", "不爱我就拉倒"
    ])
]

# 生成向量并准备插入
texts = [s["text"] for s in sample_songs]
titles = [s["title"] for s in sample_songs]
ids = [s["id"] for s in sample_songs]
embeds = model.encode(texts, show_progress_bar=True)

collection.insert([ids, titles, embeds])
collection.flush()
print(f"✅ 已成功写入 {len(titles)} 首歌曲到 Milvus！")
