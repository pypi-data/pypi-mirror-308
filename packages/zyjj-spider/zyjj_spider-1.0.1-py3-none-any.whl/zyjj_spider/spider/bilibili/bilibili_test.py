import json

import pytest

from zyjj_spider.base import Base
from zyjj_spider.spider import BilibiliSpider

base = Base()
spider = BilibiliSpider(base)

@pytest.mark.asyncio
async def test_get_bid_info():
    # res = await spider.get_cid('BV16f4y1F7QQ')
    # res = await spider.video_play_url_get('BV16f4y1F7QQ', 415994521)
    # res = await spider.video_info_get('BV16f4y1F7QQ', 415994521)
    # res = await spider.video_danmu_v1_get(415994521)
    # res = await spider.web_key_get()
    # res = await spider.video_comment_get(378288937)
    # res = await spider.video_play_info_get('BV16f4y1F7QQ', 415994521)
    # res = await spider.video_subtitle_get('BV16f4y1F7QQ', 415994521)
    # res = await spider.video_subtitle_download('//aisubtitle.hdslb.com/bfs/ai_subtitle/prod/378288937415994521bc1ab3df0891daeb9e34ca8f7bf84020?auth_key=1731023923-4e67bd0c188c4ce4b2c8a225fb270396-0-e384f9c9b85909a0a52275fd41437ce5')
    res = await spider.user_info_get()
    print("")
    print(res)
    print(json.dumps(res, ensure_ascii=False))


@pytest.mark.asyncio
async def test_get_bid():
    url1 = "https://www.bilibili.com/video/BV1BPyeY5Ehj/?spm_id_from=333.1007.tianma.1-1-1.click&vd_source=9ccbad7f79eb9981ed9ededbd6531cfb"
    url2 = "https://www.bilibili.com/video/BV1BPyeY5Ehj"
    url3 = "BV1BPyeY5Ehj"
    url4 = "【ドラマスペシャル 2009 椿山課長の七日間_[704☆396]】 https://www.bilibili.com/video/BV1kmmmYAEcW/?share_source=copy_web&vd_source=ae00683721fc1cc834484cfb3f6f954a"
    url5 = "【【python】这个十多年的bug，没点黑魔法还真解决不了-哔哩哔哩】 https://b23.tv/DPqohwo"
    print(await spider.tool_bid_get(url1))
    print(await spider.tool_bid_get(url2))
    print(await spider.tool_bid_get(url3))
    print(await spider.tool_bid_get(url4))
    print(await spider.tool_bid_get(url5))
