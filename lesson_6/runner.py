from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from hh_parser import settings
from hh_parser.spiders.hhru import HhruSpider
from hh_parser.spiders.sjobru import SJobruSpider

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(HhruSpider)
    process.crawl(SJobruSpider)

    process.start()