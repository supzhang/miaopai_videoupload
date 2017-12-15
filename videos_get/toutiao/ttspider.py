#-*- coding:utf-8 -*-
#用于获取头条的视频信息
import requests
import re
import time
import random
import binascii
import base64
from PyQt5.QtCore import QThread,pyqtSignal

class ttspider(QThread):
    finalInfo = pyqtSignal(dict)
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
            res = self.sess.get(url, headers=self.headers,verify = False)
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
        try:
            abstract=d['abstract']
        except Exception as e:
            abstract = ''
        for d in self.rett:
            ret1 = {
                'source':'今日头条',
                'title':d['title'],
                'abstract':abstract,
                'media_url':self.mainurl + d['media_url'],
                'source_url':self.mainurl + d['source_url'],
                'video_play_count':d['video_play_count'],
                'publish_time':d['behot_time'],
                'avatar_url':d['image_url'],
                'video_id':d['video_id'],
                'time_period':0,
            }
            try:
                final = self.get_video_url(ret1)
                self.ret = final
                print(final)
                self.finalInfo.emit(final)


            except Exception as e:
                print(e)

    def get_video_url(self,info):
        r = str(random.random())[2:]
        r_1 = ('/video/urls/v/1/toutiao/mp4/' + info['video_id'] + '?r=' + r)
        r_bin  =r_1.encode('utf-8')
        s = binascii.crc32(r_bin)
        s = self.right_shift(s,0)
        url = 'https://ib.365yg.com'+ r_1 + '&s=' + str(s)
        try:
            real_urls = self.get_url_real_url(url)
            info['video_url'] = real_urls['video_url']
            info['video_type'] = real_urls['video_type']
            info['video_def'] = real_urls['video_def']
        except Exception as e:
            print('获取视频真实地址：',e)
        return info
    def get_url_real_url(self,url):   #获取真实视频地址
        res = requests.get(url,headers = self.headers,verify = False)
        url_json = res.json()
        videolist = url_json['data']['video_list']
        keys = list(videolist.keys())
        videoinfo = videolist[keys[-1:][0]]
        url = base64.b64decode(videoinfo['main_url']).decode('utf-8')

        ret = {
                    'video_url' : url,
                    'video_type' : videoinfo['vtype'],
                    'video_def' : videoinfo['definition'],
                }
        return ret

    ##获取右移后的数据
    def right_shift(self,val, n):
        return val >> n if val >= 0 else (val + 0x100000000) >> n


# t = ttspider('subv_funny',20)
# t.start()
# t.exec()



# categories = {'搞笑':'subv_funny',
#               '音乐':'subv_voice',
#               '推荐':'video_new',
#               '开眼':'subv_broaden_view',
#               '原创':'subv_boutique',
#               '游戏':'subv_game',
#               '呆盟':'subv_cute',
#               '娱乐':'subv_entertainment',
#               '影视':'subv_movie',
#               '生活':'subv_life',
#               '小品':'subv_comedy',
#               '社会':'subv_society',
#               }
# hotvideo_url = 'https://www.ixigua.com/api/pc/hot_video/'  #热视频
