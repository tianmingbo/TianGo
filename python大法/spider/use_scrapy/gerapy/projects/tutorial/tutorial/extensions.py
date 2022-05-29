# @Time : 2022/5/4 18:16
# @Author :bo~
# @FileName: extensions.py
# @Description: 扩展


import requests
from scrapy import signals

NOTIFY_URL = 'http://localhost:5000/notify'


class NotificationException(object):

    @classmethod
    def from_crawler(cls, crawler):
        # 将方法和scrapy信号绑定
        ext = cls()
        crawler.signals.connect(ext.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(ext.spider_closed, signal=signals.spider_closed)
        crawler.signals.connect(ext.item_scraped, signal=signals.item_scraped)
        return ext

    def spider_opened(self, spider):
        requests.post(NOTIFY_URL, json={'event': 'start', 'data': {'name': spider.name}})

    def spider_closed(self, spider):
        requests.post(NOTIFY_URL, json={'event': 'close', 'data': {'name': spider.name}})

    def item_scraped(self, item, spider):
        requests.post(NOTIFY_URL, json={'event': 'item', 'data': {'name': spider.name}, 'item': dict(item)})
