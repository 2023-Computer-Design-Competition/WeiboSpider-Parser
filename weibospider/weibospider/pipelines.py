# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from settings import MONGO_URL
from datetime import datetime
import time


class WeibospiderPipeline(object):
    def process_item(self, item, spider):
        client = pymongo.MongoClient(MONGO_URL)
        db = client["weibo"]
        now = datetime.now()
        # Add date to classify the data
        # collection = db["Tweets-" + now.strftime("%Y-%m-%d-%H-%M-%S")]
        collection = db["Tweets"]
        item["crawl_time_stamp"] = int(time.time())
        item["crawl_time"] = now.strftime("%Y-%m-%d-%H-%M-%S-%f")
        try:
            collection.insert(dict(item))
        except Exception as e:
            pass
        return item
