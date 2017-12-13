from PyQt5.QtCore import pyqtSignal,QThread
import requests
from PyQt5.QtGui import QPixmap,QColor
class download(QThread):
    statusSignal = pyqtSignal(dict) #1('status':成功,rowid:id}

    def __init__(self,que):
        super().__init__()
        self.que = que
    def run(self):
        self.downloadVideo(self.que)

    def downloadVideo(self,que):
        while not que.empty():
            try:
                q1 = que.get()
                url = q1[0]
                filename = q1[1]
                rowid = q1[2]
                self.statusSignal.emit({'status':'下载中',
                                        'rowid':rowid})
                res = requests.get(url)
                content = res.content
                with open(filename, 'wb') as f:
                    f.write(content)
                self.statusSignal.emit({'status':'成功',
                                        'rowid':rowid})
            except Exception as e:
                print(e)
                self.statusSignal.emit({'status':'失败',
                                        'rowid':rowid})