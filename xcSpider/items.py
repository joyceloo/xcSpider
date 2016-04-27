# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class XcspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 点评用户
    dp_user=scrapy.Field()
    # 用户网址
    dp_link=scrapy.Field()
    # 点评时间
    dp_time=scrapy.Field()
    # 点评内容
    dp_content=scrapy.Field()
    # dp_useful_count=scrapy.Field()
    # 点评景点
    dp_scence=scrapy.Field()
    dp_provice=scrapy.Field()
    pass

class YjspiderItem(scrapy.Item):
    yj_title=scrapy.Field()
    yj_author=scrapy.Field()
    yj_time=scrapy.Field()
    yj_looknum=scrapy.Field()
    yj_pl=scrapy.Field()
    yj_link=scrapy.Field()
    yj_province=scrapy.Field()
    pass

class AskspiderItem(scrapy.Item):
    q_title=scrapy.Field()
    q_link=scrapy.Field()
    q_time=scrapy.Field()
    q_user=scrapy.Field()
    q_province=scrapy.Field()
    # q_content=scrapy.Field()
    # q_huida=scrapy.Field()
    pass
