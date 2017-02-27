# coding: utf-8
from scrapy.spider import Spider
import scrapy
import logging
import os


class SpiderQuanTangPoem(Spider):
    name = "spider_quan_tang_poem"
    allowed_domains = [
        "http://www3.zzu.edu.cn"
    ]
    start_urls = [
        "http://www3.zzu.edu.cn/qtss/zzjpoem1.dll/query"
    ]

    def parse(self, response):
        """
            use to get the url of chapters
        """
        chapter_url_list = list()
        for sel in response.xpath('//span'):
            link = sel.xpath('a/@href').extract()
            chapter_url_list.append(link[0])
        # get the poem url list
        for url in chapter_url_list:
            yield scrapy.Request(url, callback=self.parse_poem_list, dont_filter=True)

    def parse_poem_list(self, response):
        """
            get the poem url list
        """
        poem_url_list = list()

        for sel in response.xpath('/html/body/div[1]/center/table/tr[2]/td[2]/p/a'):
            text = sel.xpath('text()').extract()
            if text[0] == u'下页':
                logging.info("yes")
                link = sel.xpath('@href').extract()
                yield scrapy.Request(link[0], callback=self.parse_poem_list, dont_filter=True)

        for sel in response.xpath('//span'):
            # file_open.writelines(sel.encode('utf-8'))
            link = sel.xpath('a/@href').extract()
            poem_url_list.append(link[0])

        for url in poem_url_list:
            yield scrapy.Request(url, callback=self.parse_poem, dont_filter=True)

    def parse_poem(self, response):
        """
            get the poem
        """
        chapter_poem = response.url.split("/")[-1].split("?")[1].split("&")
        folder_name = "/Users/koprvhdix/Projects/PoemTools/poem/" + chapter_poem[0].split("=")[1]
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
        file_name = folder_name + "/" + chapter_poem[1].split("=")[1]
        file_open = open(file_name, 'w')
        text_set = response.xpath('//font/text()').extract()
        for text in text_set:
            file_open.writelines(text)
