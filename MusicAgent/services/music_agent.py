from models.schema import AgentState
from langchain_core.messages import ToolMessage, AIMessage
from rag.song_retriever import retrieve_song
from langchain_community.chat_models import ChatZhipuAI
from langchain_core.messages import ToolMessage, HumanMessage
import json
import re
llm = ChatZhipuAI(
    zhipuai_api_key="16d7bb61e4fb438fb212266be2ba7478.7To5DD4sn6lBliwG",
    model="glm-4-plus"
)

def music_node(state: AgentState) -> dict:
    user_input = state["user_input"]
    print("🎧 music_node 收到用户输入：", user_input)

    prompt = build_intent_prompt(user_input)

    try:
        # 调用 GLM
        response = llm.invoke([HumanMessage(content=prompt)])
        print("music_node-🧠 GLM 回复：", response.content)

        # 尝试提取 JSON，去掉可能的非 JSON 内容
        content_str = response.content.strip()

        # 保险处理：用正则匹配 JSON 段
        match = re.search(r"\{.*\}", content_str, re.DOTALL)
        if not match:
            raise ValueError("未能找到 JSON 内容")

        json_str = match.group(0)
        intent_data = json.loads(json_str)
        print("intent_data：", response.content)
        action_json = {
            "type": "music",
            "intent": intent_data.get("intent"),
            "song": intent_data.get("song")
        }
        print("action_json：", response.content)

        return {
            "messages": [
                ToolMessage(content=json.dumps(action_json), tool_call_id="music_agent")
            ]
        }

    except Exception as e:
        print(f"⚠️ music_node 解析出错: {e}")
        return {
            "messages": []  # 失败时返回空消息
        }


#
# def music_node(state: AgentState) -> dict:
#     user_input = state["user_input"]
#     print("🎧 music_node 收到用户输入：", user_input)
#     print(user_input)
#
#     song = retrieve_song(user_input)
#     print("🎵 匹配到歌曲：", song)
#
#     action_json = {
#         "type": "music",
#         "action": "play_song",
#         "song": song
#     }
#
#     return {
#         "messages": [
#             ToolMessage(content=json.dumps(action_json), tool_call_id="music_agent")
#         ]
#     }
# 意图 prompt
def build_intent_prompt(user_input: str) -> str:
    return f"""
你是一个音乐助手，用户会对你说播放控制类指令，你需要根据用户的输入，提取意图 intent 和歌曲名 song，返回标准 JSON 格式。

规则：
- 如果用户要播放指定歌曲，intent 用 "play"，song 填歌曲名
- 如果是下一首，intent 用 "next"，song 填 null
- 如果是上一首，intent 用 "prev"，song 填 null
- 如果是暂停，intent 用 "pause"，song 填 null
- 只输出 JSON，不能有其他文字

示例：
用户输入: 播放周杰伦的稻香
输出: {{"intent": "play", "song": "稻香"}}

用户输入: 下一首
输出: {{"intent": "next", "song": null}}

用户输入: 暂停
输出: {{"intent": "pause", "song": null}}

用户输入: {user_input}
输出:
"""
