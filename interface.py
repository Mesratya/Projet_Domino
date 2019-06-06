# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\Yassi\PycharmProjects\ProjetDomino\interface.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import QtMultimedia as M


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        #MainWindow.resize(800, 587)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("images/logo.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.centrallayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.centrallayout.setObjectName("centrallayout")
        self.gridwidget = QtWidgets.QWidget(self.centralwidget)
        self.gridwidget.setObjectName("gridwidget")
        self.gridlayout = QtWidgets.QGridLayout(self.gridwidget)
        self.gridlayout.setObjectName("gridlayout")
        self.centrallayout.addWidget(self.gridwidget)
        self.handwidget = QtWidgets.QWidget(self.centralwidget)
        self.handwidget.setObjectName("handwidget")
        self.handlayout = QtWidgets.QHBoxLayout(self.handwidget)
        self.handlayout.setObjectName("handlayout")

        # self.dominowidget = QtWidgets.QWidget(self.handwidget)
        # self.dominowidget.setObjectName("dominowidget")
        # self.domino_layout = QtWidgets.QVBoxLayout(self.dominowidget)
        # self.domino_layout.setObjectName("domino_layout")
        # self.handlayout.addWidget(self.dominowidget)

        self.centrallayout.addWidget(self.handwidget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        #self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)



        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Domino Adventure"))



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

