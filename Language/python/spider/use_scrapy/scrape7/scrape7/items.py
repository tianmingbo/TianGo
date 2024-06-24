# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Field, Item


class BookItem(Item):
    authors = Field()
    comments = Field()
    isbn = Field()
    name = Field()
    score = Field()
    tags = Field()
    page_number = Field()
