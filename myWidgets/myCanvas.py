import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor, QPalette, QColor
from PyQt5.QtWidgets import QApplication, QWidget, QMenu, QAction, QMainWindow
from myWidgets.CommonHelper import CommonHelper


class myRightMenu(QMenu):
    """
    self.menu = myRightMenu()
        上层画布需要开放右键策略
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.rightMenuShow)  # 开放右键策略
    """

    def __init__(self):
        super(myRightMenu, self).__init__()

    def rightMenuShow(self):
        self.exec_(QCursor.pos())

    def addMenuAction(self, action):
        """
        向右键菜单添加一项action
        :param action: str
        :return: void
        """
        self.addAction(QAction(action, self))

    def addMenuSpliter(self):
        """
        向右键菜单添加一个分割线
        :return:
        """
        self.addSeparator()


class myCanvas(QWidget):
    """
    self.canvas = myCanvas()
    """

    def __init__(self):
        super(myCanvas, self).__init__()
        self.dict = {}
        self.index = 0

        self.menu = myRightMenu()
        self.mySettings()
        self.myRightMenu()
        self.setBcPic()
        self.loadQSS()

    def mySettings(self):
        self.setAutoFillBackground(True)
        self.setSize(500, 450)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.menu.rightMenuShow)  # 开放右键策略
        self.menu.triggered.connect(self.menuSlot)

    def loadQSS(self):
        styleFile = 'E:/structureVisualization/myQSS/canvas.qss'
        qssStyle = CommonHelper.readQSS(styleFile)
        self.setStyleSheet(qssStyle)

    def showUi(self):
        """
        函数需要被重载用于创建结点
        详见最下面的案例
        :return:
        """
        pass

    def menuSlot(self, ac):
        """
        本函数需要被重载
        通过ac.text()来判断被点击的是哪个action然后连接至相应函数
        :return:
        """
        if ac.text() == 'xinjian':
            print(1)
        pass

    def myRightMenu(self):
        """
        需要被重载
        self.menu.addMenuAction('xinjian') -> 向右键菜单添加一列
        self.menu.addMenuSpliter() -> 添加分割线
        :return:
        """
        pass

    def setBcPic(self, r=90, g=90, b=90):
        """
        设置背景颜色
        :param r: int[0-255]
        :param g: int[0-255]
        :param b: int[0-255]
        :return: void
        """
        if r < 0 or g < 0 or b < 0 or r > 255 or b > 255 or g > 255:
            raise ValueError('RGB must be between 0 and 255')
        palette = QPalette()
        palette.setBrush(QPalette.Background, QColor(r, g, b))
        self.setPalette(palette)

    def setSize(self, width, height):
        """
        用来设置画布大小大接口
        :param width: int
        :param height: int
        :return: void
        """
        self.setMaximumSize(width, height)
        self.setMinimumSize(width, height)
        self.resize(width, height)


if __name__ == '__main__':
    class test(QMainWindow):
        def __init__(self):
            super(test, self).__init__()
            # self.setWindowFlags(Qt.FramelessWindowHint)
            self.setCentralWidget(myCanvas())
            self.resize(400, 400)


    app = QApplication(sys.argv)
    win = test()
    win.show()
    sys.exit(app.exec_())

# class myCanvasTest(myCanvas):
#     def __init__(self):
#         super(myCanvasTest, self).__init__()
#         self.index = 1
#         self.dict = {}
#
#     def myRightMenu(self):
#         self.menu.addMenuAction('新建')
#
#     def showUi(self):
#         self.dict["button" + str(self.index)] = myNode(self)
#         self.dict["button" + str(self.index)].setText("botton" + str(self.index))
#
#         return self.dict["button" + str(self.index)]
#
#     def menuSlot(self, ac):
#         if ac.text() == '新建':
#             self.showUi().setVisible(True)
#             self.index += 1
