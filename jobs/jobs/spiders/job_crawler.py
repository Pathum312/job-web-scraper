from typing import Any, Generator
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
        yield {
            "upc": response.css(query='td::text').getall()[0], # type: ignore
            "title": response.css(query='h1::text').get(), # type: ignore
            "type": response.css(query='a::text').getall()[3], # type: ignore
            "price": response.css(query='p.price_color::text').get().replace('£', ''), # type: ignore
            "tax": response.css(query='td::text').getall()[4].replace('£', ''), # type: ignore
            "stock": response.css(query='p.availability::text').getall()[1] # type: ignore
            .replace('\n', '')
            .replace(' ', '')
            .replace('Instock(', '')
            .replace('available)', ''),
            "description": response.css(query='p::text').getall()[10], # type: ignore
        }