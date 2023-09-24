import json
from datetime import date
from PyQt5 import QtCore, QtGui, QtWidgets

from main import CreationWindow, add_note

import sys


class Ui_window(object):
    def setupUi(self, window):  # установка параметров окна
        window.setObjectName('window')
        window.resize(1000, 700)

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(window.sizePolicy().hasHeightForWidth())

        window.setSizePolicy(sizePolicy)
        window.setMinimumSize(QtCore.QSize(1000, 700))
        window.setStyleSheet('background-color:rgb(40, 40, 40)')

        self.centralwidget = QtWidgets.QWidget(window)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setMouseTracking(False)
        self.centralwidget.setTabletTracking(False)
        self.centralwidget.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.centralwidget.setObjectName('centralwidget')

        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName('gridLayout')

        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.verticalLayout.setObjectName('verticalLayout')

        self.gridLayout.addLayout(self.verticalLayout, 1, 0, 1, 1)

        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 1, 1, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(868, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)

        self.gridLayout.addItem(spacerItem1, 0, 0, 1, 1)

        self.cr_button = QtWidgets.QPushButton(self.centralwidget)

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cr_button.sizePolicy().hasHeightForWidth())

        self.cr_button.setSizePolicy(sizePolicy)
        self.cr_button.setMinimumSize(QtCore.QSize(105, 50))
        self.cr_button.setSizeIncrement(QtCore.QSize(100, 100))
        self.cr_button.setBaseSize(QtCore.QSize(105, 50))

        font = QtGui.QFont()
        font.setPointSize(10)

        self.cr_button.setFont(font)
        self.cr_button.setStyleSheet('background-color:rgb(0, 0, 0);color:rgb(255, 255, 255);\n'
'border-radius:10px')
        self.cr_button.setObjectName("cr_button")
        self.cr_button.clicked.connect(self.cr_but_is_pressed)

        self.gridLayout.addWidget(self.cr_button, 0, 1, 1, 1)
        window.setCentralWidget(self.centralwidget)

        self.statusbar = QtWidgets.QStatusBar(window)
        self.statusbar.setEnabled(True)
        self.statusbar.setObjectName("statusbar")

        window.setStatusBar(self.statusbar)

        self.retranslateUi(window)
        QtCore.QMetaObject.connectSlotsByName(window)

        self.cr_window = None

        self.notes = []

        self.scrollWidget = QtWidgets.QWidget()
        self.scrollLayout = QtWidgets.QGridLayout(self.scrollWidget)

        with open('info.json') as file:
            temp_list = json.load(file)
            row_layout = None

            for i in range(len(temp_list)):
                add_note(temp_list[i]['name'], temp_list[i]['mes'], temp_list[i]['par_3'], self.notes, self.scrollLayout)

        self.scrollArea = QtWidgets.QScrollArea()
        self.scrollArea.setWidget(self.scrollWidget)
        #self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scrollArea.setMinimumSize(800, 500)

        self.verticalLayout.addWidget(self.scrollArea)

    def cr_but_is_pressed(self):
        self.cr_window = CreationWindow(self, self.notes, self.scrollLayout)
        self.cr_window.show()

    def retranslateUi(self, window):
        _translate = QtCore.QCoreApplication.translate
        window.setWindowTitle(_translate("window", "MainWindow"))
        self.cr_button.setText(_translate("window", "Create note"))

if __name__ == "__main__":
    
    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QMainWindow()
    ui = Ui_window()
    ui.setupUi(window)

    window.show()

    sys.exit(app.exec_())
