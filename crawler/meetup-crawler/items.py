# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class GroupItem(scrapy.Item):
    groupId = scrapy.Field()
    groupName = scrapy.Field()
    categoryName = scrapy.Field()
    membersId = scrapy.Field()
