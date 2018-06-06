# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
import bs4
import re
import demjson
from scrapy.spidermiddlewares.httperror import HttpError

"""
jd_comment 里获取了comment和price
"""

class DianpingSpider(scrapy.Spider):
    name = 'jd_comment'

    def __init__(self):
        self.count = 0
        self.price_file = open('/Users/conghua/jd/items_price', 'a')
        self.comment_file = open('/Users/conghua/jd/items_comment', 'a')
        self.skus = []
        with open('/Users/conghua/jd/loaded_urls', 'r') as file:
            for line in file:
                self.skus.append(re.split('/|\.', line.strip())[-2])

    def start_requests(self):
        self.comment_file.write('sku;commentCount;goodCount;generalCount;poorCount;afterCount;hotcomments'+'\n')
        self.price_file.write('sku;originalprice;price' + '\n')
        sku_lst = []
        for sku in self.skus:
            sku_lst.append(sku)
            if len(sku_lst) == 99:
                s = 'J_'
                s += '%2CJ_'.join(sku_lst)
                url = "https://p.3.cn/prices/mgets?type=1&pdtk=&pdpin=&pin=null&pdbp=0&skuIds="+s+"&ext=11100000&source=item-pc"
                yield scrapy.Request(url, meta={'sku': sku_lst}, callback=self.parse_price, errback=self.errorback,
                                     dont_filter=True)
                sku_lst = []
            url = "https://club.jd.com/comment/skuProductPageComments.action?productId=%s&score=0&sortType=5" \
                  "&page=0&pageSize=10&isShadowSku=0&fold=1"%sku
            yield scrapy.Request(url, meta={'sku': sku, 'url': url},callback=self.parse_comment, errback=self.errorback, dont_filter=True)
        if sku_lst:
            s = 'J_'
            s += '%2CJ_'.join(sku_lst)
            url = "https://p.3.cn/prices/mgets?type=1&pdtk=&pdpin=&pin=null&pdbp=0&skuIds=" + s + "&ext=11100000&source=item-pc"
            yield scrapy.Request(url, meta={'sku': sku_lst, 'url': url}, callback=self.parse_price, errback=self.errorback,
                                 dont_filter=True)

    def parse_price(self, response):
        try:
            body = response.body.decode('gbk')
            op = re.findall('(?<="op":")[^"]*(?=")', body)
            p = re.findall('(?<="p":")[^"]*(?=")', body)
            id = re.findall('(?<="id":"J_)[^"]*(?=")', body)
            if len(op) != len(p) != len(id):
                raise IndexError("op,p,ids长度不一")
            if len(op) == 0:
                raise IndexError("返回为空")
            res = list(zip(id,op,p))
            for price in res:
                self.price_file.write(';'.join(price)+'\n')
        except Exception as e:
            with open('/Users/conghua/jd/error_1', 'a') as file:
                file.write(str(response.meta['url'])+' '+str(e)+'\n')


    def parse_comment(self, response):
        try:
            body = response.body.decode('gbk')
            res = []
            res.append(response.meta['sku'])
            commentCount = re.search('(?<="commentCount":)[^,]*', body).group()
            res.append(commentCount)
            goodCount = re.search('(?<="goodCount":)[^,]*', body).group()
            res.append(goodCount)
            generalCount = re.search('(?<="generalCount":)[^,]*', body).group()
            res.append(generalCount)
            poorCount = re.search('(?<="poorCount":)[^,]*', body).group()
            res.append(poorCount)
            afterCount = re.search('(?<="afterCount":)[^,]*', body).group()
            res.append(afterCount)

            hot = []
            hotcomments = re.findall('"id":"[^"]*","name":"[^"]*","rid":"[^"]*","count":[^"]*(?=,)', body)
            if not hotcomments:
                hotcomments = re.findall('"id":"[^"]*","name":"[^"]*","status":[^"]*,"rid":"[^"]*","productId":[^"]*,"count":[^"]*(?=,)', body)

            for comment in hotcomments:
                comment = re.split('","|":"|":',comment)
                name = comment[3]
                count = comment[-1]
                hot.append(name)
                hot.append(count)
            res += hot
            res = list(map(lambda x:str(x).replace(';',','),res))
            res = ';'.join(res)
            self.comment_file.write(res+'\n')
        except Exception as e:
            with open('/Users/conghua/jd/error_1', 'a') as file:
                file.write(str(response.meta['url'])+' '+str(e)+'\n')




    def errorback(self, failure):
        with open('/Users/conghua/jd/error_1', 'a') as file:
            if failure.check(HttpError):
                response = failure.value.response
                file.write(str(response.url) + response.status)
