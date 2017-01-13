import json

import scrapy


class AvitoItem(scrapy.Item):

    id = scrapy.Field()
    title = scrapy.Field()
    images = scrapy.Field()


class AvitoMobileSpider(scrapy.Spider):

    name = 'avito'

    start_urls = [
        'https://m.avito.ru/perm'
    ]

    custom_settings = {
        'DOWNLOAD_DELAY': 1,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 2,
    }

    pages = 0

    def parse(self, response: scrapy.http.HtmlResponse):

        self.pages += 1

        if self.pages == 2:
            return

        for url in response.css('.item-link::attr(href)').extract():

            item = AvitoItem()

            yield scrapy.Request(response.urljoin(url), callback=lambda r: self.parse_details(r, item))

            break

        # next_url = response.css('.page-next a::attr(href)').extract_first()
        #
        # if next_url:
        #     yield scrapy.Request(response.urljoin(next_url), callback=self.parse)

    def parse_details(self, response: scrapy.http.HtmlResponse, item: scrapy.Item):

        image_urls = []

        for img_url in response.css('meta[property="og:image"]::attr(content)').extract():
            self.logger.info('img=%s', img_url)

        # header_title = response.css('article header::text').extract_first()
        #
        # if header_title:
        #     header_title = header_title.strip()
        #
        # self.logger.info('phone_url=%s', phone_url)
        #
        # yield {
        #     'header_title': header_title
        # }

        phone_url = response.css('.js-action-show-number::attr(href)').extract_first()

        self.logger.info('phone_url=%s', phone_url)

        if phone_url:
            phone_url += '?async'

        yield scrapy.Request(response.urljoin(phone_url), callback=self.parse_phone)

        # self.logger.info('parse details %s', response.url)

    def parse_phone(self, response: scrapy.http.HtmlResponse):

        body = json.loads(response.body.decode())

        self.logger.info('phone=%s', body.get('phone'))



