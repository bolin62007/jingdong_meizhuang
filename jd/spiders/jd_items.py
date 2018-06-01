# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
import bs4
import re
import demjson
from scrapy.spidermiddlewares.httperror import HttpError

"""

"""

class DianpingSpider(scrapy.Spider):
    name = 'jd_items'

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


    def parse_item_normal(self, response):
        try:
            self.count += 1
            if self.count %10 == 0:
                print(self.count)
            sku_id = re.split('/|\.',response.url)[-2]
            res = [sku_id]
            soup = BeautifulSoup(response.body, 'html.parser')
            category_soup = str(soup.find('div', class_='crumb fl clearfix'))
            category = re.findall('(?<=>)[^><]+(?=</a></div>)', category_soup)
            res += category+['']*(3-len(category))
            name_soup = str(soup.find('div', class_='sku-name'))
            name = re.findall('(?<=>)[^<>]*(?=</div>)',name_soup)
            name = list(map(lambda x:x.strip(),name))
            res += name+['']*(1-len(name))

            if re.findall('alt="京东超市',name_soup):
                shop_name = ['京东超市']
            else:
                shop_name_soup = str(soup.find('div', class_='J-hove-wrap EDropdown fr').contents[:4])
                shop_name = re.findall('(?<=title=")[^"]*(?=")',str(shop_name_soup))[:1]
            res += shop_name+['']*(1-len(shop_name))
            shop_type_soup = str(soup.find('div', class_='name goodshop EDropdown'))
            res.append(['非自营','自营'][int(bool(re.findall('自营',shop_type_soup)))])
            res.append('普通')
            score_soup = str(soup.find('div', class_='m m-aside popbox'))
            score1 = re.findall('(?<=number down">)[^<]*', score_soup)
            res += score1+['']*(1-len(score1))
            score2 = re.findall('(?<=title=")[^"|分]*', score_soup)[2:]
            res += score2+['']*(3-len(score2))
            detail_soup = soup.find('ul', class_='parameter2 p-parameter-list')
            detail = []
            for child in detail_soup.contents:
                if type(child) == bs4.element.Tag:
                    detail+=child.contents
            detail = str(detail)
            res.append(detail)
            brand_soup = soup.find('ul', id='parameter-brand')
            brand = re.findall('(?<=title=")[^"]*(?=")',str(brand_soup))
            res += brand+['']*(1-len(brand))
            for i in range(len(res)):
                res[i] = res[i].replace(';',',')
            with open('/Users/conghua/jd/items','a') as file:
                file.write(';'.join(res)+'\n')

            attrs_soup = soup.find('div', id='choose-attrs')
            skus = re.findall('(?<=data-sku=")[^"]*', str(attrs_soup))
            with open('/Users/conghua/jd/loaded_urls','a') as file:
                file.write(response.meta['url']+'\n')
            for sku in skus:
                url = 'https://item.jd.com/%s.html' % sku
                if url not in self.urls:
                    self.urls.add(url)
                    yield scrapy.Request(url, meta={'url': url},callback=self.parse_item_normal, errback=self.errorback,dont_filter=True)
        except (AttributeError, IndexError) as e:
            with open('/Users/conghua/jd/error', 'a') as file:
                file.write(str(response.meta['url'])+' '+str(type(e))+str(e)+'\n')
            yield scrapy.Request(response.meta['url'], meta={'url': response.meta['url']},
                                 callback=self.parse_item_normal, errback=self.errorback,dont_filter=True)
        except Exception as e:
            with open('/Users/conghua/jd/error', 'a') as file:
                file.write(str(response.meta['url'])+' '+str(e)+'\n')

    def parse_item_global(self, response):
        try:
            self.count += 1
            if self.count % 10 == 0:
                print(self.count)
            sku_id = re.split('/|\.', response.url)[-2]
            res = [sku_id]
            soup = BeautifulSoup(response.body, 'html.parser')
            category_soup = str(soup.find('script'))
            category = demjson.decode(re.findall('(?<=catName: )\[[^\[\]]*\]', category_soup)[0])
            res += category + [''] * (3 - len(category))
            name_soup = str(soup.find('div', class_='sku-name'))
            name = re.findall('(?<=</span>)[^<>]*(?=</div>)', name_soup)
            name = list(map(lambda x: x.strip(), name))
            res += name + [''] * (1 - len(name))
            shop_name_soup = soup.find('div', class_='shopName')
            shop_name = re.findall('(?<=>)[^><]*(?=</)',str(shop_name_soup))[:1]
            res += shop_name + [''] * (1 - len(shop_name))
            shop_type_soup = name_soup
            res.append(['非自营', '自营'][int(bool(re.findall('自营', shop_type_soup)))])
            res.append('全球购')
            score_soup = str(soup.find('div', class_='m m-aside popbox'))
            score1 = ['']
            res += score1
            score2 = re.findall('(?<=title=").*(?=分)', score_soup)
            res += score2 + [''] * (3 - len(score2))
            detail_soup = soup.find('ul', class_='parameter2')
            detail = []
            for child in detail_soup.contents:
                if type(child) == bs4.element.Tag:
                    detail.append(str(child.contents[0]))
            detail = str(detail)
            res.append(detail)
            brand = ''
            res.append(brand)
            for i in range(len(res)):
                res[i] = res[i].replace(';',',')
            with open('/Users/conghua/jd/items','a') as file:
                file.write(';'.join(res)+'\n')

            attrs_soup = soup.find('div', id='choose-attrs')
            skus = re.findall('(?<=data-sku=")[^"]*', str(attrs_soup))
            with open('/Users/conghua/jd/loaded_urls','a') as file:
                file.write(response.meta['url']+'\n')
            for sku in skus:
                url = 'https://item.jd.hk/%s.html' % sku
                if url not in self.urls:
                    self.urls.add(url)
                    yield scrapy.Request(url, meta={'url': url},callback=self.parse_item_normal, errback=self.errorback,dont_filter=True)
        except (AttributeError, IndexError) as e:
            with open('/Users/conghua/jd/error', 'a') as file:
                file.write(str(response.meta['url']) + ' ' + str(type(e)) + str(e) + '\n')
            yield scrapy.Request(response.meta['url'], meta={'url': response.meta['url']},
                                 callback=self.parse_item_normal, errback=self.errorback, dont_filter=True)
        except Exception as e:
            with open('/Users/conghua/jd/error', 'a') as file:
                file.write(str(e))
                file.write('\n'+response.meta['url']+'\n')

    def errorback(self,failure):
        with open('/Users/conghua/jd/error', 'a') as file:
            if failure.check(HttpError):
                response = failure.value.response
                file.write(str(failure.value.response)+'\n')
                file.write(str(response.url))
                file.write('\n')

