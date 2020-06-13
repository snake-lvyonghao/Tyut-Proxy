from scrapy import Spider, Request, FormRequest, cmdline

from DoubleHaoapp.models import Student
from bots.eduScrapy.eduScrapy import Tool
from bots.eduScrapy.eduScrapy.items import PersonalInformationItem


class XskkcSpider(Spider):
    name = "pi"

    # 指定pipline
    custom_settings = {
        'ITEM_PIPELINES': {
            'eduScrapy.pipelines.EduscrapyPipeline': 300
        }
    }

    def __init__(self, username=None, password=None, *args, **kwargs):
        super(XskkcSpider, self).__init__(*args, **kwargs)
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
            yield FormRequest(url=url, cookies=cookies, callback=self.GeXsKb, method="GET", headers=headers)
        else:
            # 登陆失败相应处理
            pass

    # 获取成绩统计分析
    def GeXsKb(self, response):
        url = 'http://202.207.247.49/Tschedule/C6Cjgl/GetXskccjResult'
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
            'Referer': 'http://202.207.247.49/Tschedule/C6Cjgl/XskccjIndex',
            'Origin': 'http://202.207.247.49',
            'Connection': 'keep-alive',
        }
        yield FormRequest(url=url, cookies=cookies, callback=self.parse, method="POST",
                          headers=headers)

    def parse(self, response):
        item = PersonalInformationItem()
        item['ClassId'] = Student.objects.get(
            Sid=response.xpath('/html/body/div[1]/div/div[1]/div[2]/span/text()').extract()[0])
        item['Class'] = response.xpath('/html/body/div[1]/div/div[2]/div[2]/span/text()').extract()[0]
        item['Coct'] = response.xpath('/html/body/div[1]/div/div[3]/div[2]/span/text()').extract()[0]
        item['Gpa'] = response.xpath('/html/body/div[1]/div/div[4]/div[2]/span/text()').extract()[0]
        item['GpaSort'] = response.xpath('/html/body/div[1]/div/div[5]/div[2]/span/text()').extract()[0]
        item['WeightSort'] = response.xpath('/html/body/div[1]/div/div[6]/div[2]/span/text()').extract()[0]
        item['AverageCredit'] = response.xpath('/html/body/div[1]/div/div[7]/div[2]/span/text()').extract()[0]
        item['AverageCreditSort'] = response.xpath('/html/body/div[1]/div/div[8]/div[2]/span/text()').extract()[0]
        item['FailingCredits'] = response.xpath('/html/body/div[1]/div/div[9]/div[2]/span/text()').extract()[0]
        item['Name'] = response.xpath('/html/body/div[2]/div/div[1]/div[2]/span/text()').extract()[0]
        item['TotalCreditsRequired'] = response.xpath('/html/body/div[2]/div/div[2]/div[2]/span/text()').extract()[0]
        try:
            item['ComInPraCre'] = response.xpath('/html/body/div[2]/div/div[3]/div[2]/span/text()').extract()[0]
        except:
            item['ComInPraCre'] = 0
        item['GpaSortClass'] = response.xpath('/html/body/div[2]/div/div[4]/div[2]/span/text()').extract()[0]
        item['WeightCredit'] = response.xpath('/html/body/div[2]/div/div[5]/div[2]/span/text()').extract()[0]
        item['WeightCreditSort'] = response.xpath('/html/body/div[2]/div/div[6]/div[2]/span/text()').extract()[0]
        item['AverageSortClass'] = response.xpath('/html/body/div[2]/div/div[7]/div[2]/span/text()').extract()[0]
        item['FailedCredits'] = response.xpath('/html/body/div[2]/div/div[8]/div[2]/span/text()').extract()[0]
        yield item
