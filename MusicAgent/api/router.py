from fastapi import APIRouter, HTTPException
from models.schema import InferenceRequest, InferenceResponse
from services.graph_builder import graph
import json

router = APIRouter()

@router.post("/infer", response_model=InferenceResponse)
def infer(request: InferenceRequest):
    try:
        print("router-📥 用户输入：", request.user_input)

        # 初始化状态
        state = {
            "user_input": request.user_input,
            "intent": "",
            "messages": []
        }

        # 执行 LangGraph
        result = graph.invoke(state)
        print("router-✅ LangGraph 返回状态：", result)

        messages = result.get("messages", [])
        if not messages:
            raise ValueError("❌ LangGraph 返回的 messages 为空")

        last_msg = messages[-1]
        print("router🧠 最终消息对象：", last_msg)
        print("router📄 内容类型：", type(last_msg.content), "，内容值：", last_msg.content)

        if last_msg.type == "tool":
            # 若是字符串形式的 dict，则使用 json.loads
            content = last_msg.content
            try:
                data = json.loads(content) if isinstance(content, str) else content
                response_type = data.get("type")

                if response_type == "music":
                    return {
                        "type": "music",
                        "intent": data.get("intent"),
                        "song": data.get("song")
                    }
                elif response_type == "navigation":
                    return {
                        "type": "navigation",
                        "destination": data.get("destination"),
                        "poi_type": data.get("poi_type"),
                        "mode": data.get("mode"),
                    }
                else:
                    raise ValueError(f"未知的 tool 响应类型：{response_type}")
            except Exception as e:
                print("⚠️ tool message 内容解析失败：", str(e))
                raise

        else:
            return {
                "type": "chat",
                "reply": str(last_msg.content)
            }

    except Exception as e:
        print("router🔥 处理过程出错：", str(e))
        raise HTTPException(status_code=500, detail=f"后端异常：{str(e)}")
