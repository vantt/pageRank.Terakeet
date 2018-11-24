import sys
import os 
import re
import binascii
from scrapy.selector import HtmlXPathSelector
from scrapy.linkextractors import LinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule

try:
    from urllib.parse import urljoin
except ImportError:
     from urlparse import urljoin

from farnamgraph.items import FarnamgraphItem


class GraphspiderSpider(CrawlSpider):

    name = 'graphspider'

    customs_settings = {
        'FEED_URI' : 'file://%(storage_path)s/.json'
    }

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

     def __init__(self, category=None, *args, **kwargs):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        self.category = dir_path        
        print(dir_path)
        print(os.getcwd())
        quit()

        super(GraphspiderSpider, self).__init__(*args, **kwargs)
        
    def parse_item(self, response):
        hxs = HtmlXPathSelector(response)
        i = FarnamgraphItem()
        i['url'] = response.url.strip()
        i['title'] = hxs.select('//h1/text()').extract()[0].strip()
        llinks = []

        for anchor in hxs.select('//a[@href]'):
            href = anchor.select('@href').extract()[0].strip()
            if not href.lower().startswith("javascript"):
                if not any(regex.match(href) for regex in self.ignore_urls):
                    llinks.append(urljoin(response.url, href))

        i['links'] = llinks

        return i