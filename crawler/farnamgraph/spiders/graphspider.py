from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.utils.url import urljoin_rfc
from farnamgraph.items import FarnamgraphItem

class GraphspiderSpider(CrawlSpider):
    name = 'graphspider'
    allowed_domains = ['fs.blog']
    start_urls = ['https://fs.blog/blog']

    rules = (
        Rule(SgmlLinkExtractor(allow=(r'/',), deny=(r'/tag',)), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        hxs = HtmlXPathSelector(response)
        i = FarnamgraphItem()
        i['url'] = response.url        
        i['title'] = hxs.select('//h1/text()').extract()[0]
        llinks=[]
        for anchor in hxs.select('//a[@href]'):
            href=anchor.select('@href').extract()[0]
            if not href.lower().startswith("javascript"):
                llinks.append(urljoin_rfc(response.url,href))
        i['linkedurls'] = llinks
        return i