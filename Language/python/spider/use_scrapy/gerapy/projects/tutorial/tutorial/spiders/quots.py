import scrapy

from tutorial.items import TutorialItem


class QuotsSpider(scrapy.Spider):
    name = 'quotes'  # 每个项目唯一的名字，区分Spider
    allowed_domains = ['quotes.toscrape.com']  # 允许爬取的域名，不是这个域名下的请求会过滤
    start_urls = ['http://quotes.toscrape.com/']  # 启动时的URL列表，这里定义了初始请求

    def parse(self, response):
        # 解析返回的数据
        quotes = response.css('.quote')
        for quote in quotes:
            item = TutorialItem()
            item['text'] = quote.css('.text::text').extract_first()
            item['author'] = quote.css('.author::text').extract_first()  # 导出第一个
            item['tags'] = quote.css('.tags .tag::text').extract()  # 导出所有
            yield item
        next_page = response.css('.pager .next a::attr("href")').extract_first()  # 获取下一页链接
        url = response.urljoin(next_page)
        yield scrapy.Request(url=url, callback=self.parse)
