from langchain_community.chat_models import ChatZhipuAI
from langchain_core.messages import HumanMessage, AIMessage
from models.schema import AgentState

llm = ChatZhipuAI(
    zhipuai_api_key="16d7bb61e4fb438fb212266be2ba7478.7To5DD4sn6lBliwG",
    model="glm-4-plus"
)

prompt_template = """
你是一个意图识别助手，只需识别用户的指令意图。
请严格按照以下 JSON 格式输出：

{"intent": "music"} 或 {"intent": "chat"}

用户输入："""

def intent_router_node(state: AgentState) -> dict:
    query = state["user_input"]
    prompt = prompt_template + query
    print("intent_router_node-意图识别 Prompt:", prompt)

    response = llm.invoke([HumanMessage(content=prompt)])
    content = response.content.strip()
    print("📤 ChatGLM 返回：", content)

    intent = "chat"  # 默认兜底
    if "music" in content:
        intent = "music_agent"
    elif "chat" in content:
        intent = "chat_agent"

    # 返回包含 intent 和消息流
    return {
        "intent": intent,
        "messages": [
            AIMessage(content=f"intent_router_node-🧠 系统识别用户意图为：{intent}")
        ]
    }
