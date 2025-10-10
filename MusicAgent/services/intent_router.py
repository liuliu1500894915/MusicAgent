# services/intent_router.py
from models.schema import MusicActionResponse, ChatResponse

# 临时实现：基于关键词判断是否为音乐控制类意图
def route_user_intent(user_input: str):
    lowered = user_input.lower()

    # 简单关键词匹配，判断是否是音乐指令（可替换为大模型结构化输出）
    music_keywords = ["播放", "暂停", "继续", "上一首", "下一首", "音量", "动感", "安静", "来一首"]
    if any(kw in lowered for kw in music_keywords):
        # 模拟进一步解析播放行为（这里统一为播放某首歌）
        return MusicActionResponse(
            type="music",
            action="play_song",
            song="稻香"
        )

    # 默认走聊天流程
    return ChatResponse(
        type="chat",
        reply="你好，请问有什么我可以帮助你的？"
    )
