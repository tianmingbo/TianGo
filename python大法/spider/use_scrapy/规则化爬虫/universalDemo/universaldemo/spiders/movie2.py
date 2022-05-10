from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..items import MovieItem


class MovieSpider(CrawlSpider):
    name = 'movie2'
    allowed_domains = ['ssr1.scrape.center']
    start_urls = ['http://ssr1.scrape.center/']
    
    rules = (
        Rule(LinkExtractor(restrict_css='.item .name'), follow=True, callback='parse_detail'),
        Rule(LinkExtractor(restrict_css='.next'), follow=True),
    )
    
    def parse_detail(self, response):
        item = MovieItem()
        item['name'] = response.css('.item h2::text').extract_first()
        item['categories'] = response.css('.categories button span::text').extract()
        item['cover'] = response.css('.cover::attr(src)').extract_first()
        item['published_at'] = response.css('.info span::text').re_first('(\d{4}-\d{2}-\d{2})\s?上映')
        item['score'] = response.xpath('//p[contains(@class, "score")]/text()').extract_first().strip()
        item['drama'] = response.xpath('//div[contains(@class, "drama")]/p/text()').extract_first().strip()
        yield item
