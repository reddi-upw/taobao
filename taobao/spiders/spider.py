from urllib.parse import urlencode, urlsplit, urlunsplit, parse_qsl

import scrapy
import scrapy_splash


def clean_url(url):
    if isinstance(url, (bytes, str)):
        if isinstance(url, bytes):
            url = url.decode('utf-8')
        url = urlsplit(url)
    s, n, p, q, f = url
    s = s or 'https'
    pq = dict(parse_qsl(q))
    return urlunsplit((s, n, p, urlencode(pq), f))


def next_url(url):
    s, n, p, q, f = urlsplit(url)
    pq = dict(parse_qsl(q))
    pq['s'] = int((pq.get('s') or 0)) + 44
    return urlunsplit((s, n, p, urlencode(pq), f))


def SplashRequest(url, callback):
    return scrapy_splash.SplashRequest(
        url=url,
        callback=callback,
        args={'timeout': 3600})


class ProductsSpider(scrapy.Spider):
    name = 'products'

    def start_requests(self):
        urls = ('https://world.taobao.com',)
        for u in urls:
            yield SplashRequest(url=u, callback=self.parse)

    def parse(self, response):
        XPATH_CATEGORY = "//div[@class='cat-title']//a/@href"

        for l in response.xpath(XPATH_CATEGORY).extract():
            yield SplashRequest(
                url=clean_url(l),
                callback=self.parse_items_list)

    def parse_items_list(self, response):
        XPATH_ITEM = "//a[contains(@id, 'J_Itemlist_PLink_')]/@href"
        XPATH_NEXT_PAGE = (
            "//div[@id='mainsrp-pager']//li[@class='next']/a[class='J_Ajax']")

        for l in response.xpath(XPATH_ITEM).extract():
            yield SplashRequest(
                url=clean_url(l),
                callback=self.parse_item)

        if response.xpath(XPATH_NEXT_PAGE).extract_first():
            yield SplashRequest(
                url=next_url(clean_url(response.url)),
                callback=self.parse_items_list)

    def parse_item(self, response):
        yield {'url': response.url}
