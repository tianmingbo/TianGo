import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


class ExampleSpider(scrapy.Spider):
    name = "example"
    allowed_domains = ["baidu.com"]
    start_urls = ["https://www.baidu.com/"]

    def parse(self, response):
        print(response.url)


if __name__ == '__main__':
    # 获取默认配置，添加用户配置get_project_settings()
    process = CrawlerProcess(get_project_settings())
    process.crawl(ExampleSpider)
    process.start()
