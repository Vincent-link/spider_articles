import re
from mitmproxy import http
from content import content

content_list_url_redirect = 'https://mp.weixin.qq.com/mp/profile_ext?action=home&__biz=%s#wechat_redirect'

def response(flow):
    req_url = flow.request.pretty_url
    res_headers = flow.response.headers
    req_headers = flow.request.headers
    body = flow.response.text
    status_code = flow.response.status_code

    if status_code == 200:
        if re.compile('r'mp\.weixin\.qq\.com\/mp\/profile_ext\?action=home', re.I).findall(self.req_url):
            '''启动一个线程去抓取到的页面中获取到文章列表的处理'''
            _thread.append(threading.Thread(target=content().run, args=(body)))
            body = get_next_body()

            flow.response = http.HTTPResponse.make(
                200, bytes(body, encoding='utf-8'),
                {'Content-Type': 'text/html', 'Cache-Control': 'no-cache, must-revalidate'}
            )

def get_next_body(content_body):
    if body != '':
        wechat_account_name = parse_wechat_account_name(content_body)
        if wechat_account_name:
            _body = '<p>当前抓取公众号: %s</p>' % (wechat_account_name)
    else:
        _body = ''

    body = '''<meta http-equiv="content-type" content="text/html;charset=utf8">
        <meta id="viewport" name="viewport" content="width=device-width,initial-scale=1.0,maximum-scale=1.0,user-scalable=0" />
        <style>p {font-size:1.25em;}</style>
        %s
        <script>setTimeout(function(){window.location.href="%s";},%s);</script> %s''' %\
        (_body, get_next_url(), str(80*1000), content_body)

    return body

def parse_wechat_account_name(body):
    ''' 从内容中解析公众号名称 '''
    _regular = r'<strong\s+class="profile_nickname"\s+id="nickname">\s+(.*?)\s+</strong>'
    data = re.compile(_regular, re.I).findall(body)

    if data:
        return data[0]

    return False

def get_next_url():
    '''这部分写要跳转到下一页的url'''

if __name__ == '__main__':
    # 注意在运行之前，先确保该文件的同路径下存在一个download的文件夹, 用于存放爬虫下载的图片
    url = 'https://www.zhihu.com/question/27364360'  # 有一双美腿是一种怎样的体验?
    crawl(url)
