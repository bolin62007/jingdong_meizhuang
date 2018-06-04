# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
import bs4
import re
import demjson
from scrapy.spidermiddlewares.httperror import HttpError

"""
jd_price 里获取了price和comment
"""

class DianpingSpider(scrapy.Spider):
    name = 'jd_price'

    def __init__(self):
        self.count = 0
        with open('/Users/conghua/jd/items','a') as file:
            file.write('sku;category1;category2;category3;name;shopname;shoptype1;shoptype2;score1;score2;score3;score4;detail;brand' + '\n')
        with open('/Users/conghua/jd/item_urls', 'r') as file:
            self.urls = set(list(map(lambda x: x.strip(),file.readlines())))

    def start_requests(self):
        urls = list(self.urls)
        for url in urls:
            if 'com' in url:
                yield scrapy.Request(url, meta={'url': url}, callback=self.parse_item_normal, errback=self.errorback,dont_filter=True)
            else:
                yield scrapy.Request(url, meta={'url':url}, callback=self.parse_item_global, errback=self.errorback,dont_filter=True)



    def errorback(self,failure):
        with open('/Users/conghua/jd/error', 'a') as file:
            if failure.check(HttpError):
                response = failure.value.response
                file.write(str(failure.value.response)+'\n')
                file.write(str(response.url))
                file.write('\n')

