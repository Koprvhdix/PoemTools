# coding: utf-8
from scrapy.spider import Spider
import scrapy


class SpiderGushiwenOrg(Spider):
    name = "spider_gushiwen_org"
    allowed_domains = ["www.diyifanwen.com"]
    start_urls = [
        "http://www.gushiwen.org/gushi/tangshi.aspx",
        "http://www.gushiwen.org/gushi/songsan.aspx",
        ""
    ]

    def parse(self, response):
        poem_url = list()
        for sel in response.xpath('//dd'):
            link = sel.xpath('a/@href').extract()
            poem_url.append('http://www.diyifanwen.com' + link[0])

        for item in poem_url:
            yield scrapy.Request(item, callback=self.parse_next)

    def parse_next(self, response):
        file_name = "poem/" + response.url.split("/")[-1].split(".")[0]
        file_open = open(file_name, 'wb')
        for sel in response.xpath('//p').extract():
            file_open.writelines(sel.encode('utf-8'))
