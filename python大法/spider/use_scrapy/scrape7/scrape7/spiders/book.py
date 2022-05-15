import json
from scrapy import Request, Spider


class BookSpider(Spider):
    name = 'book'
    allowed_domains = ['antispider7.scrape.center']
    base_url = 'https://antispider7.scrape.center'
    max_page = 512

    def start_requests(self):
        for page in range(1, self.max_page + 1):
            url = f'{self.base_url}/api/book/?limit=18&offset={(page - 1) * 18}'
            yield Request(url, callback=self.parse_index)

    def parse_index(self, response):
        # print(response.__dict__)
        if response.status == 200:
            data = json.loads(response.text)
            results = data.get('results', [])
            for result in results:
                print(result.get('id'), '*' * 100)
