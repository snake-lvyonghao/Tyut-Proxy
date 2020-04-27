from scrapy import Spider, Request, FormRequest, cmdline

from DoubleHaoapp.models import Student
from bots.eduScrapy.eduScrapy import Tool
from bots.eduScrapy.eduScrapy.items import KccjItem


class kccj(Spider):
    name = "kccj"

    # 指定pipline
    custom_settings = {
        'ITEM_PIPELINES': {
            'eduScrapy.pipelines.EduscrapyPipeline': 300
        }
    }

    def __init__(self, username=None, password=None, *args, **kwargs):
        super(kccj, self).__init__(*args, **kwargs)
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
        cookies = {
            # "ASP.NET_SessionId":"canujsnuqlojigcquf2fg4pl",
            # '__RequestVerificationToken':'KrdCc8ISStfgpgOLHEmLNaWJglvkX_uZJEhewOPjAEZuW2uWIsmtTUzppfBVwE_T_UK_AsB6M6KsIbjsypIbn_M0lIC5wWUfBwDOcTXXcZs1',
            # 'learun_login_error':'Overdue',
        }
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
        yield FormRequest(url=url, cookies=cookies, formdata=formatdata, callback=self.getCookie,
                          method="POST", headers=headers)

    # 登陆成功后获取Cookie
    def getCookie(self, response):
        message = response.text.replace("null", "0")
        message = eval(message)
        if message["type"] == 1:
            url = "http://202.207.247.49/Home/Default"
            # 获取登陆请求的Cookie
            Cookie = response.request.headers.getlist('Cookie')
            cookies = {}
            # 便利整个cookies
            for cookie in Cookie:
                #  转码并对每一行用 = 分隔开，在加入到字典当中
                cookie = cookie.decode('utf-8').split('=')
                cookies[cookie[0]] = cookie[1]
            headers = {
                'Accept': 'application/json, text/javascript, */*; q=0.01',
                'Host': '202.207.247.49',
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
                'X-Requested-With': 'XMLHttpRequest',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'Referer': 'http://202.207.247.49/Login/Index',
                'Origin': 'http://202.207.247.49',
                'Connection': 'keep-alive',
            }
            yield FormRequest(url=url, cookies=cookies, callback=self.getkkcj, method="GET", headers=headers)
        else:
            # 登陆失败相应处理
            pass

    def getkkcj(self, response):
        url = 'http://202.207.247.49/Tschedule/C6Cjgl/GetKccjResult'
        Cookie = response.request.headers.getlist('Cookie')
        cookies = {}
        # 便利整个cookies
        for cookie in Cookie:
            #  转码并对每一行用 = 分隔开，在加入到字典当中
            cookie = cookie.decode("utf-8").split('=')
            cookies[cookie[0]] = cookie[1]
        headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Host': '202.207.247.49',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Referer': 'http://202.207.247.49/Tschedule/C6Cjgl/KccjIndex',
            'Origin': 'http://202.207.247.49',
            'Connection': 'keep-alive',
        }
        formdata = {
            'order': 'zxjxjhh desc,kch'
        }
        yield FormRequest(url=url, cookies=cookies, callback=self.parse, method="POST", formdata=formdata,
                          headers=headers)

    def parse(self, response):
        kccjResultList = []
        tr = response.xpath('//tr')
        for td in tr:
            Item = KccjItem()
            if td.xpath('td[1][not(@colspan)]/text()').get() == None:
                continue
            Item['Kid'] = Student.objects.get(Sid=self.username)
            Item['ClassId'] = td.xpath('td[1][not(@colspan)]/text()').get()
            Item['ClassName'] = td.xpath('td[3]/text()').get()
            Item['GPA'] = td.xpath('td[5]/text()').get()
            Item['ClassAttribute'] = td.xpath('td[6]/text()').get()
            Item['TestTime'] = td.xpath('td[7]/text()').get()
            Item['Credit'] = td.xpath('td[8]/text()').get()
            print(Item)
            yield Item
