'''
from bs4 import BeautifulSoup
import requests
#获取新闻正文
def getArticleByUrl():
    url = 'https://news.sina.com.cn/o/2020-12-15/doc-iiznezxs6986815.shtml?cre=tianyi&mod=pcpager_news&loc=20&r=9&rfunc=98&tj=none&tr=9'
    payload = {}
    headers = {}
    response = requests.get(url)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'lxml')
    getArticle = soup.find(id='article')
    getArticleDetails = getArticle.find_all('p')
    txtFile = open(r"Library\1.txt", "wt")
    for child in getArticleDetails:
        print(child.text,file=txtFile)
    txtFile.close()
    getArticleLinks=soup.find_all("h3",class_='ty-card-tt')
    print(getArticleLinks)
    print("running...")
    for link in getArticleLinks:
        print("running...")
        print(link)


if __name__ == '__main__':
    getArticleByUrl()

'''

from bs4 import BeautifulSoup
import requests
import sqlite3
import queue
import threading
import io
import sys
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from COVID_Spider_Layout import *
import hashlib

sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8')


def createSqlite3Table():
    # 创建sqlite表,如果已经存在则跳过
    sql = '''
    create table buff
           (id int primary key not null,
            name text,
            scale_buff2steam  real,
            scale_steam2buff  real,
            minus_steam2buff real,
            steam_min_price real,
            buff_min_price real,
            buffonSale int,
            buffBuy int,
            buy_max_price real,
            exterior text,
            type text,
            category_group text,
            steam_market_link text,
            time  text
            );
     '''
    try:
        c.execute(sql)  # 执行sql语句
        conn.commit()  # 提交数据库操作
        print("数据库创建成功！")
    except (sqlite3.OperationalError):
        print("数据库开启成功！")
        pass

class spiderThread(threading.Thread):
    def __init__(self,threadID,name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name

    def run(self):
        print('Starting:'+self.name)
        while True:
          print("URL序列剩余:",q.qsize())
          getArticleByUrl()

#页面解析
def getArticleByUrl():
    "解析新闻页面,获取相关链接"
    url = q.get()
    payload = {}
    headers = {}
    response = requests.get(url)
    response.encoding = 'GBK'
    soup = BeautifulSoup(response.text, 'lxml')
    getTitle = soup.find("h1")
    #输入文件
    txtStr="Library\{}.txt".format(getTitle.text)
    print(txtStr)
    txtFile = open(txtStr,"wt",encoding="utf-8")
    #print("----------------------------------------------")
    print(getTitle.text,file=txtFile)
    print(url)
    getArticleBlock = soup.find(id="rwb_zw")
    getArticle = getArticleBlock.find_all("p")
    for child in getArticle:
        print(child.get_text(),file=txtFile)
    # 获取相关新闻
    try:
        getLinksBlock = soup.find("div", class_="clearfix box_news")
        getLinks = getLinksBlock.find_all("a")
        getLinksToSearch(getLinks)
    except:
        print("无相关新闻栏")
        return



def getLinksToSearch(getLinks):
    "将相关新闻中符合的url加入url队列中"
    for child in getLinks:
        url=child['href']
        if compareDict(child.get_text())==True:
            if  ("2020" in url):
                print(child.get_text())
                print(url)
                if not url in urlHistory:
                    print("url不重复")
                    q.put(url)
                    urlHistory.add(url)
                else:
                    print("很重复")

def compareDict(str):
    "比较输入字符串是否包含新冠相关关键词"
    dict={0:'新冠',1:'冠状病毒',2:'疫情',3:'方舱医院',4:'呼吸衰竭',5:'肺炎',6:'COVID'}
    for i in range(len(dict)):
        if dict[i] in str:
            return True
        else:
            pass
    return False

def urlSquare():
    "url调度器,宽度优先"
    threads = []
    for i in range(3):
        thread = spiderThread(i, "name")  # 指定线程i的执行函数为myThread
        threads.append(thread)  # 先讲这个线程放到线程threads
    url = ['http://world.people.com.cn/n1/2020/0820/c1002-31830298.html',
           'http://world.people.com.cn/n1/2020/0714/c1002-31783025.html',
           'http://world.people.com.cn/n1/2020/1218/c1002-31970532.html', ]
    for i in url:
        urlHistory.add(i)
    for i in range(3):
        q.put(url[i])
    for t in threads:
        t.start()

def textShow(filename):
    f = open(filename,'r',encoding='utf-8')
    ui.textBrowser.setText(f.read())

def txtList():
    d = QDir()
    d.cd("Library")
    for i in d.entryList()[2:]:
        ui.listWidget.addItem(i)


if __name__ == '__main__':
    conn=sqlite3.connect("COVID-Database.db")
    c = conn.cursor()
    createSqlite3Table()
    q = queue.Queue()
    urlHistory = set()
    app = QApplication(sys.argv)
    Mainwindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(Mainwindow)
    Mainwindow.show()
    filename="Library/澳大利亚单日新增新冠病例数创新高.txt"
    #textShow(filename)
    #urlSquare()
    txtList()
    sys.exit(app.exec_())


