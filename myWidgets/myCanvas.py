import sys

from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QCursor, QPalette, QColor
from PyQt5.QtWidgets import QWidget, QMenu, QAction, QFrame, QApplication
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
    def __init__(self):
        super(myCanvas, self).__init__()
        self.menu = myRightMenu()
        self.mySettings()
        self.myRightMenu()
        self.setBcPic()
        # self.loadQSS()

    def mySettings(self):

        self.setContentsMargins(0, 0, 0, 0)
        # self.setAutoFillBackground(True)
        self.setSize(800, 450)
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

    def addMenuAction(self, ac):
        self.menu.addMenuAction(ac)

    def addMenuSpliter(self):
        self.menu.addMenuSpliter()

    def myRightMenu(self):
        """
        需要被重载
        self.addMenuAction('xinjian') -> 向右键菜单添加一列
        self.addMenuSpliter() -> 添加分割线
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
        # palette.setBrush(QPalette.Background, QColor(r, g, b))
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
    class test(QWidget):
        def __init__(self):
            super(test, self).__init__()
            self.button = myCanvas()
            self.resize(400, 300)


    app = QApplication(sys.argv)
    win = test()
    win.show()
    sys.exit(app.exec_())
