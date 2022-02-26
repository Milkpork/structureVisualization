# coding: utf-8
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout
from CustomWidgets import MyTopBar
from Structures.LinearList.WorkPlace import WorkPlace


class LinearList(QMainWindow):
    def __init__(self):
        super(LinearList, self).__init__()

        self.mainWidget = QWidget()
        self.mainLayout = QVBoxLayout()

        self.topbar = MyTopBar(self)
        self.workplace = WorkPlace()

        self.mySettings()
        self.myLayouts()

    def mySettings(self):
        self.setMinimumSize(800, 600)

    def myLayouts(self):
        self.setCentralWidget(self.mainWidget)
        self.mainWidget.setLayout(self.mainLayout)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)

        self.mainLayout.addWidget(self.topbar)
        self.mainLayout.addWidget(self.workplace)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = LinearList()
    win.show()
    sys.exit(app.exec_())
