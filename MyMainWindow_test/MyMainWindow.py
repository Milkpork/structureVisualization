import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QVBoxLayout, QHBoxLayout
from CanvasTest import CanvasTest
from myWidgets import myInformation, myTopBar,myRunButton, myLogInfo


class MyMainWindow(QMainWindow):
    def __init__(self):
        super(MyMainWindow, self).__init__()
        # 以下为使用到的组件的声明
        self.mainframe = QWidget()
        self.topBar = myTopBar(self)
        self.canvas = CanvasTest()
        self.myInfo = myInformation()
        self.runButton = myRunButton()
        self.info = myLogInfo()

        self.mainLayout = QVBoxLayout()
        self.mainBodyLayout = QHBoxLayout()
        self.workPlaceLayout = QVBoxLayout()
        self.runAndInfoLayout = QHBoxLayout()

        # 以下为成员参数的声明
        pass
        # 基础函数
        self.mySettings()
        self.myLayout()

    def mySettings(self):
        self.resize(800, 600)
        self.setWindowTitle('数据结构可视化')
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.myInfo.setText(self.canvas.title)

    def myLayout(self):
        self.setCentralWidget(self.mainframe)
        self.mainframe.setLayout(self.mainLayout)
        self.mainLayout.addStretch(0)
        self.mainLayout.addWidget(self.topBar)
        self.mainLayout.addStretch(1)
        self.mainLayout.addLayout(self.mainBodyLayout)
        self.mainLayout.addStretch(1)

        self.mainBodyLayout.addLayout(self.workPlaceLayout)
        self.mainBodyLayout.addWidget(self.info)

        self.workPlaceLayout.addLayout(self.runAndInfoLayout)
        self.runAndInfoLayout.addWidget(self.myInfo)
        self.runAndInfoLayout.addWidget(self.runButton)
        self.workPlaceLayout.addWidget(self.canvas)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MyMainWindow()
    win.show()
    sys.exit(app.exec_())
