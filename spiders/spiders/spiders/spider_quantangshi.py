# coding: utf-8
from scrapy.spider import Spider
import scrapy


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
        # file_name = "poem/" + response.url.split("/")[-1].split(".")[0]
        # file_open = open(file_name, 'wb')
        for sel in response.xpath('//span'):
            # file_open.writelines(sel.encode('utf-8'))
	    link = sel.xpath('a/@href').extract()
