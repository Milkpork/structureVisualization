import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QHBoxLayout
from PyQt5.QtWidgets import QWidget, QVBoxLayout
from myWidgets.myTopBar import myTopBar
from myWidgets.myCanvas import myCanvas
from myWidgets.myNode import myNode


class myCanvasTest(myCanvas):
    def __init__(self):
        super(myCanvasTest, self).__init__()
        self.index = 1
        self.dict = {}

    def myRightMenu(self):
        self.menu.addMenuAction('新建')

    def showUi(self):
        self.dict["button" + str(self.index)] = myNode(self)
        self.dict["button" + str(self.index)].setText("botton" + str(self.index))

        return self.dict["button" + str(self.index)]

    def menuSlot(self, ac):
        if ac.text() == '新建':
            self.showUi().setVisible(True)
            self.index += 1


class mainWindow(QMainWindow):
    def __init__(self):
        super(mainWindow, self).__init__()

        self.mainframe = QWidget()
        self.mainLayout = QVBoxLayout()
        self.mainBodyLayout = QHBoxLayout()

        self.topBar = myTopBar(self)

        self.canvas = myCanvasTest()

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
    win = mainWindow()
    win.show()
    sys.exit(app.exec_())
