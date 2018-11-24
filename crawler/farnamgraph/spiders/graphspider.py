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

    name = 'graphspider'

    allowed_domains = ['fs.blog']
    start_urls = ['https://fs.blog/blog']
    ignore_urls = [
        r'/best-articles',
        r'/mental-models',
        r'/popular',
        r'/prime',
        r'/privacy-policy',
        r'/random-articles',
        r'/blog',
        r'/reading',
        r'/smart-decisions',
        r'/principles',
        r'/newsletter',
        r'/principles',
        r'/podcast',
        r'/membership',
    ]

    rules = (
        Rule(
            LinkExtractor(allow=(r'/',), deny=(r'/tag', r'/category', r'/search', r'/blog')),
            callback='parse_item',  follow=True
        ),
    )
        
    def parse_item(self, response):
        hxs = Selector(response)
        i = FarnamgraphItem()
        i['url'] = response.url.strip()
        i['title'] = hxs.xpath('//h1/text()').extract()[0].strip()
        llinks = []

        for anchor in hxs.xpath('//a[@href]'):
            href = anchor.xpath('@href').extract()[0].strip()
            if not href.lower().startswith("javascript"):
                if not any(re.match(regex, href) for regex in self.ignore_urls):
                    llinks.append(urljoin(response.url, href))

        i['links'] = llinks

        return i