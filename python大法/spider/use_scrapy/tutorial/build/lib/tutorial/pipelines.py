# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import pymongo
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline

"""
Item Pipeline的作用
清洗HTML数据
验证爬取数据，检查爬取字段
查重并丢弃重复内容
将爬取结果储存到数据库
"""


class TextPipeline(object):
    def __init__(self):
        self.limit = 50

    def process_item(self, item, spider):
        """
        必须实现的方法
        :param item:
        :param spider:
        :return:
        Item对象：低优先级的Item Pipeline继续处理
        DropItem异常：Item被丢弃，不处理
        """
        if item['text']:
            if len(item['text']) > 50:
                item['text'] = item['text'][0:self.limit].rstrip() + '...'
            return item
        else:
            return DropItem('Missing text')


class MongoDBPipeline(object):
    def __init__(self, connection_url, database):
        self.connection_url = connection_url
        self.database = database

    @classmethod
    def from_crawler(cls, crawler):
        """
        返回一个Class实例。通过crawler可以拿到Scrapy所有的核心组件，如配置
        :param crawler:
        :return:
        """
        return cls(connection_url=crawler.settings.get('MONGODB_URL_STRING'),
                   database=crawler.settings.get('MONGODB_DATABASE'))

    def open_spider(self, spider):
        """
        Spider开启的时候默认调用，在这里进行初始化操作，如连接数据库
        :param spider:
        :return:
        """
        self.client = pymongo.MongoClient(self.connection_url)
        self.db = self.client[self.database]

    def process_item(self, item, spider):
        name = item.__class__.__name__
        self.db[name].insert(dict(item))
        return item

    def close_spider(self, spider):
        """
        数据库关闭的时候使用，可以关闭数据库连接
        """
        self.client.close()
