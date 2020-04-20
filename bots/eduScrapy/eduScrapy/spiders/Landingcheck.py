import scrapy

from scrapy import Spider, Request, cmdline, FormRequest

from bots.eduScrapy.eduScrapy import Tool

# 注册检查
from bots.eduScrapy.eduScrapy.items import studentItem


class Landingcheck(Spider):
    name = "Landingcheck"

    def __init__(self, username=None, password=None, *args, **kwargs):
        super(Landingcheck, self).__init__(*args, **kwargs)
        self.username = username
        self.password = password

    # 首先拿到RSA的publickey
    def start_requests(self):
        # 设置请求校园网网址

        url = "http://202.207.247.49"
        yield Request(url, self.login_parse)

    def login_parse(self, response):
        publickey = response.xpath("/html/body/div[2]/@data-val").extract()[0]
        url = "http://202.207.247.49/Login/CheckLogin"
        username = Tool.crack_pwd(publickey, self.username)
        formatdata = {
            'username': username,
            'password': self.password,
            'code': '',
            'isautologin': '0'
        }
        cookies = {}
        headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Host': '202.207.247.49',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Referer': 'http://202.207.247.49/Login/Index',
            'Origin': 'http://202.207.247.49/',
            'Connection': 'keep-alive',
        }
        # yield  Request(url=url,callback=self.parse,method="POST",body=json.dumps(formatdata),headers=headers)
        yield FormRequest(url=url, cookies=cookies, formdata=formatdata, callback=self.parse,
                          method="POST", headers=headers)

    def parse(self, response):
        message = response.text.replace("null", "0")
        message = eval(message)
        item = studentItem()
        item['Sid'] = self.username
        item['Spassword'] = self.password
        item['Stype'] = message['type']
        yield item
