import scrapy

from scrapy import Spider, Request, cmdline, FormRequest


class SpiderRequest(Spider):
    name = "spider_request"

    def start_requests(self):
        url = "http://202.207.247.49/Home/Default"
        cookies = {
            "ASP.NET_SessionId": "canujsnuqlojigcquf2fg4pl",
            '__RequestVerificationToken': 'KrdCc8ISStfgpgOLHEmLNaWJglvkX_uZJEhewOPjAEZuW2uWIsmtTUzppfBVwE_T_UK_AsB6M6KsIbjsypIbn_M0lIC5wWUfBwDOcTXXcZs1',
            # 'learun_login_error': 'Overdue',
        }
        headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Host': '202.207.247.49',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Referer': 'http://202.207.247.49/Tresources/A1Xskb/XsKbIndex',
            'Origin': 'http://202.207.247.49',
            'Connection': 'keep-alive',
        }
        # yield  Request(url=url,callback=self.parse,method="POST",body=json.dumps(formatdata),headers=headers)
        yield FormRequest(url=url, cookies=cookies,callback=self.parse, method="POST",headers=headers)

    def parse(self, response):
        print(response.request.headers)
