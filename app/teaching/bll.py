import requests
import re
import datetime


def baidu_news_search(words):
    result = []
    url = r'http://news.baidu.com/ns?word=title%3A%28' + words + r'%29&pn=0&cl=2&ct=0&tn=newstitle&rn=20&bt=0&et=0'
    try:
        htm = requests.get(url).text
    except:
        htm = ''
    p_1 = re.compile(r'''<h3 class="c-title"><a href="(.*?)".*?>(.*?)<\/div><\/div><div''',
                     re.MULTILINE | re.DOTALL)
    s_1 = p_1.findall(htm)
    for line in s_1:
        p_2 = re.compile(r'^(.*?)<\/a><\/h3><div class="c-title-author">')
        s_2 = p_2.search(line[1]).groups()
        s_2 = s_2[0].replace('<em>', '')
        s_2 = s_2.replace('</em>', '')
        s_2 = s_2.replace('&quot;', '')

        p_3 = re.compile(r'c-title-author">((.*?)&nbsp;&nbsp;.*?|\d+.*?)$')
        s_3a = p_3.search(line[1]).groups()
        s_3 = list(s_3a)
        if s_3[1] == None:
            s_3[1] = 'null'

        date = datetime.datetime.now()
        p_4 = re.compile(r'c-title-author">.*?(\d+?.*?)($|&nbsp;.*?</a>)')
        s_4 = p_4.search(line[1]).groups()
        s_4 = s_4[0].replace(' ', '')
        s_4 = s_4.replace('</div>', '')
        s_4 = s_4.replace(s_3[1] + '&nbsp;&nbsp;', '')
        s_4 = s_4.replace('年', '-')
        s_4 = s_4.replace('月', '-')
        s_4 = s_4.replace('日', ' ')
        pr = re.compile(r'(\d+)(\D{6})')
        s_4a = pr.search(s_4)
        if s_4a != None:
            s_4a = s_4a.groups()
            if s_4a[1] == '分钟前':
                s_4b = int(s_4a[0])
                s_4 = date - datetime.timedelta(minutes=s_4b)
            else:
                s_4b = int(s_4a[0])
                s_4 = date - datetime.timedelta(hours=s_4b)

        # p_5 = re.compile(r'''c-title-author">.*?({'fm':'sd'}">(\d+).*?>></a>|$)''')
        # s_5a = p_5.search(line[1]).groups()
        # s_5 = list(s_5a)
        # if s_5[1] == None:
        #     s_5[1] = 0
        # s_5 = int(s_5[1])
        # s_5 = s_5 + 1
        # s_5 = str(s_5)

        result.append({
            'url': line[0],
            'title': s_2,
            'source': s_3[1],
            'data': s_4
        })
    return result
