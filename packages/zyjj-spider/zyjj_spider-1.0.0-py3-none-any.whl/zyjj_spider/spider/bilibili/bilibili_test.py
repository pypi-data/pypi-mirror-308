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
