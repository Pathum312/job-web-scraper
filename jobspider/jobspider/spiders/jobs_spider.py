from typing import Any, Generator, List
from scrapy import Spider # type: ignore
from scrapy.http.response.html import HtmlResponse # type: ignore

class JobsSpider(Spider):
    name: str = 'jobs'
    
    start_urls: list[str] = [
        "https://quotes.toscrape.com/page/1/",
        "https://quotes.toscrape.com/page/2/",
    ]
    
    def parse(self, response: HtmlResponse) -> Generator[dict[str, str | List[str] | None], Any, None]: # type: ignore
        for quote in response.css(query='div.quote'): # type: ignore
            yield {
                "text": quote.css(query="span.text::text").get(),
                "author": quote.css(query="small.author::text").get(),
                "tags": quote.css(query="div.tags a.tag::text").getall(),
            }
        
    