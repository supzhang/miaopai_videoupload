# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:\python_project\miaopai_videoupload\videos_get\getVideoUi.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_getVideoUi(object):
    def setupUi(self, getVideoUi):
        getVideoUi.setObjectName("getVideoUi")
        getVideoUi.resize(881, 654)
        self.tableView = QtWidgets.QTableView(getVideoUi)
        self.tableView.setGeometry(QtCore.QRect(0, 160, 881, 491))
        self.tableView.setObjectName("tableView")
        self.videoCat = QtWidgets.QGroupBox(getVideoUi)
        self.videoCat.setGeometry(QtCore.QRect(0, 70, 881, 41))
        self.videoCat.setObjectName("videoCat")
        self.checkBox_5 = QtWidgets.QCheckBox(self.videoCat)
        self.checkBox_5.setGeometry(QtCore.QRect(10, 20, 71, 16))
        self.checkBox_5.setObjectName("checkBox_5")
        self.videSource = QtWidgets.QGroupBox(getVideoUi)
        self.videSource.setGeometry(QtCore.QRect(0, 10, 881, 41))
        self.videSource.setObjectName("videSource")
        self.checkBox_2 = QtWidgets.QCheckBox(self.videSource)
        self.checkBox_2.setGeometry(QtCore.QRect(10, 20, 71, 16))
        self.checkBox_2.setObjectName("checkBox_2")
        self.btn_getvideo = QtWidgets.QPushButton(getVideoUi)
        self.btn_getvideo.setGeometry(QtCore.QRect(10, 130, 75, 23))
        self.btn_getvideo.setObjectName("btn_getvideo")
        self.pushButton = QtWidgets.QPushButton(getVideoUi)
        self.pushButton.setGeometry(QtCore.QRect(110, 130, 91, 23))
        self.pushButton.setObjectName("btn_")
        self.line_videoSave = QtWidgets.QLineEdit(getVideoUi)
        self.line_videoSave.setGeometry(QtCore.QRect(410, 130, 401, 20))
        self.line_videoSave.setReadOnly(True)
        self.line_videoSave.setPlaceholderText("")
        self.line_videoSave.setObjectName("line_videoSave")
        self.lab_videoPosition = QtWidgets.QLabel(getVideoUi)
        self.lab_videoPosition.setGeometry(QtCore.QRect(320, 130, 81, 20))
        self.lab_videoPosition.setObjectName("lab_videoPosition")
        self.btn_selectSavePath = QtWidgets.QPushButton(getVideoUi)
        self.btn_selectSavePath.setGeometry(QtCore.QRect(820, 130, 31, 23))
        self.btn_selectSavePath.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../image/ico/Arzo_Icons_018.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_selectSavePath.setIcon(icon)
        self.btn_selectSavePath.setIconSize(QtCore.QSize(16, 16))
        self.btn_selectSavePath.setObjectName("btn_selectSavePath")

        self.retranslateUi(getVideoUi)
        QtCore.QMetaObject.connectSlotsByName(getVideoUi)

    def retranslateUi(self, getVideoUi):
        _translate = QtCore.QCoreApplication.translate
        getVideoUi.setWindowTitle(_translate("getVideoUi", "网上视频收集下载器"))
        self.videoCat.setTitle(_translate("getVideoUi", "视频分类"))
        self.checkBox_5.setText(_translate("getVideoUi", "CheckBox"))
        self.videSource.setTitle(_translate("getVideoUi", "视频来源"))
        self.checkBox_2.setText(_translate("getVideoUi", "今日头条"))
        self.btn_getvideo.setText(_translate("getVideoUi", "获取视频"))
        self.pushButton.setText(_translate("getVideoUi", "下载选中视频"))
        self.lab_videoPosition.setText(_translate("getVideoUi", "视频下载位置："))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    getVideoUi = QtWidgets.QDialog()
    ui = Ui_getVideoUi()
    ui.setupUi(getVideoUi)
    getVideoUi.show()
    sys.exit(app.exec_())

