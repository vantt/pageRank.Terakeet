import re
import libcrc
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from urllib.parse import urljoin
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
            SgmlLinkExtractor(allow=(r'/',), deny=(r'/tag', r'/category', r'/search', r'/blog')),
            callback='parse_item',  follow=True
        ),
    )

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
