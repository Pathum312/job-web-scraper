from io import TextIOWrapper
import json
from typing import Sequence
from scrapy.spiders import CrawlSpider, Rule # type: ignore
from scrapy.linkextractors import LinkExtractor # type: ignore

class CrawlingSpider(CrawlSpider):
    name: str = 'mycrawler'
    allowed_domains: list[str] = ['toscrape.com']
    start_urls: list[str] = ['http://books.toscrape.com/']
    
    PROXY_SERVER = '38.188.249.5:8080'
    
    rules: Sequence[Rule] = (
        Rule(link_extractor=LinkExtractor(allow='catalogue/category')),
    )
