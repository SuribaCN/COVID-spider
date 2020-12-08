#get方法研究
"""
import requests
url = 'http://www.cntour.cn/'
strhtml = requests.get(url)
print(strhtml)
"""
#Header研究
"""
import requests
url = 'https://music.163.com'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36 Edg/87.0.664.47'}
html = requests.get(url, headers=headers)
print(html)
print('****')
print(html.text)
"""

#post方法研究
#区别于get，post方法必须构建请求头

import requests
import json
def get_translate_date(word=None):
  #构建请求头
  #构建url，在网页F12-Header中获取“Request URL”
  #构建Form_data，其为键值对组，格式也由网页端获取
  url = 'http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule'
  Form_data={
'i': word,
'from': 'AUTO',
'to': 'AUTO',
'smartresult': 'dict',
'client': 'fanyideskweb',
'salt': '16073335860665',
'sign': 'de5eb7914e485ea1d01f17c058865d88',
'lts': '1607333586066',
'bv': '4f7ca50d9eda878f3f40fb696cce4d6d',
'doctype': 'json',
'version': '2.1',
'keyfrom': 'fanyi.web',
'action': 'FY_BY_REALTlME',}
  response = requests.post(url,data=Form_data)
  #print(response.text)
  content = json.loads(response.text)
  print(content)
  '''
   json字符串数组格式分析，目标源自Response中返回值
  {
        "translateResult":
         [[{"tgt": "I love you", "src": "我爱你"}]],
       "errorCode": 0, 
       "type": "zh-CHS2en",
       "smartResult": {"entries": ["", "I love you\r\n"], "type": 1}
       }
   #'translateResult'对应的是“translateResult”“errorCode”“type”，相当于数组、变量的id
   实际输出的content中没有smartResult这一条，导致无法指定，原理暂时未知。
   其中translateResult可以由两层[]看出其内容是一个二维数组，需要具体指定到某一个元素，而在指定
   其具体为某个元素后，在指明需要被打印的变量名/标签“tgt”
  '''
  print(content['translateResult'][0][0]["tgt"])
  #if __name__=='__main__'的含义为只有直接作为脚本时会被执行，被import到其他脚本时不会自动执行
if __name__=='__main__':
    get_translate_date('新冠病毒')




'''
#bs4 测试
html_doc = """
<html><head><title>The Dormouse's story</title></head>

<p class="title"><b>The Dormouse's story</b></p>

<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>

<p class="story">...</p>
'''