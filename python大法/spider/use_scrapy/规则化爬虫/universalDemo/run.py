from scrapy.utils.project import get_project_settings
from universaldemo.utils import get_config
from scrapy.crawler import CrawlerProcess
import argparse

parser = argparse.ArgumentParser(description='Universal Spider')
parser.add_argument('name', help='name of spider to run')
args = parser.parse_args()
name = args.name


# name = 'movie'


def run():
    config = get_config(name)
    spider = config.get('spider', 'universal')
    project_settings = get_project_settings()
    settings = dict(project_settings.copy())
    settings.update(config.get('settings'))
    process = CrawlerProcess(settings)
    process.crawl(spider, **{'name': name})
    process.start()


if __name__ == '__main__':
    run()
