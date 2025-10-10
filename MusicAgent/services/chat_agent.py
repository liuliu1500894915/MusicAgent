from models.schema import AgentState
from langchain_core.messages import HumanMessage, AIMessage
from langchain_community.chat_models import ChatZhipuAI

# 复用大模型
llm = ChatZhipuAI(
    zhipuai_api_key="16d7bb61e4fb438fb212266be2ba7478.7To5DD4sn6lBliwG",
    model="glm-4-plus"
)

def chat_node(state: AgentState) -> dict:
    user_input = state["user_input"]
    print("💬 Chat Node 收到用户输入：", user_input)

    response = llm.invoke([HumanMessage(content=user_input)])
    print("chat_node-🧠 ChatGLM 回复：", response.content)

    return {
        "messages": [AIMessage(content=response.content)]
    }
