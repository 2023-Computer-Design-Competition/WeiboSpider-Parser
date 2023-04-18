# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html
# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

import random
import time
import pymongo
from settings import MONGO_URL
import fake_useragent
import requests
import kdl


class CookieMiddleware(object):
    """
    get random cookie from account pool
    """

    def __init__(self):
        client = pymongo.MongoClient(MONGO_URL)
        self.account_collection = client['weibo_test']['account']
        # self.ua = fake_useragent.UserAgent()

    def process_request(self, request, spider):
        all_count = self.account_collection.count()
        if all_count == 0:
            raise Exception('Current account pool is empty!! The spider will stop!!')
        # request.headers.setdefault('User-Agent', self.ua.random)
        random_index = random.randint(0, all_count - 1)
        random_account = self.account_collection.find({})[random_index]
        # While the account is waiting, sleep 5 seconds
        if random_account["status"] == "waiting":
            self.account_collection.find_one_and_update({'cookie': random_account['cookie']},
                                                        {'$set': {'status': 'available'}}, )
            time.sleep(5)
        request.headers.setdefault('Cookie', random_account['cookie'])
        request.meta['account'] = random_account


class RedirectMiddleware(object):
    """
    check account status
    HTTP Code = 302/418 -> cookie is expired or banned, and account status will change to 'error'
    """

    def __init__(self):
        client = pymongo.MongoClient(MONGO_URL)
        self.account_collection = client['weibo_test']['account']

    def process_response(self, request, response, spider):
        http_code = response.status
        if http_code == 302 or http_code == 403:
            self.account_collection.find_one_and_update({'cookie': request.meta['account']['cookie']},
                                                        {'$set': {'status': 'waiting'}}, )
            spider.logger.error('302 or 403 error!!!!!!!!!!!!!!')
            time.sleep(30)
            return request
        elif http_code == 418 or http_code == 400:
            spider.logger.error('418 or 400 error!!!!!!!!!!!!!!!!')
            time.sleep(30)
            return request
        else:
            return response


class IPProxyMiddleware(object):
    # _proxy = ('l854.kdltps.com', '15818')
    def fetch_proxy(self):
        pass
        # You need to rewrite this function if you want to add proxy pool
        # the function should return a ip in the format of "ip:port" like "12.34.1.4:9090"
        # username = "t17843481328374"
        # password = "bnvth9hz"
        # proxy = "http://%(proxy)s/" % {"proxy": ':'.join(IPProxyMiddleware._proxy)}
        # return proxy

    def process_request(self, request, spider):
        auth = kdl.Auth('omn7fa9ro3zx6fbvy2im', 'v2fmtctj6fr1yqyzffoaq4tv0ww03u1g')
        client = kdl.Client(auth, timeout=(8, 12), max_retries=3)
        ip = client.get_kps(1, sign_type='token')
        username = "bestlemoon"
        password = "jpffrtg8"
        request.meta['proxy'] = "http://%(user)s:%(pwd)s@%(proxy)s/" % {"user": username, "pwd": password,
                                                                        "proxy": ip}
    #     proxy_data = self.fetch_proxy()
    #     if proxy_data:
    #         current_proxy = f'http://{proxy_data}'
        spider.logger.debug(f"current proxy:{ip}")
    #         request.meta['proxy'] = current_proxy
    #
    #
