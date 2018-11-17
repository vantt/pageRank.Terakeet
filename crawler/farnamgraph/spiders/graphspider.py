from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.utils.url import urljoin_rfc
from farnamgraph.items import FarnamgraphItem

#https://fs.blog/best-articles/
#https://fs.blog/mental-models/
#https://fs.blog/popular/
#https://fs.blog/prime/
#https://fs.blog/privacy-policy/
#https://fs.blog/random-articles/
#https://fs.blog/blog
#https://fs.blog/reading/
#https://fs.blog/smart-decisions/
#https://fs.blog/principles/
#https://fs.blog/newsletter
#https://fs.blog/principles
#https://fs.blog/podcast
#https://fs.blog/membership

class GraphspiderSpider(CrawlSpider):
    name = 'graphspider'
    allowed_domains = ['fs.blog']
    start_urls = ['https://fs.blog/blog']

    rules = (
        Rule(SgmlLinkExtractor(allow=(r'/',), deny=(r'/tag',r'/category',r'/search',r'/blog')), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        hxs = HtmlXPathSelector(response)
        i = FarnamgraphItem()
        i['url'] = response.url.strip()
        i['title'] = hxs.select('//h1/text()').extract()[0].strip()
        llinks=[]
        for anchor in hxs.select('//a[@href]'):
            href=anchor.select('@href').extract()[0].strip()
            if not href.lower().startswith("javascript"):
                llinks.append(urljoin_rfc(response.url,href))
        i['links'] = llinks
        return i
