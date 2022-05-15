from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst, Identity, Compose

"""
Item是处理数据的容器，ItemLoader提供填充Item的机制
"""


class MovieItemLoader(ItemLoader):
    default_output_processor = TakeFirst()  # 默认取第一个
    categories_out = Identity()  # 直接返回，无操作
    score_out = Compose(TakeFirst(), str.strip)  # 两个函数依次执行
    drama_out = Compose(TakeFirst(), str.strip)
