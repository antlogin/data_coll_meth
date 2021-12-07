import scrapy
from scrapy.http import HtmlResponse
from lm_project.items import LmProjectItem
from scrapy.loader import ItemLoader


class LmSpiderSpider(scrapy.Spider):
    name = 'lm_spider'
    allowed_domains = ['leroymerlin.ru']

    def __init__(self, query):
        super().__init__()
        self.start_urls = [f'https://leroymerlin.ru/search/?q={query}']

    def parse(self, response):
        links = response.xpath('//a[@data-qa="product-name"]')
        for link in links:
            yield response.follow(link, callback=self.parse_ads)

    def parse_ads(self, response: HtmlResponse):
        loader = ItemLoader(item=LmProjectItem(), response=response)

        loader.add_xpath('name', "//h1/text()")
        loader.add_xpath('price', "//span[@slot='price']/text()")
        loader.add_xpath('photos', "//img[@slot='thumbs']/@src")
        loader.add_value('url', response.url)
        yield loader.load_item()


