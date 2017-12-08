import requests
import time,re
from PyQt5.QtCore import QThread,pyqtSignal
from PyQt5.QtWidgets import QMessageBox

##获取最新版本线程。
class update(QThread):
    hasNewVersion = pyqtSignal(list)
    def __init__(self,version):
        super().__init__()

        t = '20180107'
        self.expire_time = int(time.mktime(time.strptime(t, "%Y%m%d")))  #过期日1516954276
        version_s = int(time.mktime(time.strptime(version, "%Y%m%d")))
        self.version = version_s
    def run(self):
        time.sleep(1)
        self.update()

    def update(self):
        try:
            weburl = 'https://pan.baidu.com/s/1eRR2PSA#list/path=%2F%E5%85%B1%E4%BA%AB'
            url = 'https://pan.baidu.com/share/list?uk=1929770749&shareid=1228615778&order=other&desc=1&showempty=0&web=1&page=1&num=100&dir=%2F%E5%85%B1%E4%BA%AB'
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
            }
            res = requests.get(url, headers=headers)
            res.encoding = 'utf-8'
            json = res.json()
            l = json['list']
            newest = 0
            newpath = ''
            for ll in l:
                path = ll['path']
                d_re = re.search(r'/共享/.+?((20)?1[789][01]\d[0123]\d)',path)

                if d_re:
                    d = d_re.group(1)
                    if len(d) == 6:
                        d = '20'+d
                stamp = int(time.mktime(time.strptime(d, "%Y%m%d")))
                if stamp > newest:
                    newest = stamp
                    newpath = path
            if self.version < newest:
                ret = [1,newpath.replace('/共享/',''),weburl]
            else:
                ret = [0,'没有更的版本发布','']
        except:
            ret = [0,'与更新服务器的网络连接出错','']
        t = self.reg()
        ret.append(t)
        self.hasNewVersion.emit(ret)
    def reg(self):  # 过期时间函数
        try:
            res = requests.head('http://www.baidu.com', timeout=2)
            h = res.headers['Date']
            t = int(time.mktime(time.strptime(h[5:25], "%d %b %Y %H:%M:%S")))
        except:
            t = time.time() + time.timezone
        if t > self.expire_time:
            return 0
        else:
            return 1
