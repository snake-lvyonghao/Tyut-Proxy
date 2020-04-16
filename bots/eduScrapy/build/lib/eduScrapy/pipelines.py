# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from bots.eduScrapy.eduScrapy.items import EduscrapytestItem


class EduscrapyPipeline(object):
    def process_item(self, item, spider):
        if isinstance(item,EduscrapytestItem):
            item.save(commit=True)
            print(item)
            return item
