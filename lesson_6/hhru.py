import scrapy
from scrapy.http import HtmlResponse
from hh_parser.items import HhParserItem

class HhruSpider(scrapy.Spider):
    name = 'hhru'
    allowed_domains = ['hh.ru']
    start_urls = ['https://hh.ru/search/vacancy?area=1&fromSearchLine=true&text=Python+developer&from=suggest_post',
                  'https://hh.ru/search/vacancy?clusters=true&area=2&ored_clusters=true&enable_snippets=true&salary=&text=Python']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath('//a[@data-qa="pager-next"]/@href').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)


        links = response.xpath('//a[@data-qa="vacancy-serp__vacancy-title"]/@href ').getall()
        for link in links:
            yield response.follow(link, callback=self.vacancy_parse)

    def vacancy_parse(self, responce: HtmlResponse):
        name = responce.xpath("//h1//text()").get()
        salary = responce.xpath("//div[contains(@class, 'vacancy-salary')]//text()").getall()
        url = responce.url
        yield HhParserItem(name=name, salary=salary, url=url)
