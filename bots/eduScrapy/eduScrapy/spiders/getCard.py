import base64

import scrapy
import urllib.request
from scrapy import Spider, cmdline, Request, FormRequest

from bots.eduScrapy.eduScrapy.Tool import yzm
from bots.eduScrapy.eduScrapy.items import amountItem


class AmountSpider(Spider):
    name = "amount"

    # 指定pipline
    custom_settings = {
        'ITEM_PIPELINES': {
            'eduScrapy.pipelines.amountPipline': 300
        }
    }

    def __init__(self, username=None, password=None, *args, **kwargs):
        super(AmountSpider, self).__init__(*args, **kwargs)
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
        yield FormRequest(url=url, cookies=cookies, callback=self.getBalance, method="POST", formdata=formatdata)

    def getBalance(self, response):
        url = "http://202.207.245.234:9090/queryBalance.action"
        Cookie = response.request.headers.getlist('Cookie')
        cookies = {}
        for cookie in Cookie:
            #  转码并对每一行用 = 分隔开，在加入到字典当中
            cookie = cookie.decode("utf-8").split('=')
            cookies[cookie[0]] = cookie[1]
        yield FormRequest(url=url, cookies=cookies, callback=self.parse, method="GET")

    def parse(self, response):
        Item = amountItem()
        Item['amount'] = response.xpath('/html/body/table//td/font/text()').get()
        Item['studentid'] = self.username
        yield Item
