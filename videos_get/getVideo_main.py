from videos_get.Ui_getVideoUi import Ui_getVideoUi
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem,QFileDialog
from PyQt5.QtCore import pyqtSignal
from videos_get.toutiao.ttspider import ttspider
import sys
class video_main(Ui_getVideoUi):
    def __init__(self):
        super().__init__()
        #####初始化界面######
        self.getVideoUi = QtWidgets.QDialog()
        self.setupUi(self.getVideoUi)
        self.getVideoUi.show()
        self.table_videos.setColumnCount(5)
        self.table_videos.setHorizontalHeaderLabels(['选择','来源','浏览量','下载地址','check'])
        self.table_videos.setColumnWidth(0,40)
        self.table_videos.setColumnWidth(1,300)
        self.table_videos.setColumnWidth(2,60)
        self.table_videos.setColumnWidth(3,400)
        self.table_videos.setColumnHidden(4,True)

        self.btn_getvideo.clicked.connect(self.getVideo)
        self.btn_selectSavePath.clicked.connect(self.selectPath)
        self.btn_download.clicked.connect(self.downloadVideo)

        self.categories = {'gaoxiao': 'subv_funny',
                      'yinyue': 'subv_voice',
                      'tuijian': 'video_new',
                      'kaiyan': 'subv_broaden_view',
                      'yuanchuang': 'subv_boutique',
                      'youxi': 'subv_game',
                      'daimeng': 'subv_cute',
                      'yule': 'subv_entertainment',
                      'yingshi': 'subv_movie',
                      'shenghuo': 'subv_life',
                      'xiaopin': 'subv_comedy',
                      'shehui': 'subv_society',
                      }


    def getVideo(self): #获取视频信息

        cats = self.getCheckCat()
        self.threads = []
        for cat in cats:
            self.t1 = ttspider(cat,10)
            self.t1.finalInfo.connect(self.addrows)
            self.threads.append(self.t1)
        for thread in self.threads:
            thread.start()

    def selectPath(self): #获取视频存放位置
        try:
            path = r'c:\\'
            path = QFileDialog.getExistingDirectory(self.getVideoUi,
                                                "请选择文件夹",
                                               )
            self.line_videoSave.setText(path)
        except Exception as e:
            print(e)

    def downloadVideo(self,url,filename):
        res = requests.get(url)
        content = res.content
        with open(filename,'wb') as f:
            f.write(content)
        pass
    def getCheckCat(self):
        checkedCat = []
        if self.check_toutiao.isChecked():
            checkedCat.append(self.categories['tuijian']) if self.tuijian.isChecked() else ''
            checkedCat.append(self.categories['yule']) if self.yule.isChecked() else ''
            checkedCat.append(self.categories['shenghuo']) if self.shenghuo.isChecked() else ''
            checkedCat.append(self.categories['yingshi']) if self.yingshi.isChecked() else ''
            checkedCat.append(self.categories['youxi']) if self.youxi.isChecked() else ''
            checkedCat.append(self.categories['yinyue']) if self.yinyue.isChecked() else ''
            checkedCat.append(self.categories['kaiyan']) if self.kaiyan.isChecked() else ''
            checkedCat.append(self.categories['shehui']) if self.shehui.isChecked() else ''
            print(checkedCat)
        if len(checkedCat) == 0:
            try:
                QtWidgets.QMessageBox.information(self.getVideoUi,'提醒','请先选择来源及分类')
            except Exception as e :
                print(e)
        return checkedCat
    def addrows(self,row):
        print('---------',row)
        colno = 1
        rowsno = self.table_videos.rowCount()
        self.table_videos.setRowCount(rowsno + 1)
        try:
            check_widget = QtWidgets.QCheckBox()
            self.table_videos.setCellWidget(rowsno,0,check_widget)
        except Exception as e:
            print(e)
        try:

            title = row['title']
            url = row['video_url']
            count = row['video_play_count']
            check = ' '
            heads = [title,count,url,check]
            print(heads)
            for head in heads:
                item = QTableWidgetItem(str(head))
                self.table_videos.setItem(rowsno,colno,item)
                colno += 1
        except Exception as e:
            print(e)





if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui = video_main()
    sys.exit(app.exec_())