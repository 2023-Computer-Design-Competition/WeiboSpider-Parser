# -*- coding: utf-8 -*-
# @Time    : 2023/2/7 14:05
# @Author  : Lemoon
# @FileName: redis_search_init.py
# @Software: PyCharm
import redis
from settings import REDIS_URL

keywords = ['丽江']
start_time = "2022-10-01-0"  # 格式为 年-月-日-小时, 2022-10-01-0 表示2022年10月1日0时
end_time = "2022-10-08-23"  # 格式为 年-月-日-小时, 2022-10-07-23 表示2022年10月7日23时
is_search_with_specific_time_scope = True  # 是否在指定的时间区间进行推文搜索
is_sort_by_hot = True  # 是否按照热度排序,默认按照时间排序
r = redis.Redis.from_url(REDIS_URL)
for keyword in keywords:
    if is_search_with_specific_time_scope:
        url = f"https://s.weibo.com/weibo?q={keyword}&timescope=custom%3A{start_time}%3A{end_time}&page=1"
    else:
        url = f"https://s.weibo.com/weibo?q={keyword}&page=1"
    if is_sort_by_hot:
        url += "&xsort=hot"
    r.lpush('search:start_urls', url)
    print("Added: ", url)
