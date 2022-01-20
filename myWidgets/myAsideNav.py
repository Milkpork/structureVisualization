"""
摆烂
"""

import sys
from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout
from myWidgets.CommonHelper import CommonHelper


class Tab(QPushButton):
    def __init__(self):
        super(Tab, self).__init__()


class Add(QPushButton):
    def __init__(self):
        super(Add, self).__init__()


class myAsideNav(QWidget):
    def __init__(self):
        super(myAsideNav, self).__init__()
        self.tabList = []

        self.layout = QVBoxLayout()
        self.addButton = Tab()

        self.mySettings()
        self.myLayouts()
        self.flash()

    def mySettings(self):
        self.setContentsMargins(0, 0, 0, 0)
        self.resize(20, 200)
