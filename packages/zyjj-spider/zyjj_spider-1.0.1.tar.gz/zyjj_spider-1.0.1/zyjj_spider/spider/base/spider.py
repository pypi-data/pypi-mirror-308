import json
import logging
from zyjj_spider.base.exception import RequestException, ServerException
from httpx import AsyncClient, Response, URL
from zyjj_spider.base import Base
import random
from typing import Callable, Union

agent_list = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0",
]


class BaseSpider:
    def __init__(
        self,
        base: Base,
        base_url: str = '',
        extra_header: dict = None,
        timeout: int = 30,
        agent: str = None
    ):
        self.agent = random.choice(agent_list) if agent is None else agent
        header = self.__get_base_header()
        if extra_header is not None:
            header.update(extra_header)
        logging.info(f"header is {header}")
        self.__aclient = AsyncClient(
            base_url=base_url,
            headers=header,
            timeout=timeout,
        )

    def __get_base_header(self):
        return {
            "user-agent": self.agent
        }

    # 底层请求
    async def __request(self, method: str, url: str, data: dict = None) -> Response:
        # 兼容//的情况
        if url.startswith("//"):
            url = "https:" + url
        response = await self.__aclient.request(method, url, json=data, follow_redirects=True)
        if response.status_code != 200:
            raise RequestException(response.status_code, url)
        if not response.text.strip() or not response.content:
            raise ServerException(-1, "返回为空")
        return response

    # json请求
    async def request_get_json(self, url: str, process: Callable[[dict], dict] = lambda a: a) -> Union[dict, list]:
        return process((await self.__request('get', url)).json())

    # 发送post json请求
    async def request_post_json(self, url: str, data: dict, process: Callable[[dict], dict] = lambda a: a) -> Union[dict, list]:
        return process((await self.__request('post', url, data)).json())

    # 发送post json请求
    async def request_post_raw(self, url: str, data: dict) -> Response:
        return await self.__request('POST', url, data)

    # 获取请求文本信息
    async def request_get_content(self, url: str) -> bytes:
        return (await self.__request('get', url)).content

    async def request_get_redirect_url(self, url: str) -> URL:
        return (await self.__request('get', url)).url

    async def close(self):
        await self.__aclient.aclose()
