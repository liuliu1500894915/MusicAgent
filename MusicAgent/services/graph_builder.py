# services/graph_builder.py
from langgraph.graph import StateGraph, END, START
from typing_extensions import TypedDict, Annotated
from operator import add
from langchain_core.messages import HumanMessage
from services.intent_node import intent_router_node
from services.chat_agent import chat_node
from services.music_agent import music_node
from services.navigation_agent import navigation_node
from models.schema import AgentState


# 构建 LangGraph 工作流
builder = StateGraph(AgentState)

# 添加节点
builder.add_node("intent_router", intent_router_node)
builder.add_node("chat_agent", chat_node)
builder.add_node("music_agent", music_node)
builder.add_node("navigation_agent", navigation_node)

# 条件路由：根据 intent 字段跳转到对应节点
builder.add_conditional_edges("intent_router", lambda state: state["intent"])

# 意图子图回到 END
builder.add_edge("chat_agent", END)
builder.add_edge("music_agent", END)
builder.add_edge("navigation_agent", END)
builder.set_entry_point("intent_router")

# 编译图对象
graph = builder.compile()
