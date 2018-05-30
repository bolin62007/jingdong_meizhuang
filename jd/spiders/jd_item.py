# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
from scrapy.spidermiddlewares.httperror import HttpError
import re

"""

"""

class DianpingSpider(scrapy.Spider):
    name = 'jd_items'

    def __init__(self):
        self.count1 = 0
        self.count2 = 0
        pass

    def start_requests(self):
        with open('/Users/conghua/jd/item_urls', 'r') as file:
            urls = list(map(lambda x: x.strip(),file.readlines()))
        for url in urls:
            if 'com' in url:
                pass
                yield scrapy.Request(url, callback=self.parse_item_normal, errback=self.errorback)
            else:
                pass
                # yield scrapy.Request(url, callback=self.parse_item_global, errback=self.errorback)


    def parse_item_normal(self, response):
        print('normal',response.url)
        pass


    def parse_item_global(self, response):
        # print('global',response.url)
        pass


    def errorback(self,failure):
        with open('/Users/conghua/jd/error', 'a') as file:
            if failure.check(HttpError):
                response = failure.value.response
                self.logger.error('HttpError on %s', response.url)
                file.write(str(failure.value.response)+'\n')
                file.write(str(response.url))
                file.write('\n')

