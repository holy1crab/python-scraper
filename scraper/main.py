from scrapy.crawler import CrawlerProcess

from scraper.spiders.avito import AvitoMobileSpider

process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})

process.crawl(AvitoMobileSpider)
process.start()
