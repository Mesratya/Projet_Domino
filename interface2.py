# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\Yassi\PycharmProjects\ProjetDomino\interface_2.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 587)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.gridwidget = QtWidgets.QWidget(self.centralwidget)
        self.gridwidget.setObjectName("gridwidget")
        self.gridlayout = QtWidgets.QGridLayout(self.gridwidget)
        self.gridlayout.setObjectName("gridlayout")
        self.pushButton_2 = QtWidgets.QPushButton(self.gridwidget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.gridlayout.addWidget(self.pushButton_2, 0, 1, 1, 1)
        self.pushButton_4 = QtWidgets.QPushButton(self.gridwidget)
        self.pushButton_4.setObjectName("pushButton_4")
        self.gridlayout.addWidget(self.pushButton_4, 1, 1, 1, 1)
        self.pushButton = QtWidgets.QPushButton(self.gridwidget)
        self.pushButton.setObjectName("pushButton")
        self.gridlayout.addWidget(self.pushButton, 0, 0, 1, 1)
        self.pushButton_3 = QtWidgets.QPushButton(self.gridwidget)
        self.pushButton_3.setObjectName("pushButton_3")
        self.gridlayout.addWidget(self.pushButton_3, 1, 0, 1, 1)
        self.verticalLayout_3.addWidget(self.gridwidget)
        self.handwidget = QtWidgets.QWidget(self.centralwidget)
        self.handwidget.setObjectName("handwidget")

        self.handlayout = QtWidgets.QHBoxLayout(self.handwidget)
        self.handlayout.setObjectName("handlayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.handlayout.addItem(spacerItem)
        self.widget = QtWidgets.QWidget(self.handwidget)
        self.widget.setObjectName("widget")
        self.d = QtWidgets.QVBoxLayout(self.widget)
        self.d.setObjectName("d")
        self.pushButton_5 = QtWidgets.QPushButton(self.widget)
        self.pushButton_5.setObjectName("pushButton_5")
        self.d.addWidget(self.pushButton_5)
        self.pushButton_6 = QtWidgets.QPushButton(self.widget)
        self.pushButton_6.setObjectName("pushButton_6")
        self.d.addWidget(self.pushButton_6)
        self.handlayout.addWidget(self.widget)
        self.widget_2 = QtWidgets.QWidget(self.handwidget)
        self.widget_2.setObjectName("widget_2")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.widget_2)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.pushButton_7 = QtWidgets.QPushButton(self.widget_2)
        self.pushButton_7.setObjectName("pushButton_7")
        self.verticalLayout_5.addWidget(self.pushButton_7)
        self.pushButton_8 = QtWidgets.QPushButton(self.widget_2)
        self.pushButton_8.setObjectName("pushButton_8")
        self.verticalLayout_5.addWidget(self.pushButton_8)
        self.handlayout.addWidget(self.widget_2)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.handlayout.addItem(spacerItem1)
        self.verticalLayout_3.addWidget(self.handwidget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton_2.setText(_translate("MainWindow", "PushButton"))
        self.pushButton_4.setText(_translate("MainWindow", "PushButton"))
        self.pushButton.setText(_translate("MainWindow", "PushButton"))
        self.pushButton_3.setText(_translate("MainWindow", "PushButton"))
        self.pushButton_5.setText(_translate("MainWindow", "PushButton"))
        self.pushButton_6.setText(_translate("MainWindow", "PushButton"))
        self.pushButton_7.setText(_translate("MainWindow", "PushButton"))
        self.pushButton_8.setText(_translate("MainWindow", "PushButton"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

