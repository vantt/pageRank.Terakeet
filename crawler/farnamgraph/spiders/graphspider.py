import sys
import os 
import re
import binascii
from scrapy.selector import Selector
from scrapy.http import HtmlResponse
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

try:
    from urllib.parse import urljoin
except ImportError:
     from urlparse import urljoin

from farnamgraph.items import FarnamgraphItem


class GraphspiderSpider(CrawlSpider):

    name = "graphspider"

    allowed_domains = ["fs.blog"]
    start_urls = ["https://fs.blog/blog"]
    ignore_urls = [
        r"^\/$",
        r"^\/about.*",
        r"^\/best-articles.*",
        r"^\/blog.*",
        r"^\/category.*",
        r"^\/feed.*",
        r"^\/membership.*",
        r"^\/mental-models.*",
        r"^\/newsletter.*",
        r"^\/podcast.*",
        r"^\/popular.*",
        r"^\/prime.*",
        r"^\/principles.*",
        r"^\/privacy-policy.*",
        r"^\/random-articles.*",
        r"^\/reading.*",
        r"^\/search.*",
        r"^\/smart-decisions.*",
        r"^\/sponsorship.*",
        r"^\/tags.*",
        r"^https:\/\/fs\.blog\/prime.*",
        r"^https:\/\/twitter\.com\/farnamstreet.*",
        r"^https:\/\/www\.youtube\.com\/user\/farnamstreetblog.*",
        r"^https:\/\/www\.instagram\.com\/farnamstreet.*",
        r"^https:\/\/www\.facebook\.com\/FarnamStreet.*",
        r"^https:\/\/syruspartners\.com.*",
        r"^https:\/\/pressable\.com.*",
        r"^https:\/\/cottonbureau\.com\/products\/listen-and-learn-crewneck-tee.*",
        r"^https:\/\/rethinkworkshops\.com.*",
    ]

    rules = (
        Rule(
            LinkExtractor(allow=(r"/",), deny=(r"/tag", r"/category", r"/search", r"/blog")),
            callback="parse_item",  follow=True
        ),
    )
        
    def parse_item(self, response):
        hxs = Selector(response)
        i = FarnamgraphItem()
        i["url"] = response.url.strip()
        i["title"] = hxs.xpath("//h1/text()").extract()[0].strip()
        llinks = []

        for anchor in hxs.xpath("//a[@href]"):
            href = anchor.xpath("@href").extract()[0].strip()
            if not href.lower().startswith("javascript"):
                if not any(re.match(regex, href) for regex in self.ignore_urls):
                    llinks.append(urljoin(response.url, href))

        i["links"] = llinks

        return i