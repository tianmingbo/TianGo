# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter


class TutorialSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        """
        当Response通过爬虫中间件时，process_spider_input被调用
        :param response:
        :param spider:
        :return:
        None: 继续处理response，直到spider处理Response
        raise an exception:
        """
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        """
        当spider处理Response返回结果时，process_spider_output方法被调用
        :param response:
        :param result: 包含Request或Item对象的可迭代对象，即spider的返回结果
        :param spider:
        :return:
        必须返回包含Request或Item对象的可迭代对象
        """
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        """
        当spider或process_spider_input抛出异常时，process_spider_exception方法被调用
        :param response:
        :param exception: 被抛出的异常
        :param spider:
        :return:
        必须返回一个None或者（包含Response或Item对象的）可迭代对象
        None：其它中间件继续处理该异常
        可迭代对象：其他中间件的process_spider_output被调用
        """
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class TutorialDownloaderMiddleware:
    """
    下载器中间件，核心方法是
    process_request
    process_response
    process_exception
    """

    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        """
        :param request:
        :param spider:
        :return:
        None: 继续执行其他中间件的process_request
        Response: 低优先级的process_request停止执行，开始执行process_response
        Request: 低优先级的process_request停止执行，放入调度器
        IgnoreRequest: 执行process_exception
        """
        return None

    def process_response(self, request, response, spider):
        """
        :param request:
        :param response:
        :param spider:
        :return:
        Request: 低优先级的process_response停止执行，放入调度器
        Response: 继续执行
        IgnoreRequest:
        """
        return response

    def process_exception(self, request, exception, spider):
        """

        :param request: 产生异常的Request
        :param exception: 抛出的异常
        :param spider:
        :return:
        None: 低优先级的下载中间件的process_exception继续执行
        Response: 低优先级的process_exception不再执行，执行process_response方法
        Request: 低优先级的process_exception不再执行，该对象会重新放入调度队列中
        """
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class ProxyMiddleware(object):
    """
    修改代理
    """

    def process_request(self, request, spider):
        request.meta['proxy'] = 'http://****'
