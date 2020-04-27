import base64
import json
import re
from datetime import datetime

import scrapy
import urllib.request
from scrapy import Spider, cmdline, Request, FormRequest

from bots.eduScrapy.eduScrapy.Tool import yzm

# from bots.eduScrapy.eduScrapy.items import consumeItem
from bots.eduScrapy.eduScrapy.items import customeItem


class CustomeSpider(Spider):
    name = "custome"

    # 指定pipline
    custom_settings = {
        'ITEM_PIPELINES': {
            'eduScrapy.pipelines.consumePipline': 300
        }
    }

    def __init__(self, username=None, password=None, startDate=datetime.today().strftime('%Y%m%d'),
                 endDate=datetime.today().strftime('%Y%m%d'), *args, **kwargs):
        super(CustomeSpider, self).__init__(*args, **kwargs)
        self.endDate = endDate
        self.startDate = startDate
        self.username = username
        self.password = password

    def start_requests(self):
        url = "http://202.207.245.234:9090/"
        yield Request(url, self.getcheck)

    def getcheck(self, response):
        url = "http://202.207.245.234:9090/login.action"
        Cookie = response.request.headers.getlist('Cookie')
        cookies = {}
        for cookie in Cookie:
            #  转码并对每一行用 = 分隔开，在加入到字典当中
            cookie = cookie.decode("utf-8").split('=')
            cookies[cookie[0]] = cookie[1]
        # 获取登录表单字段
        username = response.xpath('/html/body/form/input[1]/@name').get()
        password = response.xpath('/html/body/form/input[2]/@name').get()

        # 获取验证码，并识别
        headers = {'Cookie': Cookie[0].decode("utf-8"),
                   "Connection": "keep-alive",
                   "Referer": "http://202.207.245.234:9090/index.action"}
        request = urllib.request.Request("http://202.207.245.234:9090/check.action", headers=headers, method="GET")
        response = urllib.request.urlopen(request)
        checkname = yzm(response.read())["words_result"][0]["words"]

        # post数据
        formatdata = {
            username: self.username,
            password: self.password,
            "checkName": checkname,
            "loginType": '1',
            "input": "登陆"
        }
        yield FormRequest(url=url, cookies=cookies, callback=self.getCustome, method="POST", formdata=formatdata)

    def getCustome(self, response):
        url = "http://202.207.245.234:9090/queryConsume.action"
        Cookie = response.request.headers.getlist('Cookie')
        cookies = {}
        for cookie in Cookie:
            #  转码并对每一行用 = 分隔开，在加入到字典当中
            cookie = cookie.decode("utf-8").split('=')
            cookies[cookie[0]] = cookie[1]
        # post数据
        formatdata = {
            "opertype": "query",
            "startDate": self.startDate,
            "endDate": self.endDate,
            "input": "查询"
        }
        yield FormRequest(url=url, cookies=cookies, callback=self.Customepage, method="POST", formdata=formatdata)

    def Customepage(self, response):
        Cookie = response.request.headers.getlist('Cookie')
        cookies = {}
        for cookie in Cookie:
            #  转码并对每一行用 = 分隔开，在加入到字典当中
            cookie = cookie.decode("utf-8").split('=')
            cookies[cookie[0]] = cookie[1]

        # 拿到最后一页的页码
        endpage = int(re.findall(r"\d+\.?\d*", response.xpath('/html/body/a[4]/@href').get())[0])
        # 拿到分页数据
        for i in range(1, endpage + 1):
            url = "http://202.207.245.234:9090/queryConsume.action?opertype=page&page="
            yield FormRequest(url=url + str(i), cookies=cookies, callback=self.parse, method="GET")

    def parse(self, response):
        item = customeItem()
        for i in range(2, 11):
            item['date'] = response.xpath('/html/body/table/tr[' + str(i) + ']/td[1]/text()').get()
            item['department'] = response.xpath('/html/body/table/tr[' + str(i) + ']/td[2]/text()').get()
            item['amount'] = response.xpath('/html/body/table/tr[' + str(i) + ']/td[3]/text()').get()
            yield item

    pass
