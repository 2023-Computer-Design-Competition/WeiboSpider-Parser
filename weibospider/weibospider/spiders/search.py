# -*- coding: utf-8 -*-

from scrapy import Request, Spider
import json
import re
import json
import dateutil.parser
from scrapy_redis.spiders import RedisSpider


class SearchSpider(RedisSpider):
    name = "search_spider"
    base_url = "https://s.weibo.com/"
    redis_key = "search_spider:mid_urls"

    def parse(self, response):
        """
        解析推文
        """
        data = json.loads(response.text)
        item = self.parse_tweet_info(data)
        # item['keyword'] = response.meta['keyword']
        if item['isLongText']:
            url = "https://weibo.com/ajax/statuses/longtext?id=" + item['mblogid']
            yield Request(url, callback=self.parse_long_tweet, meta={'item': item})
        else:
            yield item

    def parse_tweet_info(self, data):
        """
        解析推文数据
        """
        tweet = {
            "_id": str(data['id']),
            "mblogid": data['mblogid'],
            "created_at": dateutil.parser.parse(data['created_at']).strftime('%Y-%m-%d %H:%M:%S'),
            "geo": data['geo'],
            "ip_location": data.get('region_name', None),
            "reposts_count": data['reposts_count'],
            "comments_count": data['comments_count'],
            "attitudes_count": data['attitudes_count'],
            "source": data['source'],
            "content": data['text_raw'].replace('\u200b', ''),
            'isLongText': False,
            "user_id": str(data['user']['id']),
        }
        if 'page_info' in data and data['page_info'].get('object_type', '') == 'video':
            tweet['video'] = data['page_info']['media_info']['mp4_720p_mp4']
        tweet['url'] = f"https://weibo.com/{tweet['user_id']}/{tweet['mblogid']}"
        if 'continue_tag' in data and data['isLongText']:
            tweet['isLongText'] = True
        return tweet

    def parse_long_tweet(self, response):
        """
        解析长推文
        """
        data = json.loads(response.text)['data']
        item = response.meta['item']
        item['content'] = data['longTextContent']
        yield item
