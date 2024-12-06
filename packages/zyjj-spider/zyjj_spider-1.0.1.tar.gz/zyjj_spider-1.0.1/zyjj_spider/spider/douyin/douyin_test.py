import json

from zyjj_spider.base import Base
from zyjj_spider.spider import DouyinSpider
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
import pytest

base = Base()
spider = DouyinSpider(base)

@pytest.mark.asyncio
async def test_awemeid():
    # res = await spider.tool_aweme_id_get("https://v.douyin.com/CeiQcRy") # 7395912224755272975
    res = await spider.video_detail_get('7402640148564921652') # 7395912224755272975
    # res = await spider.get_ms_token() # 7395912224755272975
    print("")
    print(res)
    print(json.dumps(res, ensure_ascii=False))
# https://www.douyin.com/aweme/v1/web/aweme/detail/?device_platform=webapp&aid=6383&channel=channel_pc_web&pc_client_type=1&version_code=190500&version_name=19.5.0&cookie_enabled=true&screen_width=1920&screen_height=1080&browser_language=zh-CN&browser_platform=Win32&browser_name=Edge&browser_version=122.0.0.0&browser_online=true&engine_name=Blink&engine_version=122.0.0.0&os_name=Windows&os_version=10&cpu_core_num=12&device_memory=8&platform=PC&downlink=10&effective_type=4g&round_trip_time=100&msToken=274Y6xirKKMs9t8+Zq+F8NqzKyjcZ65fx9HefrEWGnUgH6sFjAXKSbLbc4XltGmsbEZN4dcd6QfSre1wKKLhEez4+ffmY-1udKNWxGeDLye2A+ZDr1hQ0S-EmPCY7j==&aweme_id=7402640148564921652&a_bogus=YymqQmzdp3jBgESG5RCLfY3q66p3YmCV0SVkMD2fPVfVf639HMTs9exoqBTvxWbjNG/pIeEjy4hbYrOdrQCHM1wfHSsw/2CZsLs0t-P2so0j53inCLbsE0hN-iW3SFFp5hNAEO4gy75bFYz0WonamhK4bfebY7Y6i6trEf==
# https://www.douyin.com/aweme/v1/web/aweme/detail/?aweme_id=7402640148564921652&device_platform=webapp&aid=6383&channel=channel_pc_web&pc_client_type=1&version_code=190500&version_name=19.5.0&cookie_enabled=true&screen_width=1920&screen_height=1080&browser_language=zh-CN&browser_platform=Win32&browser_name=Edge&browser_version=122.0.0.0&browser_online=true&engine_name=Blink&engine_version=122.0.0.0&os_name=Windows&os_version=10&cpu_core_num=12&device_memory=8&platform=PC&downlink=10&effective_type=4g&round_trip_time=100&msToken=XaKa8cNWXuFpy0sCzmsriNSwph-8J6QnuE5EeFWpuL1paFA6OLMHwcEp8czXyjGkW4jOoCdxR_BJFyoQ6qpBp41L-qZvdoQN2QeMMA5EBmzApJpuPR13JI5PIxuOSA==&a_bog us=OjmZBQhdpryp6nWY54oLfY3q6Vp3Ymef0SVkMD2ffdfV4L39HMTj9exoxFivPFDjNG/pIeYjy4hbY3nQrQcj8HwfHWwq/25MsfSkKl12so0j53inC6fQE0wL-XsAtlHmsvHRECi8qw2nSYmklVAJ5kIlO62-zo0/9Aj=

def sort_url_query(url):
    # 解析 URL
    parsed_url = urlparse(url)

    # 解析查询参数
    query_params = parse_qs(parsed_url.query)

    # 对查询参数进行排序
    sorted_query_params = dict(sorted(query_params.items()))

    # 编码排序后的查询参数
    sorted_query_string = urlencode(sorted_query_params, doseq=True)

    # 重新构建完整的 URL
    sorted_url = urlunparse(parsed_url._replace(query=sorted_query_string))

    return sorted_url
def test_url_parse():
    # print(sort_url_query('https://www.douyin.com/aweme/v1/web/aweme/detail/?device_platform=webapp&aid=6383&channel=channel_pc_web&pc_client_type=1&version_code=190500&version_name=19.5.0&cookie_enabled=true&screen_width=1920&screen_height=1080&browser_language=zh-CN&browser_platform=Win32&browser_name=Edge&browser_version=122.0.0.0&browser_online=true&engine_name=Blink&engine_version=122.0.0.0&os_name=Windows&os_version=10&cpu_core_num=12&device_memory=8&platform=PC&downlink=10&effective_type=4g&round_trip_time=100&msToken=274Y6xirKKMs9t8+Zq+F8NqzKyjcZ65fx9HefrEWGnUgH6sFjAXKSbLbc4XltGmsbEZN4dcd6QfSre1wKKLhEez4+ffmY-1udKNWxGeDLye2A+ZDr1hQ0S-EmPCY7j==&aweme_id=7402640148564921652&a_bogus=YymqQmzdp3jBgESG5RCLfY3q66p3YmCV0SVkMD2fPVfVf639HMTs9exoqBTvxWbjNG/pIeEjy4hbYrOdrQCHM1wfHSsw/2CZsLs0t-P2so0j53inCLbsE0hN-iW3SFFp5hNAEO4gy75bFYz0WonamhK4bfebY7Y6i6trEf=='))
    print(sort_url_query('https://www.douyin.com/aweme/v1/web/aweme/detail/?aweme_id=7395912224755272975&device_platform=webapp&aid=6383&channel=channel_pc_web&pc_client_type=1&version_code=190500&version_name=19.5.0&cookie_enabled=true&screen_width=1920&screen_height=1080&browser_language=zh-CN&browser_platform=Win32&browser_name=Edge&browser_version=122.0.0.0&browser_online=true&engine_name=Blink&engine_version=122.0.0.0&os_name=Windows&os_version=10&cpu_core_num=12&device_memory=8&platform=PC&downlink=10&effective_type=4g&round_trip_time=100&msToken=9klq6CWCBSkRHc9FnQ85WbVoNONeFa6Vyhrn9_3lKrgV4NmnY8W7VXkqHhJ6BsX1E2wP91DR5ASYGnDs4tj0jEhdbZxY2NAbNDkWHAE7Ijr4KB_ui563BZPLWcl64A==&&a_bogus=DXWhBfz3prnPkEyS54CLfY3q63l3YmeJ0SVkMD2fExfVuy39HMPi9exoN0wvA9WjNG/pIeLjy4hbYNCprQ2G01wfHuUw/25DmfSkKl5Q5xSSs1XHeLkgrUkq5wsAtee0sv1liOmkqwICFuR2WoFe-wHvPjojx2f39gbk'))

# https://www.douyin.com/aweme/v1/web/aweme/detail/?a_bogus=YymqQmzdp3jBgESG5RCLfY3q66p3YmCV0SVkMD2fPVfVf639HMTs9exoqBTvxWbjNG%2FpIeEjy4hbYrOdrQCHM1wfHSsw%2F2CZsLs0t-P2so0j53inCLbsE0hN-iW3SFFp5hNAEO4gy75bFYz0WonamhK4bfebY7Y6i6trEf%3D%3D&aid=6383&aweme_id=7402640148564921652&browser_language=zh-CN&browser_name=Edge&browser_online=true&browser_platform=Win32&browser_version=122.0.0.0&channel=channel_pc_web&cookie_enabled=true&cpu_core_num=12&device_memory=8&device_platform=webapp&downlink=10&effective_type=4g&engine_name=Blink&engine_version=122.0.0.0&msToken=274Y6xirKKMs9t8+Zq+F8NqzKyjcZ65fx9HefrEWGnUgH6sFjAXKSbLbc4XltGmsbEZN4dcd6QfSre1wKKLhEez4+ffmY-1udKNWxGeDLye2A+ZDr1hQ0S-EmPCY7j%3D%3D&os_name=Windows&os_version=10&pc_client_type=1&platform=PC&round_trip_time=100&screen_height=1080&screen_width=1920&version_code=190500&version_name=19.5.0
# https://www.douyin.com/aweme/v1/web/aweme/detail/?a_bogus=DXWhBfz3prnPkEyS54CLfY3q63l3YmeJ0SVkMD2fExfVuy39HMPi9exoN0wvA9WjNG%2FpIeLjy4hbYNCprQ2G01wfHuUw%2F25DmfSkKl5Q5xSSs1XHeLkgrUkq5wsAtee0sv1liOmkqwICFuR2WoFe-wHvPjojx2f39gbk&aid=6383&aweme_id=7395912224755272975&browser_language=zh-CN&browser_name=Edge&browser_online=true&browser_platform=Win32&browser_version=122.0.0.0&channel=channel_pc_web&cookie_enabled=true&cpu_core_num=12&device_memory=8&device_platform=webapp&downlink=10&effective_type=4g&engine_name=Blink&engine_version=122.0.0.0&msToken=9klq6CWCBSkRHc9FnQ85WbVoNONeFa6Vyhrn9_3lKrgV4NmnY8W7VXkqHhJ6BsX1E2wP91DR5ASYGnDs4tj0jEhdbZxY2NAbNDkWHAE7Ijr4KB_ui563BZPLWcl64A%3D%3D&os_name=Windows&os_version=10&pc_client_type=1&platform=PC&round_trip_time=100&screen_height=1080&screen_width=1920&version_code=190500&version_name=19.5.0
def test_xbogus():
    from zyjj_spider.spider.douyin.xbogus import XBogus
    xb = XBogus()
    print(xb.getXBogus('aweme_id=7395912224755272975'))