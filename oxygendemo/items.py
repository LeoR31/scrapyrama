import scrapy


class OxygenItem(scrapy.Item):
    title = scrapy.Field()
    author = scrapy.Field()
    description = scrapy.Field()
    date = scrapy.Field()
    images = scrapy.Field(serializer=list)
    link = scrapy.Field()
    tags = scrapy.Field(serializer=list)

