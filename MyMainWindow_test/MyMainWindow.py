import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QVBoxLayout, QHBoxLayout
from CanvasTest import CanvasTest
from myWidgets.myTopBar import myTopBar


class MyMainWindow(QMainWindow):
    def __init__(self):
        super(MyMainWindow, self).__init__()
        # 以下为使用到的组件的声明
        self.mainframe = QWidget()
        self.topBar = myTopBar(self)
        self.canvas = CanvasTest()

        self.mainLayout = QVBoxLayout()
        self.mainBodyLayout = QHBoxLayout()
        # 以下为成员参数的声明
        # 基础函数
        self.mySettings()
        self.myLayout()

    def mySettings(self):
        self.resize(800, 600)
        self.setWindowTitle('数据结构可视化')
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)

    def myLayout(self):
        self.setCentralWidget(self.mainframe)
        self.mainframe.setLayout(self.mainLayout)
        self.mainLayout.addStretch(0)
        self.mainLayout.addWidget(self.topBar)
        self.mainLayout.addStretch(1)
        self.mainLayout.addLayout(self.mainBodyLayout)
        self.mainLayout.addStretch(1)
        self.mainBodyLayout.addWidget(self.canvas)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MyMainWindow()
    win.show()
    sys.exit(app.exec_())
