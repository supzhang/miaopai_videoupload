#-*- coding:utf-8 -*-
#用于获取头条的视频信息
#https://github.com/liubo0621/headlines_today
import requests
import re
import time
from PyQt5.QtCore import QThread
#mediaurl = https://www.ixigua.com/a6464842031897248269/#mid=58363379363
#https://www.ixigua.com/group/6483718332703834638/
#https://www.ixigua.com/c/user/58363379363/
#https://www.ixigua.com/item/6497799282349834765/
class ttspider(QThread):
    def __init__(self,category,maxcount):  #需要获取的分类
        super().__init__()
        self.category = category
        self.maxcount = maxcount
        self.isFirstPage = True
        self.headers = {
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'
        }
        self.sess = requests.session()
        self.mainurl = 'https://www.ixigua.com'
        self.countnow = 0
        self.rett = [] #临时存放
        self.ret = [] #返回值
    def run(self):
        for x in range(3):
            self.get_info()
        self.processData()

    #
    def get_info(self):
        if self.isFirstPage == True:
            maxmin = 'min_behot_time=0'
            self.isFirstPage = False
        else:
            maxmin = 'max_behot_time=' + self.max_behot_time
        url = 'https://www.ixigua.com/api/pc/feed/?' + maxmin + '&category=' + self.category
        try:
            res = self.sess.get(url, headers=self.headers)
            json = res.json()
            data = json['data']
            l = len(data)
            self.countnow += l
            self.max_behot_time = str(json['next']['max_behot_time'])
            for d in data:
                self.rett.append(d)
            if self.countnow >= self.maxcount:
                return
        except Exception as e:
            print(e)
    def processData(self):
        print(len(self.rett))
        for d in self.rett:
            ret1 = {
                'title':d['title'],
                'abstract':d['abstract'],
                'media_url':self.mainurl + d['media_url'],
                'source_url':self.mainurl + d['source_url'],
                'video_play_count':d['video_play_count'],
                'publish_time':d['behot_time'],
                'avatar_url':d['image_url'],
                'video_id':d['video_id'],
            }
            print(ret1)

            #break


t = ttspider('subv_entertainment',20)

t.start()
t.exec()



# from urllib.parse import urlparse
# import binascii
#
# def right_shift(val, n):
#     return val >> n if val >= 0 else (val + 0x100000000) >> n
# import random
# r = str(random.random())[2:]
# vid = '185e6cd90312486dbd4a99ddf66dd4c1'
# url = 'https://ib.365yg.com/video/urls/v/1/toutiao/mp4/%s' % vid
# ###https://ib.365yg.com/video/urls/v/1/toutiao/mp4/4d0b1c54cead42e4ab56c1ea821c2a39?r=27247661144819957&s=805232848&callback=tt_playerooswk
# r = '27247661144819957'
# n = urlparse(url).path + '?r=' + r
# n = n.encode('utf-8')
# print(n)
# c = binascii.crc32(n)
# s = right_shift(c, 0)
# print('-------------',c)
# url = 'https://ib.365yg.com/video/urls/v/1/toutiao/mp4/c0d0bbbcc22d48b4ae4327a35198a184?r=%s&s=%s'%(r,s)
# res = requests.get(url)
# print(res.json())

