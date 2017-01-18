from scrapy.crawler import CrawlerProcess

from scraper.spiders.avito import AvitoMobileSpider
from scraper import settings

process = CrawlerProcess(vars(settings))
process.crawl(AvitoMobileSpider)
process.start()
