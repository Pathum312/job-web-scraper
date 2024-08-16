from scrapy import Item, Field # type: ignore
from w3lib.html import remove_tags
from itemloaders.processors import MapCompose, TakeFirst

class JobsItem(Item):
    upc: Field = Field(
        input_processor=MapCompose(remove_tags),
        output_processor=TakeFirst()
    )
    title: Field = Field(
        input_processor=MapCompose(remove_tags),
        output_processor=TakeFirst()
    )
    category: Field = Field(
        input_processor=MapCompose(remove_tags),
        output_processor=TakeFirst()
    )
    price: Field = Field(
        input_processor=MapCompose(remove_tags),
        output_processor=TakeFirst()
    )
    tax: Field = Field(
        input_processor=MapCompose(remove_tags),
        output_processor=TakeFirst()
    )
    stock: Field = Field(
        input_processor=MapCompose(remove_tags),
        output_processor=TakeFirst()
    )
    description: Field = Field(
        input_processor=MapCompose(remove_tags),
        output_processor=TakeFirst()
    )
