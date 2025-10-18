from langchain_community.chat_models import ChatZhipuAI
from langchain_core.messages import HumanMessage, ToolMessage
from models.schema import AgentState
from typing import Optional
import json
import re

llm = ChatZhipuAI(
    zhipuai_api_key="16d7bb61e4fb438fb212266be2ba7478.7To5DD4sn6lBliwG",
    model="glm-4-plus"
)

def navigation_node(state: AgentState) -> dict:
    user_input = state["user_input"]
    print("🧭 navigation_node 收到用户输入：", user_input)

    prompt = build_navigation_prompt(user_input)

    try:
        response = llm.invoke([HumanMessage(content=prompt)])
        print("navigation_node-🧠 GLM 回复：", response.content)

        content_str = response.content.strip()
        match = re.search(r"\{.*\}", content_str, re.DOTALL)
        if not match:
            raise ValueError("未能找到 JSON 内容")

        action_raw = json.loads(match.group(0))
        destination = normalise_destination(
            user_input,
            action_raw.get("destination"),
            action_raw.get("poi_type"),
        )

        action_json = {
            "type": "navigation",
            "destination": destination,
            "poi_type": action_raw.get("poi_type"),
            "mode": action_raw.get("mode"),
        }

        return {
            "messages": [
                ToolMessage(
                    content=json.dumps(action_json, ensure_ascii=False),
                    tool_call_id="navigation_agent"
                )
            ]
        }

    except Exception as e:
        print(f"⚠️ navigation_node 解析出错: {e}")
        return {
            "messages": []
        }

def build_navigation_prompt(user_input: str) -> str:
    return f"""
你是一个导航助手，需要根据用户的指令提取导航相关的信息，并返回 JSON。

请遵守以下要求：
- destination: 优先提取用户提到的具体地点名称或短语（如“最近的蜜雪冰城”），若未提及则返回 null。
- poi_type: 如果用户只提到地点类型（如加油站、超市），请标注该类型，否则为 null。
- mode: 结合用户描述识别导航方式，可选值包括 drive、walk、transit、ride、bike，若未提及返回 null。
- 只输出一个 JSON，对中文保持原样。

示例：
用户输入：带我去最近的加油站
输出：{{"destination": null, "poi_type": "加油站", "mode": "drive"}}

用户输入：我要步行去人民广场
输出：{{"destination": "人民广场", "poi_type": null, "mode": "walk"}}

用户输入：{user_input}
输出：
"""


def normalise_destination(
    user_input: str,
    destination: Optional[str],
    poi_type: Optional[str],
) -> Optional[str]:
    """回填或修正模型返回的目的地信息，避免为 None 时触发响应验证错误。"""

    if destination:
        cleaned = destination.strip()
        if cleaned:
            return cleaned

    extracted = extract_destination_from_text(user_input)
    if extracted:
        return extracted

    if poi_type:
        poi_cleaned = poi_type.strip()
        if poi_cleaned:
            return poi_cleaned

    return None


def extract_destination_from_text(user_input: str) -> Optional[str]:
    """利用简单规则从中文指令中提取目的地短语。"""

    text = user_input.strip()
    if not text:
        return None

    # 常见的导航触发词
    patterns = [
        r"(?:到|去|导航到|导航去|前往|带我去|想去|我要去)([^,，。！？;；]*)",
    ]

    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            candidate = match.group(1).strip()
            if candidate:
                # 去掉开头多余的连接词
                candidate = re.sub(r"^(?:的|到)", "", candidate).strip()
                return candidate or None

    return None
