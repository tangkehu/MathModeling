import urllib, re, datetime
from flask import request, redirect, url_for, render_template
from flask_login import login_required
from . import teaching
from ..models import KnowResource


@teaching.route('/main/', methods=['GET', 'POST'])
@login_required
def main():
    if request.method == 'POST':
        return redirect(url_for('.search', words=request.form.get("words")))
    if request.method == 'GET':
        return render_template('teaching/main.html', active_flg=['teaching'])


@teaching.route('/search/<words>', methods=['GET', 'POST'])
@login_required
def search(words):
    if request.method == 'POST':
        words = request.form.get("words")
        url_key = request.form.get('url_key')
        url_key = url_key.encode('utf-8')
        url_page = request.form.get('url_page')
        url_page = int(url_page)
        url_page_1 = 0
        url_page_2 = (url_page - 1) * 20
        while url_page_1 >= 0 and url_page_1 <= url_page_2:
            url_page_1 = str(url_page_1)
            url = r'http://news.baidu.com/ns?word=title%3A%28' + url_key + r'%29&pn=' + url_page_1 + r'&cl=2&ct=0&tn=newstitle&rn=20&bt=0&et=0'
            htm = urllib.urlopen(url).read()
            p_1 = re.compile(r'''<h3 class="c-title"><a href="(.*?)".*?>(.*?)<\/div><\/div><div''')
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
                p_5 = re.compile(r'''c-title-author">.*?({'fm':'sd'}">(\d+).*?>></a>|$)''')
                s_5a = p_5.search(line[1]).groups()
                s_5 = list(s_5a)
                if s_5[1] == None:
                    s_5[1] = 0
                s_5 = int(s_5[1])
                s_5 = s_5 + 1
                s_5 = str(s_5)
            url_page_1 = int(url_page_1)
            url_page_1 += 20
            KnowResource.helpful()
        return redirect(url_for('.search', words=words)) if words else redirect(url_for('.main'))
    if request.method == 'GET':
        return render_template('teaching/search.html', active_flg=['teaching'], words=words)
