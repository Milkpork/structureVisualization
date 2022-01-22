import sys
from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout, QVBoxLayout


class MoreButtonList(QWidget):
    def __init__(self):
        super(MoreButtonList, self).__init__()
        self.button1 = QPushButton('遍历1')
        self.button2 = QPushButton('遍历2')

    def setSize(self, width, height):
        self.resize(width, height)
        self.setMaximumSize(width, height)
        self.setMinimumSize(width, height)


class MoreButton(QPushButton):
    def __init__(self):
        super(MoreButton, self).__init__()
        self.settings()

    def settings(self):
        self.setSize(50, 50)
        self.setText("上")

    def setSize(self, width, height):
        self.resize(width, height)
        self.setMaximumSize(width, height)
        self.setMinimumSize(width, height)


class RunButton(QPushButton):
    def __init__(self):
        super(RunButton, self).__init__()


class myRunButton(QWidget):
    def __init__(self):
        super(myRunButton, self).__init__()
