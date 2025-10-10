# rag/song_retriever.py
from typing import List

# 模拟的歌曲知识库（可替换为向量检索）
songs = [
    {"title": "稻香", "artist": "周杰伦", "lyrics": "回到最初的美好", "tags": ["温暖", "青春"]},
    {"title": "龙卷风", "artist": "周杰伦", "lyrics": "爱像龙卷风离不开暴风圈", "tags": ["情感"]},
    {"title": "夜曲", "artist": "周杰伦", "lyrics": "黑色的毛衣遮住你坏掉的表情", "tags": ["暗黑"]},
    {"title": "晴天", "artist": "周杰伦", "lyrics": "故事的小黄花", "tags": ["校园"]},
    {"title": "青春修炼手册", "artist": "TFBOYS", "lyrics": "这是我们的青春修炼手册", "tags": ["青春", "动感"]}
]

# 模拟检索函数：关键词匹配标题、歌词、标签
def retrieve_song(query: str, top_k: int = 1) -> str:
    query_lower = query.lower()
    matched = []
    for song in songs:
        text = song["title"] + song["artist"] + song["lyrics"] + "".join(song["tags"])
        if any(q in text.lower() for q in query_lower.split()):
            matched.append(song)

    return matched[0]["title"] if matched else "稻香"  # 默认返回稻香
