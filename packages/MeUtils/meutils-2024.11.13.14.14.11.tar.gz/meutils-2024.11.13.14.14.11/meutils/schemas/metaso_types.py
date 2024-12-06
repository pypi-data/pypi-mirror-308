#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : metaso_types
# @Time         : 2024/11/11 17:26
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *

BASE_URL = "https://metaso.cn"
FEISHU_URL = "https://xchatllm.feishu.cn/sheets/Bmjtst2f6hfMqFttbhLcdfRJnNf?sheet=cyKbvv"


class MetasoRequest(BaseModel):
    question: str = "Chatfire"

    """search-mini search search-pro"""
    mode: Literal["concise", "detail", "research"] = "detail"  # concise detail research
    scholarSearchDomain: str = "all"
    engineType: str = ""

    searchTopicId: Optional[str] = None
    searchTopicName: Optional[str] = None

    # 自定义字段
    response_format: Optional[str] = None  # 原生内容

    class Config:
        frozen = True


class MetasoResponse(BaseModel):  # sse

    type: Optional[str] = None  # query set-reference heartbeat append-text
    content: str = ""

    data: Optional[dict] = None

    # 原生内容
    chunk: str

    def __init__(self, /, **data: Any):
        super().__init__(**data)

        chunk = self.chunk.lstrip("data:")
        self.data = json.loads(chunk)

        self.type = self.data.get("type")
        self.content = self.data.get("text", "")

        # {'realQuestion': '你是谁', 'data': [], 'label': '', 'id': '8544588308750417920', 'type': 'query'}
        if self.type == "query":
            # self.content = f"""> search( {self.data.get("realQuestion")}: {self.data.get("data")} )\n"""
            self.content = f"""> 🚀Search( {self.data.get("realQuestion")}: {self.data.get("data")} )\n"""


if __name__ == '__main__':
    chunk = """data:{"type":"heartbeat"}"""

    print(MetasoResponse(chunk=chunk))
