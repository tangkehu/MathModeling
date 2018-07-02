# 数学建模智慧教学平台
是一个人工智能与教育届的初次碰撞，这是一次尝试也是一个开端。
主要使用协同推荐算法和用户画像为学生提供精准服务。

## 运行日志
运行日志的位置在app/static/logs/run.log

在运行过程中出现的BUG将会记录在该日志文件。

## 部署日志
部署日志记录在实施部署的过程中所遇到的问题。

### flask-moment扩展的使用问题
本项目在使用flask-moment的过程中介于数据库设计的原因，只能传递给moment的参数类型为int型的timestamp时间戳，然后flask-moment没有默认处理int类型的时间戳。需要对源码进行如下更改。

源代码为：
```
class _moment(object):

    ...
    
    def _timestamp_as_iso_8601(self, timestamp):
    tz = ''
    if not self.local:
        tz = 'Z'
    return timestamp.strftime('%Y-%m-%dT%H:%M:%S' + tz)
    
    ...
```

修改后的代码为：
```
class _moment(object):

    ...
    
    def _timestamp_as_iso_8601(self, timestamp):
    tz = ''
    if not self.local:
        tz = 'Z'
    if isinstance(timestamp, int):
        timestamp = datetime.utcfromtimestamp(timestamp)
    return timestamp.strftime('%Y-%m-%dT%H:%M:%S' + tz)
    
    ...
```

增加了参数int型判断。

### IIS部署时url链接中文乱码问题
IIS服务器默认为ASCII，当前解决方法为将所有的url链接中的中文全部由python自带的urllib模块的quote和unquote方法进行转换。

转换方法如下：

引入包
`from urllib.parse import quote, unquote`

转换成非中文
`return redirect(url_for('.search', words=quote(words)))`

转换成中文
`words = unquote(words)`

例如：
```
@news.route('/search/<words>', methods=['GET', 'POST'])
@login_required
def search(words):
    words = unquote(words)
    if request.method == 'POST':
        words = request.form.get('words')
        if words:
            return redirect(url_for('.search', words=quote(words)))
        flash('请输入关键词')
    news_list = News.search(words)
    return render_template('news/main.html', active_flg=['news'], words=words, news_list=news_list)
```

