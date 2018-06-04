# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
from scrapy.spidermiddlewares.httperror import HttpError
import re

"""
jd_urls.py 用来从list页面获取所有item页的url，并写入txt
init_urls里存的是美妆/个护下共9个二级类的list页url

"""

class DianpingSpider(scrapy.Spider):
    name = 'jd_urls'

    def __init__(self):
        self.count1 = 0
        self.count2 = 0
        pass

    def start_requests(self):
        init_urls = ['https://list.jd.com/list.html?cat=1316,16831',
                        'https://list.jd.com/list.html?cat=1316,16832',
                        'https://list.jd.com/list.html?cat=1316,1381',
                        'https://list.jd.com/list.html?cat=1316,1387',
                        'https://list.jd.com/list.html?cat=16750,16751',
                        'https://list.jd.com/list.html?cat=16750,16752',
                        'https://list.jd.com/list.html?cat=16750,16753',
                        'https://list.jd.com/list.html?cat=16750,16754',
                        'https://list.jd.com/list.html?cat=16750,16755',
                    ]
        for url in init_urls:
            yield scrapy.Request(url, callback=self.parse_list, errback=self.errorback)

    def parse_list(self, response):
        soup = BeautifulSoup(response.body, 'lxml')
        if len(response.url)<50:            # 如果是init_url
            max_page = soup.find('span', class_='p-skip').find('b').contents[0]
            for page in range(1,int(max_page)+1):
                url = response.url + '&page=%i&sort=sort_tota' \
                      'lsales15_desc&trans=1&JL=6_0_0#J_main'%page
                yield scrapy.Request(url, callback=self.parse_list, errback=self.errorback)
        else:                       # 如果是init_url的翻页后页面，提取改页面所有item的url，
            items_div = soup.find_all('div', class_='gl-i-wrap j-sku-item')
            for div_tag in items_div:
                div_tag = str(div_tag)
                sku_id = re.search('data-sku="[^"]*',div_tag).group()[10:]
                print(self.count1, ', ', self.count2,', ')
                if re.search('>全球购</span>',div_tag):    # url分全球购和普通页面两种，域名不一样
                    self.count1 += 1
                    url = 'https://item.jd.hk/%s.html' % sku_id
                else:
                    self.count2 += 1
                    url = 'https://item.jd.com/%s.html' % sku_id
                with open('/Users/conghua/jd/item_urls', 'a') as file:
                    file.write(url)
                    file.write('\n')



    def errorback(self,failure):
        with open('/Users/conghua/jd/error', 'a') as file:
            if failure.check(HttpError):
                response = failure.value.response
                self.logger.error('HttpError on %s', response.url)
                file.write(str(failure.value.response)+'\n')
                file.write(str(response.url))
                file.write('\n')

