# -*- coding: utf-8 -*-
# @Time    : 2023/4/5 9:47
# @Author  : TimDiana
# @FileName: db_mid_url.py
# @Software: PyCharm
import redis
from settings import REDIS_URL
from urllib.parse import quote


def redis_init(spider_name, urls):
    r = redis.from_url(REDIS_URL)
    for key in r.scan_iter(f"{spider_name}*"):
        r.delete(key)
    print(f'Add urls to {spider_name}:mid_urls')
    for url in urls:
        r.lpush(f'{spider_name}:mid_urls', url)
        # print('Added:', url)


def init_url():
    urls = []
    with open('../../topic_mid_url.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()  # 读取文件中的所有行
    for line in lines:
        # 对每行数据进行处理
        urls.append(line.strip())  # 去除行末的换行符 '\n'
    redis_init('search_spider', urls)


if __name__ == '__main__':
    init_url()
