from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from lm_project.spiders.lm_spider import LmSpiderSpider
from lm_project import settings

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings=crawler_settings)
    query = 'газонокосилка'
    process.crawl(LmSpiderSpider, query=query)
    process.start()
