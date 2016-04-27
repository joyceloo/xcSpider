# coding=utf-8
import scrapy
from scrapy.spiders import Spider 
from xcSpider.items import XcspiderItem,YjspiderItem
from scrapy.loader import ItemLoader
from scrapy.loader.processors import Join,MapCompose,TakeFirst
# from scrapy.spiders import CrawlSpider,Rule
from scrapy.http import Request
# from scrapy.linkextractors import LinkExtractor
from bs4 import BeautifulSoup

class SpiderXC(Spider):
	name="xiechengSP"
	allowed_domains=['you.ctrip.com']
	start_urls=['http://you.ctrip.com/place/beijing1.html',]

	def parse(self,response):
		base="http://you.ctrip.com"
		sel=response.xpath("//div[@class='innerbox']/ul[@class='cf']")
		sight=sel.xpath("li[4]/a/@href").extract()
		eat=sel.xpath("li[@class='current']/a/@href").extract()
		yj=sel.xpath("li[9]/a/@href").extract()
		sight_url=base+str(sight[0])
		# eat_url=base+str(eat[0])
		# yj_url=base+str(yj[0])
		return Request(sight_url,callback=self.parse_sight)
		# yield Request(eat_url,)

	# 	print sight_url

	def parse_sight(self,response):
		# print response.url
		base_url='http://you.ctrip.com'
		# 获取每个景点的点评链接，进一步解析
		sights=response.xpath("//div[@class='list_wide_mod2']/div[@class='list_mod2']")
		for sight in sights:
			# item=XcspiderItem()
			tmp=sight.xpath("div[@class='rdetailbox']/dl/dt/a")
			sname=tmp.xpath("text()")[0].extract()
			s_url=tmp.xpath("@href")[0].extract()
			dp_url=base_url+s_url
			print "dp_url: %s " % dp_url
			yield Request(dp_url,callback=self.parse_dp)
		next_page=response.xpath("//a[@class='nextpage']/@href").extract()[0]
		if next_page:
			next_url=base_url+next_page
			yield Request(next_url,callback=self.parse_sight)

	# 利用itemloader
	def parse_dp(self,response):
		base_url='http://you.ctrip.com/destinationsite/TTDSecond/SharedView/AsynCommentView?'
		end="poiID=75595&districtId=1&districtEName=Beijing&pagenow=%s&order=3.0&star=0.0&tourist=0.0&resourceId=229&resourcetype=2"
		links=response.xpath("//ul/li[@class='from_link']/span[@class='f_right']/a[@class='gsn_btn_detail']/@href").extract()
		for l in links:
			link="http://you.ctrip.com"+l
			yield Request(link,callback=self.parse_item)
		m=response.xpath("//a[@class='current']/text()").extract()[0]
		# print m
		mark=str(int(m)+1)
		# print mark
		next_page=response.xpath("//a[@class='nextpage']/@href").extract()
		if next_page:
			end_url=end % mark
			next_url=base_url+end_url
			# print next_url
			yield Request(next_url,callback=self.parse_dp)

	def parse_item(self,response):
		l=ItemLoader(item=XcspiderItem(),response=response)
		m=response.xpath("//span[@class='ellipsis']/a/@title")
		# print m
		l.add_xpath('dp_content',"//ul/li[@class='main_con']/text()",MapCompose(unicode.strip),Join())
		l.add_xpath('dp_user',"//span[@class='ellipsis']/a/@title",MapCompose(unicode.strip))
		l.add_value('dp_link',response.url)
		l.add_xpath('dp_scence',"//div[@class='f_left']/h1/text()")
		l.add_xpath('dp_provice',"//div[@class='breadbar_v1 cf']/ul/li[4]/a/text()",MapCompose(lambda i:i.replace("景点",'')))
		l.add_xpath('dp_time',"//span[@class='youcate']/text()",MapCompose(unicode.strip))
		return l.load_item()

	def parse_youji(self,response):
		base="http://you.ctrip.com"
		links=response.xpath("//a[@class='journal-item cf']/@href").extract()
		for i in links:
			link=base+i[0]
			yield Request(link,callback=self.parse_item_yj)
		next=response.xpath("//a[@class='nextpage']/@href").extract()
		if next:
			next_url=base+next[0]
			yield Request(next_url,callback=self.parse_youji)

	def parse_item_yj(self,response):
		l=ItemLoader(item=YjspiderItem(),response=response)
		l.add_xpath('yj_title',"//div[@class='ctd_head_left']/h2/text()",MapCompose(unicode.strip),Join())
		l.add_xpath('yj_time',"//div[@class='w_journey']/dl/dt/span[2]/text()",MapCompose(unicode.strip))
		l.add_value('yj_link',response.url)
		l.add_xpath('yj_looknum',"//a[@class='link_browse']/span/text()")
		l.add_xpath('yj_pl',"//a[@class='link_comment']/span/text()")
		l.add_xpath('yj_author',"//a[@id='authorDisplayName']/text()",MapCompose(unicode.strip))
		l.add_xpath('yj_province',"//div[@class='breadbar_v1 cf']/ul/li[4]/a/text()")
		return l.load_item()
			










