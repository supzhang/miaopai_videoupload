from videos_get.Ui_getVideoUi import Ui_getVideoUi
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QTableWidgetItem,QFileDialog
from PyQt5.QtCore import pyqtSignal,Qt
from videos_get.toutiao.ttspider import ttspider
from videos_get.downloadThread import download
from multiprocessing import Queue
import webbrowser
from PyQt5.QtGui import QPixmap,QColor,QIcon
import requests
import sys,os
class video_main(Ui_getVideoUi):
    def __init__(self,conf):
        super().__init__()
        #####初始化界面######
        self.getVideoUi = QtWidgets.QDialog()
        self.setupUi(self.getVideoUi)
        self.getVideoUi.show()
        self.conf = conf
        self.getVideoUi.setWindowTitle('热门视频下载器from zzy,' + conf['version'])
        pixmap = QPixmap(r'image/ico_down.png')
        titleIco = QIcon(pixmap)
        self.getVideoUi.setWindowIcon(titleIco)

        self.table_videos.setColumnCount(7)
        self.table_videos.setHorizontalHeaderLabels(['选择','来源','下载','标题','浏览量','下载地址','check'])
        self.table_videos.setColumnWidth(0,20)
        self.table_videos.setColumnWidth(1,60)
        self.table_videos.setColumnWidth(2,60)
        self.table_videos.setColumnWidth(3,300)
        self.table_videos.setColumnWidth(4,60)
        self.table_videos.setColumnWidth(5,350)
        self.table_videos.setColumnHidden(6,True)

        self.btn_getvideo.clicked.connect(self.getVideo)
        self.btn_selectSavePath.clicked.connect(self.selectPath)
        self.btn_download.clicked.connect(self.selectRow)
        self.btn_delall.clicked.connect(self.deleteAll)
        self.btn_delsel.clicked.connect(self.deleteSel)

        self.table_videos.cellClicked.connect(self.playVideo)
        path = self.conf['video_path'] if len(self.conf['video_path']) > 5 else os.getcwd()
        self.line_videoSave.setText(path)

        self.rowid = 0
        self.rowsinfo = []
        self.check_toutiao.setCheckState(Qt.Checked)
        self.tuijian.setCheckState(Qt.Checked)
        self.status_color = {'成功': QColor('green'),
                             '失败': QColor('red'),
                             '等待':QColor('yellow'),
                             '下载中': QColor('blue')
                             }
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
        #print('---------',row)
        row['rowid'] = self.rowid  #此记录的唯一标识
        self.rowsinfo.append(row)
        colno = 1
        rowsno = self.table_videos.rowCount()
        self.table_videos.setRowCount(rowsno + 1)
        try:
            # check_widget = QtWidgets.QCheckBox()
            # self.table_videos.setCellWidget(rowsno,0,check_widget)
            checkItem = QTableWidgetItem()
            checkItem.setCheckState(Qt.Unchecked)
            #checkItem.setFlags(Qt.ItemIsEditable)
            self.table_videos.setItem(rowsno,0,checkItem)
        except Exception as e:
            print(e)
        try:
            source = row['source']
            title = row['title']
            url = row['video_url']
            count = row['video_play_count']
            rowid = row['rowid']
            check = ' '
            heads = [source,'未下载',title,count,url,rowid]
            print(heads)
            for head in heads:
                item = QTableWidgetItem(str(head))
                if colno != 3:
                    item.setFlags(Qt.ItemIsEditable)
                self.table_videos.setItem(rowsno,colno,item)

                colno += 1
            self.rowid += 1
        except Exception as e:
            print(e)

    def playVideo(self,row,col):
        if col == 5:
            item = self.table_videos.item(row,col).text()
            webbrowser.open(item)
    def selectRow(self):
        try:
            rowsno = []
            rows = self.table_videos.rowCount()
            for row in range(rows-1) :
                check = self.table_videos.item(row,0).checkState()
                if check == Qt.Checked:
                    rowsno.append(row)
        except Exception as e:
            print(e)
        try:
            filepath = self.line_videoSave.text()
            if len(filepath.strip()) == 0:
                filepath = os.getcwd()
            que = Queue()
            for row in rowsno:
                rowid = int(self.table_videos.item(row,6).text())
                rowinfo = self.findRowInfo(rowid)
                url = rowinfo['video_url']
                ext = rowinfo['video_type']
                filename = self.table_videos.item(row,3).text()
                pathname = filepath + '\\' + filename + '.' + ext
                item = QTableWidgetItem('等待')

                item.setBackground(self.status_color['等待'])
                item.setFlags(Qt.ItemIsEditable)
                item = self.table_videos.setItem(row,2,item)
                que.put([url, pathname,rowid])
            self.t = download(que)
            self.t.statusSignal.connect(self.changeStatus)
            self.t.start()

        except Exception as e:
            print(e)



    def findRowInfo(self,rowid):
        for rowinfo in self.rowsinfo:
            if rowinfo['rowid'] == rowid:
                return rowinfo
    def changeStatus(self,info):
        try:
            rowid = info['rowid']
            status = info['status']
            rowsno = self.table_videos.rowCount()
            for x in range(rowsno-1):
                currentid = int(self.table_videos.item(x,6).text())
                if currentid == rowid:
                    item = QTableWidgetItem(status)
                    item.setFlags(Qt.ItemIsEditable)
                    item.setBackground(self.status_color[status])
                    self.table_videos.setItem(x,2,item)
        except Exception as e:
            print(e)
    def deleteAll(self):
        self.table_videos.setRowCount(0)
    def deleteSel(self):
        try:
            rowno = self.table_videos.rowCount()
            print('row no',rowno)
            l = range(rowno)[::-1]
            for row in l:
                print(row)
                check = self.table_videos.item(row, 0).checkState()
                if check != Qt.Checked:

                    self.table_videos.removeRow(row)
        except Exception as e:
            print(e)
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui = video_main()
    sys.exit(app.exec_())