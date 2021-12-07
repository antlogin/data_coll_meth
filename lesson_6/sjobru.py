import scrapy
from scrapy.http import HtmlResponse
from hh_parser.items import SJobParserItem

class SJobruSpider(scrapy.Spider):
    name = 'sjobru'
    allowed_domains = ['superjob.ru']
    start_urls = ['https://russia.superjob.ru/vacancy/search/?keywords=Python']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath('//a[@rel="next"][2]/@href').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        links = response.xpath('//div[@class="f-test-search-result-item"]/div/div/div/div/div[3]/div/div[1]//a/@href').getall()
        for link in links:
            yield response.follow(link, callback=self.vacancy_parse)

    def vacancy_parse(self, responce: HtmlResponse):
        name = responce.xpath("//h1//text()").getall()
        salary = responce.xpath("//span[@class='_2Wp8I _1e6dO _1XzYb _3Jn4o']//text()").getall()
        url = responce.url
        yield SJobParserItem(name=name, salary=salary, url=url)
