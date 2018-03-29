from scrapy import Spider, Request
from scrapy.http import FormRequest

from firmware.items import FirmwareImage
from firmware.loader import FirmwareLoader

import urlparse
import json
import logging

class NetgearSpider(Spider):
    name = "netgear"
    allowed_domains = ["netgear.com"]
    start_urls = ["http://netgear.com/system/supportModels.json"]

    def parse(self, response):
        products = json.loads(response.body)

        unsupported = 0
        for product in products[:]:
            if not ("/support/product/" in product['url'] and "aspx" in product['url']):
                logging.warning('Unprocessible product URL: ' + product['url'])
                unsupported += 1
            else:
                yield Request(url="http://netgear.com" + product['url'], callback=self.parse_product)
        logging.warning("Total number of unprocessible products: %d" % unsupported)

    outer_count_map = {}
    extension_map = {}

    def parse_product(self, response):
        results = []

        outers = response.css('#topicsdownload:not(.hidea)')
        outer_count = len(outers)
        if outer_count not in self.outer_count_map:
            self.outer_count_map[outer_count] = 0
        self.outer_count_map[outer_count] += 1

        if outer_count == 0:
            logging.warning('Cannot find download section on URL: ' + response.request.url)
            return
        elif outer_count > 0:
            logging.warning('Duplicate download sections present on URL: ' + response.request.url + '. Picking the first.')

        outer = outers[0]
        items = outer.css('.accordion-item')

        if len(items) == 0:
            logging.warning('No download items found on URL: ' + response.request.url)
            return

        for item in items:
            name = item.css('.accordion-title h1')[0].xpath("text()").extract()[0].encode('utf-8')
            link = item.css('.accordion-content a')[0].xpath("@href").extract()[0]

            if not ("Firmware" in name or "firmware" in name):
                logging.warning('Skipping non-firmware download: ' + name)
                continue

            result = FirmwareImage()
            result['product'] = response.css('.model .product-code').xpath("text()").extract()[0].strip()
            result['vendor'] = 'Netgear'

            result['description'] = name
            result['url'] = link

            results.append(result)

        return results
