# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader import ItemLoader
from scrapy.http import Request
from scrapy.loader.processors import Join,MapCompose,TakeFirst
from xcSpider.items import AskspiderItem


class WendaspiderSpider(scrapy.Spider):
    name = "wendaSpider"
    allowed_domains = ["you.ctrip.com"]
    start_urls = []
    q="北京"
    start_urls.append("http://you.ctrip.com/asks/search/?keywords=%s" % str(q))

    def parse(self, response):
    	base="http://you.ctrip.com"
    	links=response.xpath("//li[@class='cf']/@href").extract()
    	for l in links:
    		link=base+l
    		yield Request(link,callback=self.parse_item)
    	next=response.xpath("//a[@class='nextpage']/@href").extract()
    	if next:
    		url=base+next[0]
    		yield Request(url,callback=self.parse)

    def parse_item(self,response):
    	l=ItemLoader(item=AskspiderItem())
    	l.add_xpath('q_title',"//h1[@class='ask_title']/text()",MapCompose(unicode.strip),Join())
    	l.add_xpath('q_time',"//span[@class='ask_time']/text()",MapCompose(unicode.strip))
    	l.add_xpath('q_province',"//div[@class='abouttdd']/ul/li[1]/h3/span/text()",MapCompose(unicode.strip))
    	l.add_value('q_link',response.url)
    	l.add_xpath('q_user',"//a[@class='ask_username']/text()")
    	return l.load_item()
		# l.add_xpath('q_content',"//div[@class='breadbar_v1 cf']/ul/li[4]/a/text()",MapCompose(lambda i:i.replace("景点",'')))
		# l.add_xpath('q_huida',"//span[@class='youcate']/text()",MapCompose(unicode.strip))
		

        
