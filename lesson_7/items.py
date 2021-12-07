# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
from platform import processor
import scrapy
from itemloaders.processors import TakeFirst, MapCompose

def process_photos_url(value):
    try:
        value = str(value).replace(',w_82,h_82', '')
    except Exception as e:
        print(e)
    finally:
        return value


def process_price(value):
    try:
        value = value.replace(' ', '')
        value = int(value)
    except Exception as e:
        print(e)
    finally:
        return value

class LmProjectItem(scrapy.Item):
    # define the fields for your item here like:
    _id = scrapy.Field()
    name = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(output_processor=TakeFirst(), input_processor=MapCompose(process_price))
    url = scrapy.Field(output_processor=TakeFirst())
    photos = scrapy.Field(input_processor=MapCompose(process_photos_url))
    # name = scrapy.Field(output_processor=TakeFirst())
    # price = scrapy.Field(output_processor=TakeFirst(), input_processor=MapCompose(process_price))
    # url = scrapy.Field(output_processor=TakeFirst())
    # photos = scrapy.Field()
