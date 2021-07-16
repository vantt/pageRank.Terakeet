
import re
import zlib
from pprint import pprint
from urllib.parse import urlparse
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import logging


try:
    from urllib.parse import urljoin
except ImportError:
    from urlparse import urljoin

from blog_graph.items import BlogGraphItem


class BlogSpider(CrawlSpider):
    name = "blog"

    allowed_domains = ["terakeet.com"]
    start_urls = ["https://terakeet.com/seo-blog/"]
    keep_urls = [
        r"^https:\/\/terakeet\.com\/blog\/.*$",
        r"^https:\/\/terakeet\.com\/seo-blog\/.*$",
        r"^https:\/\/terakeet\.com\/seo-knowledge-hub\/.*$",
    ]

    ignore_urls = [
        # r"^https:\/\/cottonbureau\.com\/products\/listen-and-learn-crewneck-tee.*",
        # r"^https:\/\/pressable\.com.*",
        # r"^https:\/\/rethinkworkshops\.com.*",
        # r"^https:\/\/syruspartners\.com.*",
        # r"^https:\/\/twitter\.com\/farnamstreet.*",
        # r"^https:\/\/www\.facebook\.com\/FarnamStreet.*",
        # r"^https:\/\/www\.instagram\.com\/farnamstreet.*",
        # r"^https:\/\/www\.youtube\.com\/user\/farnamstreetblog.*",
        # r"^https:\/\/www\.farnamstreetblog\.com\/Royce17Logo.*",
        # r"^https:\/\/\itunes.apple.com\/$",
    ]

    rules = (
        Rule(
            LinkExtractor(
                allow=(r"/",),
                deny=(
                    r"/client-success/",
                    r"/enterprise-seo-solutions/",
                    r"/search",
                )
            ),
            callback="parse_item", follow=True
        ),
    )

    def parse_item(self, response):
        hxs = Selector(response)
        page_url = response.url.strip()

        if self.is_keep_url(page_url):
            item = BlogGraphItem()

            item["url"] = page_url
            item["id"] = zlib.crc32(bytes(page_url, 'utf-8')) & 0xffffffff
            item["title"] = hxs.xpath("//title/text()").extract()[0].strip()
            links = {}

            for anchor in hxs.xpath("//a"):
                label = anchor.xpath("text()").extract();
                label = next((item for item in label if item is not None), 'none').lower()

                #pprint(label)

                href = anchor.xpath("@href").extract()[0].strip()
                if not href.lower().startswith("javascript"):
                    if self.is_keep_url(href):
                        link_url = urljoin(page_url, href)
                        link_id = zlib.crc32(bytes(link_url, 'utf-8')) & 0xffffffff
                        links[link_id] = [link_url, label]

            item["links"] = links

            return item

        return None

    def is_keep_url(self, page_url):
        #page_path = urlparse(page_url).path.strip()
        is_keep = any(re.search(regex, page_url) for regex in self.keep_urls)

        # pprint(self.keep_paths)
        # pprint(page_url)
        # pprint(page_path)
        # pprint(is_keep)
        if is_keep:
            logging.log(logging.ERROR, "Keep: " + page_url)
        else:
            logging.log(logging.ERROR, "Skip: " + page_url)

        return is_keep

        #
        # if not is_keep:
        #     is_keep = not any(re.search(regex, url) for regex in self.ignore_urls)




