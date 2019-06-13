import re
import string
from decimal import Decimal

import scrapy
from pyquery import PyQuery

from oxygendemo.items import OxygenItem
"""from oxygendemo.constants import IN_STOCK, OUT_OF_STOCK, TYPE_GUESS_KEYWORDS_MAP, \
    GENDER_GUESS_KEYWORDS_MAP, COLORS, GENDER_FEMALE
"""

class OxygenSpider(scrapy.Spider):
    """
        Spider class implemention for numerama.com
    """
    name = "numerama"
    base_url = "https://www.numerama.com/"
    start_urls = ["https://www.numerama.com/"]


    def parse(self, response):
        pq = PyQuery(response.body)

        category_href_list = [c.attr("href") for c in pq("ul.header-container_taxonomy li a").items()]
        for href in category_href_list:
            yield scrapy.Request(url=self.get_absolute_url(href), callback=self.parse_category_page)

    def parse_category_page(self, response):
        pq = PyQuery(response.body)
        item_href_list = [c.attr("href") for c in pq("article.post-grid a").items()]
        for href in item_href_list:
            yield scrapy.Request(url=self.get_absolute_url(href), callback=self.parse_item_page)

    def parse_item_page(self, response):
        pq = PyQuery(response.body)
        item_data = {
            "title": self.get_name(pq),
            "author": self.get_author(pq),
            "description": self.get_description(pq),
            "date": self.get_date(pq)[0],
            "images": self.get_image_urls(pq)[0],
            "tags": self.get_tags(pq),
            "link": response.request.url,
        }
        yield OxygenItem(**item_data)

    def get_absolute_url(self, href):
        return href

    def get_name(self, pq):
        return pq("div.post-title h1").text()


    def get_author(self, pq):
        return pq("span.post-author-bloc_text span a").text()


    def get_description(self, pq):
        return pq("#accordion h3:contains('Description')").next().text()

    def get_date(self, pq):
        return [c.attr("datetime") for c in pq("span.post-author-bloc_text time").items()]

    def get_image_urls(self, pq):
         return [c.attr("src") for c in pq("img.post-cover__background-image").items()]


    def get_tags(self, pq):
        return [c.text() for c in pq("ul.tags-list li a").items()]
