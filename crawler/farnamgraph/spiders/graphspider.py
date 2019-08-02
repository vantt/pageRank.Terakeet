import sys
import os
import re
import zlib
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
    keep_urls = [
        r"\/\d{4}\/\d{2}\/[^\/]+\/$"
    ]

    ignore_urls = [
        r"\#$",
        r"\/$",
        r"\/about.*",
        r"\/best-articles.*",
        r"\/blog.*",
        r"\/category.*",
        r"\/tags.*",
        r"\/tag.*",
        r"\/feed.*",
        r"\/membership.*",
        r"\/mental-models.*",
        r"\/newsletter.*",
        r"\/podcast.*",
        r"\/popular.*",
        r"\/prime.*",
        r"\/principles.*",
        r"\/privacy-policy.*",
        r"\/random-articles.*",
        r"\/reading.*",
        r"\/search.*",
        r"\/smart-decisions.*",
        r"\/speaking.*",
        r"\/sponsorship.*",
        r"\/reading\/$",
        r"\/the-knowledge-project\/$",
        r"smart-decisions.*",
        r"^https:\/\/cottonbureau\.com\/products\/listen-and-learn-crewneck-tee.*",
        r"^https:\/\/pressable\.com.*",
        r"^https:\/\/rethinkworkshops\.com.*",
        r"^https:\/\/syruspartners\.com.*",
        r"^https:\/\/twitter\.com\/farnamstreet.*",
        r"^https:\/\/www\.facebook\.com\/FarnamStreet.*",
        r"^https:\/\/www\.instagram\.com\/farnamstreet.*",
        r"^https:\/\/www\.youtube\.com\/user\/farnamstreetblog.*",
        r"^https:\/\/www\.farnamstreetblog\.com\/Royce17Logo.*",
        r"^https:\/\/\itunes.apple.com\/$",
    ]

    rules = (
        Rule(
            LinkExtractor(
                allow=(r"/",),
                deny=(
                    r"/tag",
                    r"/category",
                    r"/search",
                    r"/blog"
                )
            ),
            callback="parse_item", follow=True
        ),
    )

    def parse_item(self, response):
        hxs = Selector(response)
        page_url = response.url.strip()

        if self.is_keep_url(page_url):
            item = FarnamgraphItem()

            item["url"] = page_url
            item["id"] = zlib.crc32(bytes(page_url, 'utf-8')) & 0xffffffff
            item["title"] = hxs.xpath("//title/text()").extract()[0].strip()
            links = {}

            for anchor in hxs.xpath("//a[@href]"):
                href = anchor.xpath("@href").extract()[0].strip()
                if not href.lower().startswith("javascript"):
                    if self.is_keep_url(href):
                        link_url = urljoin(page_url, href)
                        link_id = zlib.crc32(bytes(link_url, 'utf-8')) & 0xffffffff
                        links[link_id] = link_url

            item["links"] = links

            return item

        return None

    def is_keep_url(self, url):
        return any(re.search(regex, url) for regex in self.keep_urls)
        #
        # if not is_keep:
        #     is_keep = not any(re.search(regex, url) for regex in self.ignore_urls)




