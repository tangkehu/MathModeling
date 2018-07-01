import requests
import re
from flask import current_app


class WebSpider:
    """网络爬虫"""
    def __init__(self, words):
        self.result = []
        self.words = words
        self.url = ''
        self.html = ''
        self.headersParameters = {    # 发送HTTP请求时的HEAD信息，用于伪装为浏览器
            'Connection': 'Keep-Alive',
            'Accept': 'text/html, application/xhtml+xml, */*',
            'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'User-Agent': 'Mozilla/6.1 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'
        }

    def get_baidu(self):
        self.url = 'https://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=1&tn=monline_dg&wd={}'.format(self.words)
        response = requests.get(self.url, headers=self.headersParameters)
        if response.status_code is not 200:
            current_app.logger.info('爬虫请求链接响应的状态码不是200')
            return self.result
        else:
            self.html = response.text
            self.result = re.findall(r'''href = "(.*?)".*?>(.*?)</a>.*?style="text-decoration:none;">(.*?)&nbsp;</a>''',
                                     self.html, re.MULTILINE | re.DOTALL)
            return self.result
