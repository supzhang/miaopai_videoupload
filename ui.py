# -*- coding: UTF-8 -*-

from PyQt5.QtWidgets import QDialog, QHBoxLayout,QVBoxLayout,QPushButton,QLineEdit,QTextEdit,QLabel,QComboBox,QCheckBox,QTableWidget,QWidget,QAbstractItemView,QHeaderView
from PyQt5.QtGui import QIcon,QPixmap



class form(QWidget):
    def __init__(self):
        super().__init__()
        self.setupUI()
    def setupUI(self):

        pixmap = QPixmap(r'image\ico.ico')
        titleIco = QIcon(pixmap)
        self.setWindowIcon(titleIco)
        self.setWindowTitle('秒拍数据上传 171205 from zzy Q:1728570648 仅供测试，勿用于非法活动！')

        self.main_v1 = QVBoxLayout()
        self.main_v2 = QVBoxLayout()

        self.main_v3 = QVBoxLayout()
        self.main_v4 = QVBoxLayout()
        self.hideitem = QLabel()

        self.mainv = QHBoxLayout()
        self.mainv.addLayout(self.main_v1)
        self.mainv.addLayout(self.main_v2)
        self.mainv.addLayout(self.main_v3)
        self.mainv.addLayout(self.main_v4)

        # self.view = QGraphicsView()
        # self.main_v4.addWidget(self.view)


        self.mainv.setStretchFactor(self.main_v1,6)

        self.mainv.setStretchFactor(self.main_v2,0)
        self.mainv.setStretchFactor(self.main_v3,5)


        lab_user = QLabel('用户名:',self)
        self.txt_user = QLineEdit('',self)
        lab_pass = QLabel('密码:',self)
        self.txt_pass = QLineEdit('',self)
        self.txt_userlist = QTableWidget(0,3)
        self.txt_userlist.setVisible(False)
        self.txt_userlist.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.txt_userlist.setColumnHidden(2,True)
        self.txt_userlist.setHorizontalHeaderLabels(["用户名",'本次已传'])
        #userlist_tip = QToolTip('双击帐号可直接登陆，但会停止原来的上传')
        self.txt_userlist.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.txt_userlist.setSelectionMode(QAbstractItemView.SingleSelection)
        self.txt_userlist.setToolTip('双击停止正在进行的上传，也可直接登陆')
        self.txt_info = QTextEdit('',self)
        self.txt_info.setVisible(False)
        self.table_status = QTableWidget(0,5) #状态【成功、失败、未开始、运行中、等待】，标题，，进度条，实时状态，用户名，
        self.table_status.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table_status.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table_status.setAlternatingRowColors(True)
        self.table_status.setMaximumWidth(900)
        self.table_status.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_status.horizontalHeader().setSectionResizeMode(3,QHeaderView.ResizeToContents)
        self.table_status.horizontalHeader().setSectionResizeMode(1,QHeaderView.ResizeToContents)

        self.table_status.setColumnHidden(2,True)
        self.btn_login = QPushButton('登陆', self)
        self.btn_getusers = QPushButton('载入用户列表',self)
        self.btn_hideuser = QPushButton('显示用户栏',self)

        self.seldia = QPushButton('选择上传文件',self)
        self.txt_path = QLabel('',self)

        self.txt_ftitle = QLabel('视频标题：',self)
        self.ftitle = QLineEdit('',self)
        self.txt_title = QLabel('描    述：',self)
        self.title = QLineEdit('',self)
        self.txt_category = QLabel('分类：',self)
        # l = ['1','2','3']
        self.category = QComboBox()

        self.category.insertItem(0,"登陆后选择分类")
        self.txt_custom_tag = QLabel('标签：')
        self.custom_tag = QLineEdit('',self)
        self.txt_topics = QLabel('话    题：')
        self.topics = QLineEdit('',self)

        self.hasad = QCheckBox('含有广告',self)
        self.orintal = QCheckBox('原创内容',self)
        self.serial = QCheckBox('连载内容',self)
        self.upload = QPushButton('上传',self)
        self.btn_del_status = QPushButton('删除记录',self)
        self.btn_del_status.setVisible(False)
        #self.items = QLabel()

        #self.lab1 = QLabel('本次完成的上传',self)
        self.finishTable = QTableWidget(0,4)


        #self.lab2 = QLabel('已经上传的视频',self)
        self.btn_del =QPushButton('删除视频',self)
        self.allVideosNo = QLabel('',self)  #视频总数
        self.btn_getlist = QPushButton('获取视频列表（前20条）',self)
        self.okTable = QTableWidget(0,6)
        self.okTable.setAlternatingRowColors(True)
        self.okTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.okTable.horizontalHeader().setSectionResizeMode(0,QHeaderView.ResizeToContents)
        # self.okTable.horizontalHeader().setSectionResizeMode(1,QHeaderView.ResizeToContents)
        self.okTable.setSelectionMode(QAbstractItemView.SingleSelection)
        self.okTable.setEditTriggers(QAbstractItemView.NoEditTriggers)


        self.main_v3_h1 = QHBoxLayout()
        self.main_v3_h1.addWidget(self.btn_del)
        self.main_v3_h1.addWidget(self.btn_getlist)
        self.main_v3_h1.addWidget(self.allVideosNo)
        self.main_v3.addLayout(self.main_v3_h1)
        self.main_v3.addWidget(self.okTable)
        self.okTable.setColumnHidden(2,True)
        self.okTable.setColumnHidden(3,True)
        self.okTable.setColumnHidden(4,True)
        self.okTable.setColumnHidden(5,True)
        # self.okTable.setColumnHidden(1,True)

       # self.okTable.horizontalHeader().setSectionResizeMode(QHeaderView.setSectionResizeMode())

        # self.main_v2.addWidget(self.lab1)
        # self.main_v2.addWidget(self.finishTable)
        self.main_v2.addWidget(self.txt_userlist)

        hbox_loginfo = QHBoxLayout()
        hbox_path = QHBoxLayout()
        vbox_loginfo = QVBoxLayout()
        hbox3 = QHBoxLayout()
        hbox4 = QHBoxLayout()
        hbox5 = QHBoxLayout()
        hbox6 = QHBoxLayout()
        vbox1 = QHBoxLayout()

        #vbox1.addWidget(self.txt_userlist)
        vbox1.addWidget(self.table_status)#txt_info)
        #vbox1.setStretchFactor(self.txt_userlist,4)
        vbox1.setStretchFactor(self.txt_info,6)

        hbox3.addWidget(self.txt_ftitle)
        hbox3.addWidget(self.ftitle)
        hbox3.addWidget(self.txt_category)
        hbox3.addWidget(self.category)

        hbox4.addWidget(self.txt_title)
        hbox4.addWidget(self.title)

        hbox5.addWidget(self.txt_topics)
        hbox5.addWidget(self.topics)
        hbox5.addWidget(self.txt_custom_tag)
        hbox5.addWidget(self.custom_tag)

        hbox6.addWidget(self.hasad)
        hbox6.addWidget(self.orintal)
        hbox6.addWidget(self.serial)
        hbox6.addWidget(self.upload)
        hbox6.addWidget(self.btn_del_status)

        hbox_loginfo.addWidget(lab_user)
        hbox_loginfo.addWidget(self.txt_user)
        hbox_loginfo.addWidget(lab_pass)
        hbox_loginfo.addWidget(self.txt_pass)
        hbox_loginfo.addWidget(self.btn_login)
        hbox_loginfo.addWidget(self.btn_getusers)
        hbox_loginfo.addWidget(self.btn_hideuser)


        #hbox_loginfo.addWidget(self.upload)
        self.resize(1100,600)
        hbox_path.addWidget(self.seldia)
        hbox_path.addWidget(self.txt_path)
        hbox_path.setStretchFactor(self.seldia,4)
        hbox_path.setStretchFactor(self.txt_path,7)

        vbox_loginfo.addLayout(hbox_loginfo)
        vbox_loginfo.addLayout(hbox_path)
        vbox_loginfo.addLayout(hbox3)
        vbox_loginfo.addLayout(hbox4)
        vbox_loginfo.addLayout(hbox5)
        vbox_loginfo.addLayout(hbox6)

        vbox_loginfo.addLayout(vbox1)
        self.mainv.setSizeConstraint(1)
        self.main_v1.addLayout(vbox_loginfo)

        self.setLayout(self.mainv)
        self.show()

#class player_ui(object):
#    def __init__(self, width, height, url):
#        self.width= int(width)
#        self.height  = int(height)
#        self.url = url
#        form = QDialog()
#        self.setupUi(form)
#    def setupUi(self, Form):
#        Form.setObjectName("Form")
#        Form.resize(self.width, self.height)
#        self.webEngineView = QtWebEngineWidgets.QWebEngineView(Form)
#        #self.webEngineView.setGeometry(QtCore.QRect(80, 360, 300, 200))
#        self.webEngineView.setUrl(QtCore.QUrl(self.url))
#        self.webEngineView.setObjectName("webEngineView")
#        self.retranslateUi(Form)
#        QtCore.QMetaObject.connectSlotsByName(Form)
#        Form.show()
#
#    def retranslateUi(self, Form):
#        _translate = QtCore.QCoreApplication.translate
#        Form.setWindowTitle(_translate("Form", "Form"))




