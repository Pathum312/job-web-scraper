from ..items import JobsItem
from typing import Any, Generator
from scrapy.loader import ItemLoader # type: ignore
from scrapy.spiders import Rule, CrawlSpider # type: ignore
from scrapy.linkextractors import LinkExtractor # type: ignore
from scrapy.http.response.html import HtmlResponse # type: ignore

class JobCrawlerSpider(CrawlSpider):
    name: str = "jobscrawler"
    allowed_domains: list[str] = ["books.toscrape.com"]
    start_urls: list[str] = ["https://books.toscrape.com/"]
    
    rules: tuple[Rule, Rule] = ( # type: ignore
        Rule(link_extractor=LinkExtractor(allow=(r'catalogue/category'))),
        Rule(link_extractor=LinkExtractor(allow=(r'catalogue'), deny=(r'category')), callback='parse_item')
    )
    
    def parse_item(self, response: HtmlResponse) -> Generator[dict[str, str | None], Any, None]:
        l: ItemLoader = ItemLoader(item=JobsItem(), response=response)
        
        l.add_css(field_name='upc', css='tr:first-child td')
        l.add_css(field_name='title', css='h1')
        l.add_css(field_name='category', css='li:nth-child(3) a')
        l.add_css(field_name='price', css='p.price_color')
        l.add_css(field_name='tax', css='tr:nth-child(5) td')
        l.add_css(field_name='stock', css='p.availability')
        l.add_css(field_name='description', css='.product_page > p:nth-child(3)')
        
        return l.load_item()