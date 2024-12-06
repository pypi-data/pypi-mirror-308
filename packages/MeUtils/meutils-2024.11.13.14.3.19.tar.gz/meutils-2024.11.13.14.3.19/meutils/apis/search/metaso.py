#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : meta
# @Time         : 2024/11/11 17:03
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

from meutils.pipe import *
from meutils.schemas.metaso_types import FEISHU_URL, BASE_URL, MetasoRequest, MetasoResponse
from meutils.decorators.retry import retrying
from meutils.config_utils.lark_utils import get_next_token_for_polling
from meutils.apis.proxy.ips import FEISHU_URL_METASO, get_one_proxy, get_proxies
from meutils.schemas.openai_types import ChatCompletionRequest
from meutils.notice.feishu import send_message

token = "wr8+pHu3KYryzz0O2MaBSNUZbVLjLUYC1FR4sKqSW0p19vmcZAoEmHC72zPh/fHtOhYhCcR5GKXrxQs9QjN6dulxfOKfQkLdVkLMahMclPPjNVCPE8bLQut3zBABECLaSqpI0fVWBrdbJptnhASrSw=="


async def get_session_id(request: MetasoRequest, headers: Optional[dict] = None, proxies: Optional[dict] = None):
    if proxies:
        logger.debug(proxies)

    headers = headers or {
        # "cookie": "uid=65fe812a09727c19a54b0328; sid=eb6f4fe9034b4c9497fceca7ff6bafdd",
        # "cookie": f"uid={shortuuid.random(24).lower()}; sid={shortuuid.random(32).lower()}"

        # "cookie": "JSESSIONID=8B267A5E2299C2BF46EB354104AACF76; tid=b103b947-be89-40b8-b162-80fdcda60807; aliyungf_tc=8cfbed3e5fd53c2a81605c7dcb63d45d3114b94750922ef63e04cb5a6ceccba1; s=bdpc; traceid=d21e97f303b546c0; hideLeftMenu=1; usermaven_id_UMO2dYNwFz=1y1t3p1t2t; uid=65fe812a09727c19a54b0328; sid=eb6f4fe9034b4c9497fceca7ff6bafdd; newSearch=false"

        # "token": "wr8+pHu3KYryzz0O2MaBSNUZbVLjLUYC1FR4sKqSW0p19vmcZAoEmHC72zPh/fHtxcdjbUPQpQ+cHJxaEajSgJMlmjIlIUew+aPZMEcnIqI1j3rHg9aAsbcYX/MF8lyJ+zJimUWQ2SOBo4yJQ6yUOQ=="
    }

    payload = request.model_dump(exclude_none=True)
    async with httpx.AsyncClient(base_url=BASE_URL, headers=headers, timeout=30, proxies=proxies) as client:
        response = await client.post("/api/session", json=payload)
        response.raise_for_status()
        data = response.json()

        # logger.debug(bjson(data))

        # {
        #     "errCode": 4001,
        #     "errMsg": "搜索次数超出限制"
        # }
        if data.get("errCode", 0) == 4001:
            logger.debug(data)
            # request_kwargs = {
            #     "proxies": await get_one_proxy(headers.get("cookie"), exclude_ips="154.40.54.76154.12.35.201"),
            #     # "proxies": proxies,
            # }
            # continue

        return data.get("data", {}).get("id")


@alru_cache(ttl=24 * 60 * 60)
@retrying(min=3, predicate=lambda r: r is False)
async def get_access_token(session_id: Optional[str] = None):
    pattern = r'<meta\s+id="meta-token"\s+content="([^"]+)"\s*/>'
    async with httpx.AsyncClient(base_url=BASE_URL, timeout=30) as client:  # 测试token过期时间
        response = await client.get(f"/search/{session_id}")
        response.raise_for_status()

        tokens = re.findall(pattern, response.text)
        if not tokens:
            send_message(response.text, __name__)

        return tokens and tokens[0]


async def create(request: ChatCompletionRequest, response_format: Optional[str] = None):
    MODELS = {
        "search": "detail",
        "search-pro": "research"
    }
    system_fingerprint = request.system_fingerprint
    request = MetasoRequest(
        mode=MODELS.get(request.model, "concise"),
        question=request.last_content,
        response_format=response_format,
    )

    headers = {}
    if request.mode == "research":  # 登录
        cookie = await get_next_token_for_polling(FEISHU_URL)
        headers["cookie"] = cookie

    proxies = {}
    # proxies = await get_proxies()
    session_id = await get_session_id(request, headers=headers, proxies=proxies)
    # session_id = None
    if session_id is None:  # 走代理: 随机轮询
        # ip = "121.196.183.67"
        # proxies = {
        #     "http://": f"http://{ip}:8443",  # 自建 8443
        #     "https://": f"http://{ip}:8443",
        # }
        proxies = await get_one_proxy(feishu_url=FEISHU_URL_METASO)
        session_id = await get_session_id(request, headers=headers, proxies=proxies)

    token = await get_access_token(session_id)
    params = {
        'token': token,

        'question': request.question,
        "sessionId": session_id,
        'lang': 'zh',
        'mode': 'detail',
        # 'url': f'https://metaso.cn/search/{sessionId}?q={q}',
        'enableMix': 'true',
        'scholarSearchDomain': 'all',
        'expectedCurrentSessionSearchCount': '1',
        'newEngine': 'true',
        'enableImage': 'true',
    }

    pattern = re.compile('\[\[(\d+)\]\]')
    async with httpx.AsyncClient(base_url=BASE_URL, headers=headers, params=params, proxies=proxies) as client:
        async with client.stream(method="GET", url="/api/searchV2") as response:
            response.raise_for_status()
            logger.debug(response.status_code)

            reference_mapping = {}
            async for chunk in response.aiter_lines():
                if (chunk := chunk.strip()) and chunk != "data:[DONE]":
                    # logger.debug(chunk)

                    try:
                        response = MetasoResponse(chunk=chunk)

                        if len(response.content) == 1 and response.content.startswith('秘'):  # 替换 模型水印
                            response.content = f"🔥{system_fingerprint}AI搜索，它是一款能够深入理解您的问题的AI搜索引擎。"
                            yield response.content
                            break

                        if request.response_format:  # 返回原始内容，方便二次加工或者debug
                            yield response.data
                            continue

                        if response.type in {"query", "set-reference"}:
                            # logger.debug(bjson(response.data))

                            reference_mapping = {
                                str(i): (
                                        reference.get("link")
                                        or reference.get("url")
                                        or reference.get("file_meta", {}).get("url")
                                )
                                for i, reference in enumerate(response.data.get('list', []), 1)
                            }

                            # logger.debug(bjson(reference_mapping))

                        def replace_ref(match):
                            ref_num = match.group(1)

                            return f"[[{ref_num}]({reference_mapping.get(str(ref_num))})]"

                        _ = pattern.sub(replace_ref, response.content)
                        # print(_)
                        yield _

                    except Exception as e:
                        logger.error(e)
                        logger.debug(response)


if __name__ == '__main__':
    # request = MetasoRequest(question="东北证券", mode='research')
    # request = MetasoRequest(question="你是谁", mode='detail', return_raw=True)  # concise
    # request = MetasoRequest(question="Chatfire", mode='concise', return_raw=False)  # concise

    # request = MetasoRequest(question="Chatfire", mode='detail', return_raw=False)  # concise
    # request = MetasoRequest(question="Chatfire", mode='research', response_format=False)  # concise

    # arun(get_session_id(request))
    # arun(get_access_token(request))

    request = ChatCompletionRequest(
        # model="",
        # model="search",

        model="search-pro",

    )

    arun(create(request))

    # with timer():
    #     session_id = "8544840144331366400"
    #
    #     arun(get_access_token(session_id))

    # wr8+pHu3KYryzz0O2MaBSNUZbVLjLUYC1FR4sKqSW0p19vmcZAoEmHC72zPh/fHtOhYhCcR5GKXrxQs9QjN6dulxfOKfQkLdVkLMahMclPPjNVCPE8bLQut3zBABECLaSqpI0fVWBrdbJptnhASrSw==
