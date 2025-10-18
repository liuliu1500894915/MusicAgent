# models/schema.py
from pydantic import BaseModel, Field
from typing import Literal, Optional
from typing import Union
from typing_extensions import TypedDict, Annotated
from operator import add

# 定义全局状态格式（包含用户输入、意图、模型回复等）
class AgentState(TypedDict):
    user_input: str
    intent: str
    messages: Annotated[list, add]  # 聊天记录追加式维护（如需）

class InferenceRequest(BaseModel):
    user_input: str = Field(..., description="用户输入文本（来自语音识别）")

# 请求模型：用户输入
class InferenceResponse(BaseModel):
    type: Literal["chat", "music", "navigation"]
    reply: Optional[str] = None  # 聊天回复
    intent: Optional[str] = None  # 播放器控制指令，如 play_song、pause 等
    song: Optional[str] = None    # 若是播放歌曲，返回的歌曲名
    destination: Optional[str] = None  # 导航目的地
    poi_type: Optional[str] = None  # 导航地点类型（如餐厅、加油站）
    mode: Optional[str] = None  # 导航方式（如驾车、步行）

# 音乐控制响应体格式
class MusicActionResponse(BaseModel):
    type: Literal["music"]
    intent: Literal["play", "pause", "next", "prev", "volume_up", "volume_down", "mute", "play_song"]
    song: Optional[str] = None  # 播放指定歌曲时可能包含

# 导航响应体格式
class NavigationResponse(BaseModel):
    type: Literal["navigation"]
    destination: Optional[str] = Field(
        None,
        description="用户想要导航的目的地，若只给出类型或未提及则为空",
    )
    poi_type: Optional[str] = Field(None, description="目的地类型或兴趣点分类")
    mode: Optional[str] = Field(None, description="导航方式，如驾车、步行")

# 聊天响应体格式
class ChatResponse(BaseModel):
    type: Literal["chat"]
    reply: str = Field(..., description="聊天回复内容")

# 响应模型的联合类型
InferenceResponse = Union[MusicActionResponse, ChatResponse, NavigationResponse]
