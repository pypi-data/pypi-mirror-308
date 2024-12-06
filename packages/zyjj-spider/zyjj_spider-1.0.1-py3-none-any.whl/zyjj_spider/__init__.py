from zyjj_spider.base import Base
from zyjj_spider.spider import BilibiliSpider, DouyinSpider
from zyjj_spider.utils import async_run

class Spider:
    def __init__(self):
        self.base = Base()

    def bilibili(self, cookie: str) -> BilibiliSpider:
        return BilibiliSpider(base=self.base, cookie=cookie)

    def douyin(self, cookie: str) -> DouyinSpider:
        return DouyinSpider(base=self.base, cookie=cookie)
