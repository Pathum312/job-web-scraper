from scrapy import Item, Field # type: ignore

class JobsItem(Item):
    title: Field = Field()
    price: Field = Field()
    stock: Field = Field()
    rating: Field = Field()
    description: Field = Field()
