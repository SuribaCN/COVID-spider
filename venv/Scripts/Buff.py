#bs4 buff测试

from bs4 import BeautifulSoup
import requests
import re

#获取全部物品列表
url = "https://buff.163.com/market/?game=csgo#tab=selling&page_num=1"
payload={}
headers = {
  'Cookie': 'Device-Id=G7QOBXlyu7DYMmqsgDF3; client_id=cQMlx1SvDIurPgcIeVXkwA; csrf_token=IjJmMzIwYTU3OTFlYzMxMWFkYjBiMmYwMThjODM5M2ZlZWU3YjQ4NDYi.Eq-8ig.9qRbqa-l2_36UluqMtsMjEbWJpU'
}
buffLink = requests.get (url, headers=headers, data=payload)


soup = BeautifulSoup(buffLink.text, 'lxml')
getAllGoodsClass = soup.find_all(attrs={"item w-SelType csgo_filter"})
#data = soup.select("#j_h1z1-selType > div:nth-child(2) > p")

#获取物品大类
goodsCount = 0
for goods in getAllGoodsClass:
  print('物品种类：'+goods.p.get_text()+'  物品标识：'+goods.p['value']+'\t物品索引：',goodsCount)
  goodsCount+=1
print('Total:',goodsCount)
#获取物品小类
#不能通过getClass = soup.find_all(attrs={'cols'})直接获取，有几类物品列表未设定class="cols"
#i为由前所获的大类索引,goodList为小类列表，good为列表元素
getClass = soup.find_all(attrs={'item w-SelType csgo_filter'})

for i in range(goodsCount):
  print(i)
  for goodList in getClass[i].children:
    if(type(goodList)==type(getClass[i])):
      for good in goodList.children:
        if (type(good) == type(getClass[i])):
          print(good.string, good['value'])
    else:
      pass
#获取具体物品

url = 'https://buff.163.com/market/?game=csgo#tab=selling&page_num=1&category_group=shotgun'
#url = "https://buff.163.com/market/?game=csgo#tab=selling&page_num=1"
payload={}
headers = {
  'Cookie': 'Device-Id=G7QOBXlyu7DYMmqsgDF3; client_id=cQMlx1SvDIurPgcIeVXkwA; csrf_token=IjJmMzIwYTU3OTFlYzMxMWFkYjBiMmYwMThjODM5M2ZlZWU3YjQ4NDYi.Eq-8ig.9qRbqa-l2_36UluqMtsMjEbWJpU'
}
a = requests.get (url, headers=headers, data=payload)
print(a)


'''
#对结果数据的处理
for index in range(len(getAllGoodsClass)):
    a=getAllGoodsClass[index],[0]
    b=a[0]
    print(b.li)
    c=b.li['value']
    print(c)
'''


#获取具体价格  弃用
'''
url = "https://buff.163.com/market/goods?goods_id=776764&from=market#tab=selling"
payload={}
headers = {
  'Cookie': 'Device-Id=G7QOBXlyu7DYMmqsgDF3; client_id=cQMlx1SvDIurPgcIeVXkwA; csrf_token=IjJmMzIwYTU3OTFlYzMxMWFkYjBiMmYwMThjODM5M2ZlZWU3YjQ4NDYi.Eq-8ig.9qRbqa-l2_36UluqMtsMjEbWJpU'
}
buffLink = requests.get (url, headers=headers, data=payload)
soup = BeautifulSoup(buffLink.text, 'lxml')
a=soup.find(attrs={"class":"i_Btn i_Btn_mid i_Btn_D_red btn-supply-buy"})
b=soup.find(attrs={"class":"custom-currency"})
print(a)
buffMinPrice= float(a['data-goods-sell-min-price']) / 100
steamMinPrice=float(b['data-price'])
result=buffMinPrice/(steamMinPrice*0.87)
print('buff低价', buffMinPrice,  '\nsteam低价', steamMinPrice,"转换后",steamMinPrice*0.87, '\n比例', result)
'''