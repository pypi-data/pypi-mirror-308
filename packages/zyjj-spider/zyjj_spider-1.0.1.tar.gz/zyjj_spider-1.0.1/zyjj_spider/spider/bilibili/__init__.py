import re

from zyjj_spider.base import Base, ServerException
from zyjj_spider.spider.base import BaseSpider, extract_valid_urls
from zyjj_spider.spider.bilibili.utils import get_query


class BilibiliSpider:

    def __init__(self, base: Base, cookie: str = ''):
        self.__base = base
        self.__spider = BaseSpider(
            base,
            'https://api.bilibili.com/x/',
            extra_header={
                "cookie": cookie,
                "refer": "https://www.bilibili.com/",
                "origin": "https://www.bilibili.com/",
            }
        )

    # 请求处理
    @staticmethod
    def __res_process(data: dict):
        if data['code'] != 0:
            raise ServerException(data['code'], data['message'])
        return data['data']

    # 获取用户信息
    async def user_info_get(self) -> dict:
        return await self.__spider.request_get_json('web-interface/nav', self.__res_process)

    # 获取web key信息
    async def __web_key_get(self) -> tuple[str, str]:
        info = await self.user_info_get()
        img_url: str = info['wbi_img']['img_url']
        sub_url: str = info['wbi_img']['sub_url']
        img_key = img_url.rsplit('/', 1)[1].split('.')[0]
        sub_key = sub_url.rsplit('/', 1)[1].split('.')[0]
        return img_key, sub_key

    # 获取加密后的查询参数
    async def __get_query(self, param: dict):
        img_key, sub_key = await self.__web_key_get()
        return get_query(img_key, sub_key, param)

    # 获取评论信息 https://github.com/SocialSisterYi/bilibili-API-collect/blob/master/docs/comment/list.md
    async def video_comment_get(self, aid: int, pn=1, ps=20):
        query = await self.__get_query({"oid": aid, "type": 1, "pn": pn, "ps": ps})
        return await self.__spider.request_get_json(f'v2/reply/wbi/main?{query}', self.__res_process)

    # 获取播放列表
    async def video_play_list_get(self, bid: str) -> list:
        return await self.__spider.request_get_json(f'player/pagelist?bvid={bid}', self.__res_process)

    # 获取播放信息
    async def video_play_info_get(self, bid: str, cid: int) -> dict:
        query = await self.__get_query({"bvid": bid, "cid": cid})
        return await self.__spider.request_get_json(f'player/wbi/v2?{query}', self.__res_process)

    # 根据bid获取cid
    async def tool_cid_get(self, bid: str) -> list[int]:
        video_list = await self.video_play_list_get(bid)
        return [i['cid'] for i in video_list]

    # 根据bid获取aid
    async def tool_aid_get(self, bid: str, cid: int) -> list[str]:
        video_info = await self.video_play_info_get(bid, cid)
        return video_info['aid']

    # Bv号提取
    async def tool_bid_get(self, url: str) -> str:
        def get_bid(url: str) -> str:
            # 先判断一下是否可以直接提取bv号
            re_content = re.findall(r'(BV\w+)', url)
            return '' if len(re_content) == 0 else re_content[0]
        # 先尝试直接匹配
        bid = get_bid(url)
        if bid != '':
            return bid
        # 匹配不到，我们尝试提取url ，然后直接重定向
        url = extract_valid_urls(url)
        return get_bid(str(await self.__spider.request_get_redirect_url(url)))

    # 获取播放链接
    async def video_play_url_get(self, bid: str, cid: int) -> dict:
        return await self.__spider.request_get_json(f'player/playurl?fnval=80&cid={cid}&bvid={bid}', self.__res_process)

    # 获取视频信息
    async def video_info_get(self, bid: str, cid: int) -> dict:
        return await self.__spider.request_get_json(f'web-interface/view?fnval=80&cid={cid}&bvid={bid}',
                                                    self.__res_process)

    # 获取视频字幕
    async def video_subtitle_get(self, bid: str, cid: int) -> list:
        play_info = await self.video_play_info_get(bid, cid)
        return play_info.get('subtitle', {}).get('subtitles', [])

    # 下载视频字幕
    async def video_subtitle_download(self, url: str) -> dict:
        return await self.__spider.request_get_json(url)

    # 获取B站弹幕
    async def video_danmu_v1_get(self, cid: int) -> bytes:
        return await self.__spider.request_get_content(f'v1/dm/list.so?oid={cid}')

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.__spider.close()
