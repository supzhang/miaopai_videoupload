# -*- coding: UTF-8 -*-
#打包命令nuitka --windows-disable-console --recurse-all --output-dir=D:\output --python-version=3.6 --icon=image\ico.ico mp_main.py
from PyQt5.QtWidgets import QApplication,QFileDialog,QTableWidgetItem,QLabel,QMessageBox

from PyQt5.QtCore import pyqtSignal,Qt,QTextCodec,QModelIndex
from videos_get.getVideo_main import video_main  #单独的网上视频获取器
from mp_que import que
from get_conf import getConf,writeConf
from reg_Update import update
import sys,time,os,re
from PyQt5.QtGui import QPixmap,QColor
from mp_thread import mp_thread,loginThread,getVideothread
from ui import form
import requests
from requests.adapters import HTTPAdapter
import webbrowser

class myui(form):
    txtSignal = pyqtSignal(list)
    deleteSignal = pyqtSignal(str)
    msgboxSignal = pyqtSignal(list)
    def __init__(self):
        super().__init__()
        ####################检测新版本########################
        version = '20171214'   #本软件版本
        self.setWindowTitle('秒拍视频上传工具 ' + version + '  FROM zzy Q:1728570648 仅供测试，勿用于非法活动！')
        u = update(version)
        u.hasNewVersion.connect(self.hasNewVer)  # [是否有新版本,版本名,版本路径]
        u.start()
        #######################获取配置文件及解析配置，解析用户名密码################
        self.s1 = '==|=='  #用户之间的分割
        self.s2 = '=|='  #用户名密码的分割
        self.isReg = 1  #初始化为已经注册
        self.conf = getConf() #
        self.conf.update({'version':version})
        self.retList = self.unpack_users()   #获取已经保存的用户列表
        self.msgboxSignal.connect(self.messagebox)
        self.btn_login.clicked.connect(self.login)  #登陆功能
        self.upload.clicked.connect(self.mutiThread)  #启动线程调度
        self.btn_stopThread.clicked.connect(self.getStatusTableThreads)

        self.category.currentIndexChanged.connect(self.writecat)
        self.seldia.clicked.connect(self.getfilename)
        self.btn_hideuser.clicked.connect(self.hideUsers)
        self.btn_getlist.clicked.connect(self.getList)
        self.btn_del.clicked.connect(self.deleteVideo)
        self.btn_del_status.clicked.connect(self.del_status)
        self.txtSignal.connect(self.messagebox)
        self.deleteSignal.connect(self.deleteVideo)
        self.lab_help.linkActivated.connect(self.help)
        self.txt_user.currentTextChanged.connect(self.userChange)
        self.selThread.currentIndexChanged.connect(self.selThreadChange)
        self.btn_getVideo.clicked.connect(self.getVideo)
        #self.picTipSignal.connect(self.picTip)
        self.okTable.cellClicked.connect(self.video_play)
        self.btn_getusers.clicked.connect(self.get_userlist)
        self.txt_userlist.cellDoubleClicked.connect(self.adduser)
        ###### self.okTable.  初始化上传前各按钮不可用
        self.upload.setDisabled(True)  #上传禁用
        self.seldia.setDisabled(True)  # 选择上传文件禁用
        self.btn_getlist.setDisabled(True)  #获取用户列表禁用
        self.btn_del.setDisabled(True)  #删除禁用
        self.hideuser = False #用户列表初始隐藏
        self.maxrows = 20 #视频列表最大数量
        self.display_help = False #是否显示帮助

        self.table_status.setHorizontalHeaderLabels(['状态','标题','进度条','日志','用户名'])
        self.finishTable.setHorizontalHeaderLabels(['标题', '信息', '帐号','文件名'])
        self.okTable.setHorizontalHeaderLabels(['封面','视频信息'])
        self.isLogin = 0
        self.headers = {
            'user-agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
            'Cache-Control': 'max-age=0',
            'X-Requested-With':'XMLHttpRequest',
            'Accept': 'application/json, text/plain, */*',
            'Upgrade-Insecure-Requests': '1',
            'Accept-Encoding': 'gzip, deflate',
            'Referer':'http://creator.miaopai.com/login',
            'Accept-Language': 'zh-CN,zh;q=0.8',
        }
        self.readHelp()  #读取帮助文件
        self.isLogin = False

        self.txt_info.setReadOnly(True)
        self.threadno = 0 #线程号 传递到子线程，返回数据时需要提供
        self.status_color = {'成功':QColor('green'),
                             '失败':QColor('red'),
                             '运行中':QColor('blue')
                             }

        self.topics.setText(self.conf['topics'])
        self.custom_tag.setText(self.conf['custom_tag'])

        #####线程控制#######
        self.threads = []  #存储线程变量  [[thread1,tag],[thread2,tag]]
        self.isFirstThreads = True   ##保证系统中只有一个调度线程
    def mutiThread(self): #选择多文件同时上传
        if self.isReg == 0:
            QMessageBox.information(self, '提示', '此版本已经过期，请下载新版本使用！')
            #self.txtSignal.emit(['警告','本版本已经过期，请下载新版本使用:https://pan.baidu.com/s/1eRR2PSA'])
            return
        self.upload.setDisabled(True)
        if len(self.paths) == 0:
            return
        for path in self.paths:
            self.runthread(path[0],path[1]) #路径名，路径标识
        maxThread = int(self.selThread.currentText())  #获取最大线程数
        if self.isFirstThreads == True:  #如果是第一次启动调度器，传输所有线程
            self.q = que(self.threads,maxThread)
            self.q.start()
            self.isFirstThreads = False

            self.q.exec()

        else:
            self.q.threads = self.threads
    def login(self):
       #登陆的请求线程
        if self.isLogin == 1:
            self.btn_login.setText('登陆')
            self.seldia.setDisabled(True)
            self.upload.setDisabled(True)
            self.shutThread(0)  #退出则关闭所有上传线程
            self.btn_del.setDisabled(True)
            self.btn_getlist.setDisabled(True)
            del self.sess
            self.isLogin = 0
        else:
            self.phone = self.txt_user.currentText()
            pwd = self.txt_pass.text()
            if len(self.phone.strip()) < 5 or len(pwd.strip()) < 5:
                self.msgboxSignal.emit(['输入错误','请输入正确的用户名密码'])
                return
            self.sess = requests.session()
            self.sess.mount('http://', HTTPAdapter(max_retries=3))
            login_url = 'http://creator.miaopai.com/auth/login'
            data = {
                'phone':self.phone,
                'pwd':pwd,
                'remember':'true',
                'type':'0'}

            self.login_sess = loginThread(self.sess,self,login_url,self.headers,data,self.conf)
            self.login_sess.start()
            self.btn_login.setText('正在登陆')
            self.btn_login.setDisabled(True)
            self.seldia.setDisabled(False)
            self.pack_users(self.phone,pwd)


    ####选择需要上传的文件#####
    def getfilename(self):
        try:
            if os.path.exists(self.conf['video_path']):
                path = self.conf['video_path']
            else:
                path = os.getcwd()
        except Exception as e:
            print(e)

        file = QFileDialog.getOpenFileNames(self,
                                    "请选择需要上传的文件",
                                    path,
                                    "所有类型(*.mp4;*.mov;*.3gp;*.wmv;*.avi);;MP4(*.mp4);;MOV(*.mov);;3gp(*.3gp);;avi(*.avi);;wmv(*.wmv)")
        paths = file[0]
        file_no = len(paths)
        try:
            if file_no != 0:

                self.conf['video_path'] = os.path.dirname(paths[0])
                writeConf(self.conf)
                self.upload.setDisabled(False)
                self.txt_path.setText('共选择了 ' + str(file_no) +' 个文件')
                filenames = []
                paths_l = []
                for path in paths:
                    filename = os.path.basename(path)
                    filenames.append(filename)
                    shortname = filename if len(filename) <= 15 else filename[:15] + '...'
                    item_txt = ['未开始', shortname, '', '未开始', self.phone,str(self.threadno)]

                    paths_l.append([path,self.threadno])
                    col = 0
                    self.table_status.insertRow(self.threadno)
                    for txt in item_txt:
                        if len(txt) != 0:
                            item = QTableWidgetItem(txt)
                            self.table_status.setItem(self.threadno, col, item)
                        col += 1
                    self.table_status.item(self.threadno, 1).setToolTip(filename)
                    self.threadno += 1

                filenames = '\n'.join(filenames)
                self.txt_path.setToolTip(filenames)

            elif len(self.paths) != 0:
                self.upload.setDisabled(False)
                paths_l = self.paths
        except Exception as e:
            print(e)
        try:
            self.paths = paths_l
        except Exception as e:
            paths_l = []
            print(e)

        return paths_l
    def get_userlist(self):
        path = self.conf['user_list_path']
        if not os.path.exists(path):
            path = os.getcwd()
        file = QFileDialog.getOpenFileName(self,
                                           '选择帐号列表，帐号与密码使用“----”分割',
                                           path,
                                           '文本文件(*.txt)')
        if len(file[0]) < 5:
            return
        self.conf['user_list_path'] = os.path.dirname(file[0])
        writeConf(self.conf)
        if self.hideuser == False:
            self.hideUsers()
        with open(file[0],'r',errors = 'ignore') as f:
            lines = f.readlines()
            n = 0
            rows = self.txt_userlist.rowCount()
            for x in range(rows):
                self.txt_userlist.removeRow(0)

            for line in lines:

                try:
                    line = line.replace('\n','').replace(' ','')
                    if '----' in line:
                        line_spre = line.split('----')

                        if len(line_spre) > 1:

                            user = line_spre[0]
                            pwd = line_spre[1]
                            item_user = QTableWidgetItem(user)
                            item_pwd = QTableWidgetItem(pwd)
                            self.txt_userlist.insertRow(n)
                            self.txt_userlist.setItem(n,0,item_user)
                            self.txt_userlist.setItem(n,2,item_pwd)
                            n += 1

                except Exception as e:
                    print(e)
                    continue

    def txtprint(self,txt):
        t = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())
        tip = t + '\t' + self.phone + '\t' + txt
        self.txt_info.append(tip)
    def runthread (self,path,threadno):
        #self.newThreads = [] ##初始化新增加的线程变量

        try:
            file_name = os.path.basename(path)
            ftitle_ = self.ftitle.text()
            title_ = self.title.text()
            if len(ftitle_.strip()) == 0:
                ftitle_ = re.sub(r'\..{1,4}$', '', file_name)
                #self.txtSignal.emit('标题为空自动调用文件名为标题名称！')
            if len(ftitle_) < 8 or len(ftitle_)>30:
                #self.msgboxSignal.emit(['错误',file_name + ' 标题不能少于8字或多于30字'])
                titleok = False
            else:
                titleok = True




            custom_tag_ = self.custom_tag.text().replace('，',',').strip()
            topics_ = self.topics.text().replace('，',',').strip()
            isChange = 0
            #处理暂存标签及话题
            if len(custom_tag_) != 0:
                self.conf['custom_tag'] = custom_tag_
                isChange = 1
            if len(custom_tag_) != 0:
                self.conf['topics'] = topics_
                isChange = 1
            if isChange == 1:
                writeConf(self.conf)


            category_ = self.getCategory()

            orintal_ = 1 if self.orintal.isChecked() else 0
            serial_ = 1 if self.serial.isChecked() else 0
            hasad_ = 1 if self.hasad.isChecked() else 0
            if titleok == True:
                status = '等待'
                current_status = '等待完成前面的任务'
            else:
                status = '失败'
                current_status = '标题不能少于8字或多于30字'

            # print(self.category_)
            info = {
                'phone':self.phone,
                'filename':path,
                'ftitle':ftitle_,
                'title':title_,
                'custom_tag':custom_tag_,
                'topics':topics_,
                'category':category_,
                'orintal':orintal_,
                'serial':serial_,
                'hasad':hasad_,
            }

            shorttitle = ftitle_ if len(ftitle_) < 15 else ftitle_[:15] + '...'
            item_txt = [status,shorttitle,'',current_status,self.phone]
            col = 0
            for txt in item_txt:
                if len(txt) != 0:
                    item = QTableWidgetItem(txt)
                    self.table_status.setItem(threadno,col,item)
                    if status == '失败':
                        self.table_status.item(threadno, 0).setBackground(self.status_color['失败'])

                col += 1
            self.table_status.item(threadno, 1).setToolTip(ftitle_)
            if titleok == False:
                return
            self.t = mp_thread(self.sess, path, info, threadno)
            self.t.txtSignal.connect(self.txtprint)
            self.t.finishSignal.connect(self.finishMethod)
            self.t.finishOkSignal.connect(self.getList)
            self.t.statusSignal.connect(self.statusChangem)
            self.t.setTerminationEnabled(True)
            v = [self.t,threadno] #线程，线程标识
            self.threads.append(v)
            # if self.isFirstThreads == False:
            #     self.newThreads.append(v)

        except Exception as e:
            print(e)

    def getCategory(self):
        txt = self.category.currentText()
        for t in self.l_cat:
            if t['name'] == txt:
                id = t['id']
                break
        return id

    def finishMethod(self,msg):
        l = msg[1]
        print(l)
        currentRow = self.finishTable.rowCount()
        self.finishTable.setRowCount(currentRow + 1)
        coln = 0
        for col in [1,3,0,2]: 
            newItem = QTableWidgetItem(l[col])
            newItem.setFlags(Qt.ItemIsEditable)
            self.finishTable.setItem(currentRow, coln, newItem)
            coln += 1
        self.finishTable.resizeColumnsToContents()
        if msg[0] == 1:
            for l in range(self.txt_userlist.rowCount()):
                if self.txt_userlist.item(l, 0).text() == msg[1][0]:
                    try:
                         previous_n = self.txt_userlist.item(l, 1).text()
                    except Exception as e:
                        previous_n = '0'
                    
                    n = int(previous_n)  if previous_n else 0
                    item = QTableWidgetItem(str(n + 1))
                    self.txt_userlist.setItem(l, 1, item)
                    break
            
    def shutThread(self,flags):  #控制所有线程的关闭(单线程关闭使用线程列表[线程1,线程2,线程3.....],，所有关闭使用 0
        closedTrhead = 0
        if flags == 0:
            try:
                self.q.terminate() #关闭调度线程
                self.q.exit()

                needShuts = self.threads
                self.isFirstThreads = True
                print('关闭调度---------------------')
            except:
                needShuts = self.threads
                pass
        else:
            needShuts = flags
        if len(needShuts) == 0:
            return
        l = self.table_status.rowCount()
        print(len(needShuts))
        for t in needShuts:
            try:

                for x in range(l):
                    status = self.table_status.item(x, 0).text()
                    threadTag = int(self.table_status.item(x, 5).text())
                    if t[1] == threadTag:
                        item = QTableWidgetItem('终止')
                        self.table_status.setItem(x, 0, item)
                        break
                t[0].terminate()
                t[0].exit()
                closedTrhead += 1
            except Exception as e:
                print(e)
                pass

        for tt in needShuts:
            self.threads.remove(tt)

        if closedTrhead > 0:
            self.txtSignal.emit(['提示','共有 ' + str(closedTrhead) + '个任务已经被停止'])



    def getList(self,no): #获取视频列表
        try:
            time.sleep(1)
            self.getlist_disable(1)
            self.t2 = getVideothread(self.sess,self.headers,no)

            self.t2.getListSignal.connect(self.addList)
            self.t2.getlistDisableSignal.connect(self.getlist_disable)
            self.t2.start()
        except Exception as e:
            print(e)
    def addList(self,json):
        lineheight = 80
        if json['code'] == 200:
            self.video_no = json['data']['total']
            self.allVideosNo.setText('本帐号共有视频数：' + str(self.video_no))
            video_list = json['data']['list']
            self.btn_del.setDisabled(False)
            self.maxrows = self.maxrows if self.maxrows <= len(video_list) else len(video_list)
            # if len(video_list) == 1:
            #     self.okTable.insertRow(1)
            # else:
            self.okTable.setRowCount(self.maxrows)
            time.sleep(0.2)
            newRow = 0
            for v in video_list:
                self.okTable.setRowHeight(newRow, lineheight)
                scid = v['scid']
                title = v['title']
                createtime = v['createtime']
                ftitle = v['desc']
                read = v['vcnt']
                img = v['cover']
                video_url = v['video_url']
                video_width = v['weight']
                video_height = v['height']
                txt = title + '\n' + createtime + '\n' + '已看人数：' + str(read)

                item1 = QTableWidgetItem(txt)
                self.okTable.setItem(newRow, 1, item1)

                scid_item = QTableWidgetItem(scid)
                self.okTable.setItem(newRow, 2, scid_item)
                self.getpic(newRow, 0, img)
                item_video_url = QTableWidgetItem(video_url)
                self.okTable.setItem(newRow, 3, item_video_url)
                item_video_width = QTableWidgetItem(str(video_width))
                self.okTable.setItem(newRow, 4, item_video_width)
                item_video_height = QTableWidgetItem(str(video_height))
                self.okTable.setItem(newRow, 5, item_video_height)

                newRow += 1
                if newRow == self.maxrows:
                    break
            self.btn_getlist.setDisabled(False)


    def getpic(self,row,col,img):
        try:
            #img = requests.get(cover).content
            imgLab = QLabel()
            pixmap = QPixmap()
            pixmap.loadFromData(img)

            imgLab.setPixmap(pixmap)
            imgLab.setMaximumHeight(80)
            imgLab.setMaximumWidth(120)
            imgLab.setScaledContents(True)

        except Exception as e:
            print(e)

        self.okTable.setCellWidget(row,col,imgLab)


    def deleteVideo(self): #删除视频
        row = self.okTable.currentRow()
        if row == None:
            self.txtSignal.emit(['提示','请先选择需要删除的视频'])
        else:
            scid = self.okTable.item(row,2).text()

            url_api = 'http://creator.miaopai.com/video/delete'
            data = {
                'scid':scid
            }
            res = self.sess.post(url_api,data = data,headers = self.headers)
            json = res.json()

            print(json['code'])
            if json['code'] == 200:
                self.okTable.removeRow(row)
                self.video_no = self.video_no - 1
                self.allVideosNo.setText('本帐号共有视频个数：' + str(self.video_no))
                #self.txtSignal.emit('删除视频成功')
                self.msgboxSignal.emit(['删除视频','删除成功！'])
            else:
                self.txtSignal.emit(['提示','删除失败！'+ json['msg']])
    def video_play(self,row,col):
        if col == 0:
            url = self.okTable.item(row,3).text()
            width = self.okTable.item(row, 4).text()
            height = self.okTable.item(row, 5).text()
            webbrowser.open(url)
    def adduser(self,row,col):
        user = self.txt_userlist.item(row,0).text()
        pwd = self.txt_userlist.item(row,2).text()
        self.txt_user.insertItem(self.usersCount, user)
        self.txt_user.setCurrentIndex(self.usersCount)
        self.usersCount += 1
        self.txt_pass.setText(pwd)
        if self.isLogin == 1:   #如果已经登陆，先退出
            self.login()
        self.login()
    #####更新目前各上传线程的状态##############
    def statusChangem(self,info):#线程序号，状态，实时状态，提示
        threadno = info[0]
        status = info[1]
        current_status = info[2]
        tips = info[3]
        item_status = QTableWidgetItem(status)
        self.table_status.setItem(threadno,0,item_status)
        self.table_status.item(threadno,0).setBackground(self.status_color[status])
        item_current_status = QTableWidgetItem(current_status)
        self.table_status.setItem(threadno,3, item_current_status)
        self.table_status.item(threadno,3).setToolTip(tips)
    ######删除已经上传的视频#######
    def del_status(self):
        row = self.table_status.currentRow()
        self.table_status.removeRow(row)
    #####获取视频列表的按钮不可用开关######
    def getlist_disable(self,d):
        if d ==1:
            self.btn_getlist.setDisabled(True)
        else:
            self.btn_getlist.setDisabled(False)
    #####弹窗API，msg = [标题,信息],只有OK按钮
    def messagebox(self,msg):
        try:
            QMessageBox.information(self,msg[0],msg[1])
        except Exception as e:
            print(e)
    ####将读取的默认记录写入界面####
    def writecat(self,index):
        self.conf['sort_index'] = str(index)
        writeConf(self.conf)
    def hideUsers(self):
        if self.hideuser == False:
            self.mainv.setStretchFactor(self.main_v2, 2.7)
            self.txt_userlist.setVisible(True)
            self.hideuser = True
            self.btn_hideuser.setText('隐藏用户栏')
        else:
            self.mainv.setStretchFactor(self.main_v2, 0)
            self.txt_userlist.setVisible(False)
            self.hideuser = False
            self.btn_hideuser.setText('显示用户栏')

    def unpack_users(self):
        retlist = []
        self.usersCount = 0
        users = self.conf['user']
        users_list = users.split(self.s1) if self.s1 in users else [users]
        for user in users_list:
            if self.s2 in user:
                up = user.split(self.s2)
                phone = up[0]
                pwd = up[1]
                self.txt_user.insertItem(self.usersCount,phone)
                retlist.append([phone,pwd])
                self.usersCount += 1
            else:
                continue
        if len(retlist) > 0:
            self.txt_user.setCurrentIndex(0)
            self.txt_pass.setText(retlist[0][1])
        return retlist
    def pack_users(self,user,pwd):
        hasUser = 0
        for x in self.retList:
            if user == x[0]:
                hasUser = 1
                break
        if hasUser == 0:
            
            txt = user + self.s2 + pwd
            self.conf['user'] = self.s1.join([self.conf['user'], txt])
            writeConf(self.conf)
    def userChange(self,u):
        pwd = ''
        for user in self.retList:
            if user[0] == u:
                pwd = user[1]
        self.txt_pass.setText(pwd)

    def hasNewVer(self,info):#[是否有新版本,版本名,版本路径,是否过期]
        print(info)
        if info[0] == 1:
            t = QMessageBox.information(self,'提醒','已经有新版本' + info[1] + '\n，是否下载？',QMessageBox.Yes|QMessageBox.No,QMessageBox.Yes)
            if t == QMessageBox.Yes:
                webbrowser.open(info[2])
        try:
            if info[3] == 0: #检查是版本是否过期
                self.isReg = 0
                #QMessageBox.information(self,'提示','此版本已经过期，请下载新版本使用！')
        except Exception as e:
            print(e)
    def getStatusTableThreads(self):
        threadTags = set() #暂存 需要关闭线程的标识
        neetStopThreads = []
        indexs = self.table_status.selectedIndexes()
        indexsLen = len(indexs)
        try:
            if indexsLen == 0:
                self.msgboxSignal.emit(['提醒','请先选择需要停止的线程'])
            elif len(self.threads) == 0:
                self.msgboxSignal.emit(['提醒','没有运行的线程'])
            else:
                for currentIndex in indexs:  #遍历所选行的线程标识，
                    row = self.table_status.itemFromIndex(currentIndex).row()
                    itemInt = int(self.table_status.item(row,5).text())
                    threadTags.add(itemInt)
                if len(threadTags) == 0:
                    self.msgboxSignal(['提醒','您选择的文件均未开始运行'])
                    return
                for x in self.threads:  #查找每个标识对应的线程
                    #print(x[1],threadTags)
                    if x[1] in threadTags:
                        neetStopThreads.append(x)
                        break

                self.shutThread(neetStopThreads)
        except Exception as e:
            print(e)

    def selThreadChange(self,index):  #线程数量改动时更改已经设置的线程数
        try:
            self.q.maxthread = index + 1
            print('sesstion has been changed to ' ,self.q.maxthread)
        except Exception as e:
            print(e)

    def getVideo(self):  #获取网上视频的界面
        try:
            t = video_main(self.conf)
            t.getVideoUi.exec_()

        except Exception as e:
            print(e)









if __name__ == '__main__':
    app = QApplication(sys.argv)
    t = myui()
    sys.exit(app.exec_())
