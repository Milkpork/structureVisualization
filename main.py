# coding: utf-8
# 主窗口
import sys

from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtGui import QPainterPath, QPainter, QBrush, QColor

from CustomWidgets import MyTopBar, MyTab, WelcomeInterface
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QHBoxLayout, QVBoxLayout


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.mainframe = QWidget()
        self.mainLayout = QVBoxLayout()
        self.topbar = MyTopBar(self, [1, 1, 1, 1])

        self.mainBody = QWidget()
        self.mainBodyLayout = QHBoxLayout()

        self.nav = MyTab()

        self.spaceplace = QWidget()
        self.workplace = QWidget()
        self.welcome = WelcomeInterface(self.nav, self)

        self.mySettings()
        self.myLayouts()

    def mySettings(self):
        self.nav.setWorkplace(self.workplace)
        self.resize(800 + MyTab.size_width, 600 + MyTopBar.fix_height)
        self.move((QApplication.desktop().width() - self.width()) // 2,
                  (QApplication.desktop().height() - self.height()) // 2)
        self.mainframe.setContentsMargins(0, 0, 0, 0)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.mainLayout.setSpacing(0)
        self.mainBody.setContentsMargins(0, 0, 0, 0)
        self.mainBodyLayout.setContentsMargins(0, 0, 0, 0)
        self.mainBodyLayout.setSpacing(0)
        self.spaceplace.setContentsMargins(0, 0, 0, 0)
        self.spaceplace.setFixedWidth(MyTab.size_width)
        self.workplace.setContentsMargins(0, 0, 0, 0)
        self.nav.setWorkplace(self.workplace)

    def myLayouts(self):
        self.setCentralWidget(self.mainframe)
        self.mainframe.setLayout(self.mainLayout)

        # 主界面
        self.mainLayout.addWidget(self.topbar)
        self.mainLayout.addWidget(self.mainBody)

        self.mainBody.setLayout(self.mainBodyLayout)
        self.mainBodyLayout.addWidget(self.spaceplace)
        self.mainBodyLayout.addWidget(self.workplace)
        self.welcome.setParent(self.workplace)

        self.nav.setParent(self)
        self.nav.move(0, MyTopBar.fix_height)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
