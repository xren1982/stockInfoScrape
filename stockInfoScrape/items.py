# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class NewscrawlItem(scrapy.Item):
    headlines = scrapy.Field()
    links = scrapy.Field()
    stockname = scrapy.Field()

class StockInfoItem(scrapy.Item):
    stockname = scrapy.Field()
    date = scrapy.Field()
    close = scrapy.Field()
    volume = scrapy.Field()
    open = scrapy.Field()
    high = scrapy.Field()
    low = scrapy.Field()


