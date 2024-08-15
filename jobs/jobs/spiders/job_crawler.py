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
        """
            title - /html/body/div/div/div[2]/div[2]/article/div[1]/div[2]/h1
            price - /html/body/div/div/div[2]/div[2]/article/div[1]/div[2]/p[1]
            stock - /html/body/div/div/div[2]/div[2]/article/div[1]/div[2]/p[2]
            description - /html/body/div/div/div[2]/div[2]/article/p
        """
        yield {
            "title": response.xpath(query='/html/body/div/div/div[2]/div[2]/article/div[1]/div[2]/h1/text()').get(), # type: ignore
            "price": response.xpath(query='/html/body/div/div/div[2]/div[2]/article/div[1]/div[2]/p[1]/text()').get(), # type: ignore
            "stock": response.xpath(query='/html/body/div/div/div[2]/div[2]/article/div[1]/div[2]/p[2]/text()').getall()[1] # type: ignore
            .replace('\n', '')
            .replace(' ', '')
            .replace('Instock(', '')
            .replace('available)', ''),
            "description": response.xpath(query='/html/body/div/div/div[2]/div[2]/article/p/text()').get(), # type: ignore
        }