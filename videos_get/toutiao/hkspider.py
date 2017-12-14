#-*-coding:utf-8-*-
import requests,re,sys,time
from PyQt5.QtCore import pyqtSignal,QThread
from bs4 import BeautifulSoup as bs
import json

class hkspider(QThread):
    finalInfo = pyqtSignal(dict)
    def __init__(self,category,maxcount):

        super().__init__()
        self.category = category
        self.maxcount = maxcount
        self.isFirstPage = True
        self.headers = {
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'
        }
        self.sess = requests.session()
        self.rett = [] #临时存放
        self.ret = [] #返回值
        print(category)
    def run(self):
        self.get_info()
    def get_info(self):
        lt = time.time() #初始时间，现在时间
        bt = int(lt) - 601 #追踪到的原来的时候
        lt = str(int(lt*1000))
        bt = str(int(bt))
        url_ua = 'Mozilla%252F5.0%2520(Linux%253B%2520Android%25204.4.2%253B%2520GT-I9500%2520Build%252FKOT49H)%2520AppleWebKit%252F537.36%2520(KHTML%252C%2520like%2520Gecko)%2520Version%252F4.0%2520Chrome%252F30.0.0.0%2520Safari%252F537.366'
        #&bt=1513218715&_=151321914297
        url = 'http://sv.baidu.com/videoui/list/tab?source=wise-channel&pd=' \
              '&subTab='+ self.category +\
              '&direction=down&refreshType=1' \
              '&ua=' + url_ua +\
              '&bt=' + bt + \
              '&caller=bdwise' + \
              '&_=' + lt +\
              '&cb=jsonp1'
       # url = 'http://sv.baidu.com/videoui/list/tab?source=wise-channel&pd=&subTab=doubiju&direction=down&refreshType=1&ua=Mozilla%252F5.0%2520(Linux%253B%2520Android%25204.4.2%253B%2520GT-I9500%2520Build%252FKOT49H)%2520AppleWebKit%252F537.36%2520(KHTML%252C%2520like%2520Gecko)%2520Version%252F4.0%2520Chrome%252F30.0.0.0%2520Safari%252F537.36&bt=1513218715&caller=bdwise&_=1513219142976&cb=jsonp1'

        try:
            res = requests.get(url, headers=self.headers, timeout = 8)
            res.encoding = 'utf-8'
            t = res.content.decode('unicode_escape',errors='ignore').replace('\\/', '/')
            tpl_re = re.search('"tpl":"(.*)\)',t,re.DOTALL)
            tpl = tpl_re.group(1)  # 获取Json部分的网页
            soup = bs(tpl,'html.parser') #获取的网页解析
            lis = soup.select('li')
            print(len(lis))
            for li in lis:
                try:
                    title = li.select('h4')[0].text
                    count = li.select('div.video-list-item-poster-shade > p')[0].text.strip()
                    video_play_count = float(re.search('^(\d{0,4}\.?\d{0,4})', count).group(1))
                    if '万' in count:
                        video_play_count = int(video_play_count*10000)

                    time_period= li.select('span.video-list-item-poster-duration')[0].text
                    avatar_url = li.select('img.video-list-item-poster-img')[0]['data-src']
                    source_url = li.select('div.video-show-default > div.video-icon-play')[0]['data-jump']
                    video_url = self.processData(source_url)
                    print(title)
                    ret = {
                        'source': '好看视频',
                        'title': title,
                        'abstract': '此站没有描述',
                        'media_url': '#' , #此站无法获取此用户其他的视频
                        'source_url': source_url,
                        'video_play_count': video_play_count,
                        'publish_time': '最新',
                        'avatar_url': avatar_url,
                        'video_id': '',#无法获取
                        'time_period': time_period,
                        'video_url':video_url,
                        'video_type':'mp4',  #未提供格式，随便写个默认的吧
                        'video_def':'',
                    }
                    self.finalInfo.emit(ret)
                except Exception as e:
                    print(e)

        except Exception as e:
            print(e)

    def processData(self,url):
        res = requests.get(url,headers = self.headers,timeout=5)
        txt = res.text
        url_re = re.search(',playurl:\s?\'(.+?)\'',txt)
        video_url = url_re.group(1).replace('\\/','/')
        time.sleep(0.2)
        return  video_url

# t = hkspider('tuijian',10)
# t.start()
# time.sleep(20)

# a = '{\\"name\\":\\"michael\\"}'
# print(a)
# print(type(json.loads('"' + a + '"')))
#
# print(type(json.loads(json.loads('"' + a + '"'))))
# print(json.loads(json.loads('"' + a + '"')))

