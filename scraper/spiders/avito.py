import json
import re

import scrapy

from scraper import settings


RE_ID_DETAILS = re.compile('(\d+)$')


def get_id_from_details_url(url: str) -> int:
    matches = re.findall(RE_ID_DETAILS, url)
    return int(matches[0])


class AvitoItem(scrapy.Item):

    id = scrapy.Field()
    title = scrapy.Field()
    phone_raw = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()


class AvitoMobileSpider(scrapy.Spider):

    name = 'avito'

    start_urls = [
        'https://m.avito.ru/moscow'
    ]

    custom_settings = {
        'CONCURRENT_REQUESTS_PER_DOMAIN': 2,
        'IMAGES_URLS_FIELD': 'image_urls',
    }

    max_pages = settings.MAX_PAGES

    handled = 0

    def parse(self, response: scrapy.http.HtmlResponse):

        self.max_pages -= 1

        if self.max_pages == 0:
            self.logger.info('handled=%s', self.handled)
            return

        self.handled += 1

        for url in response.css('.item-link::attr(href)').extract():

            item = AvitoItem()

            item_id = get_id_from_details_url(url)

            item['id'] = item_id

            yield scrapy.Request(response.urljoin(url), callback=lambda r: self.parse_details(r, item))

        next_url = response.css('.page-next a::attr(href)').extract_first()

        if next_url:
            yield scrapy.Request(response.urljoin(next_url), callback=self.parse)

    def parse_details(self, response: scrapy.http.HtmlResponse, item: scrapy.Item):

        image_urls = []

        for img_url in response.css('meta[property="og:image"]::attr(content)').extract():
            self.logger.info('img=%s', img_url)

            image_urls.append(img_url)

        item['image_urls'] = image_urls

        header_title = response.css('article header::text').extract_first()

        if header_title:
            header_title = header_title.strip()

        item['title'] = header_title

        phone_url = response.css('.js-action-show-number::attr(href)').extract_first()

        self.logger.info('phone_url=%s', phone_url)

        if phone_url:
            phone_url += '?async'

        yield scrapy.Request(response.urljoin(phone_url), callback=lambda r: self.parse_phone(r, item))

    def parse_phone(self, response: scrapy.http.HtmlResponse, item: scrapy.Item):

        body = json.loads(response.body.decode())

        item['phone_raw'] = body.get('phone')

        yield item

