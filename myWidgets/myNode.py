import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QPushButton, QApplication, QWidget, QMenu, QAction

from myWidgets.CommonHelper import CommonHelper


class myNode(QPushButton):
    """
    self.node = myNode(myCanvas)
    在快速拖动时会有绘制不及时的问题，需要在每种实例中用image来替换直接绘制
    """

    def __init__(self, widget=None):
        super(myNode, self).__init__(widget)
        self.menu = QMenu(self)
        self.m_flag = False
        self.canvas = widget
        self.mySettings()
        self.loadQSS()
        self.rightMenu()

    def mySettings(self):
        self.setSize(80, 80)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.rightMenuShow)  # 开放右键策略

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.m_flag = True
            self.m_Position = event.globalPos() - self.pos()  # 获取鼠标相对窗口的位置
            event.accept()
            self.setCursor(QCursor(Qt.OpenHandCursor))  # 更改鼠标图标

    def mouseMoveEvent(self, QMouseEvent):
        if Qt.LeftButton and self.m_flag:
            self.move(QMouseEvent.globalPos() - self.m_Position)  # 更改窗口位置
            QMouseEvent.accept()

    def mouseReleaseEvent(self, QMouseEvent):
        self.m_flag = False
        self.setCursor(QCursor(Qt.ArrowCursor))

    def loadQSS(self):
        styleFile = 'E:/structureVisualization/myQSS/node.qss'
        qssStyle = CommonHelper.readQSS(styleFile)
        self.setStyleSheet(qssStyle)

    def rightMenuShow(self):
        self.menu.triggered.connect(self.menuSlot)
        self.menu.exec_(QCursor.pos())

    def setSize(self, width, heigh=-1):
        """
        设置长宽
        :param width: int
        :param heigh: int
        :return: void
        """
        if heigh < 0:
            heigh = width
        self.setMinimumSize(width, heigh)
        self.setMaximumSize(width, heigh)
        self.resize(width, heigh)

    def addMenuAction(self, action):
        """
        添加右键菜单action
        :param action: str
        :return:
        """
        self.menu.addAction(QAction(action, self.menu))

    def addMenuSpliter(self):
        """
        添加右键菜单分割线
        :return:
        """
        self.menu.addSeparator()

    def menuSlot(self, act):
        """
        通过act.text()来判断选中了哪个选项
        """
        pass

    def mouseDoubleClickEvent(self, event):
        """
        弹出数据对话框
        """
        pass

    def moveEvent(self, event):
        """
        需要被重载
        设置为上下左右四个点的边界
        目前没有实例有些错误
        """
        pass
        # 大概是以下格式
        # print(self.geometry())
        # if self.geometry().x() < self.canvas.geometry().x():
        #     self.setGeometry(self.canvas.geometry().x(), self.geometry().y(), 80, 80)
        # elif self.geometry().x() > self.canvas.geometry().x() + self.canvas.width():
        #     self.setGeometry(self.canvas.geometry().x() + self.canvas.width(), self.geometry().y(), 80, 80)
        # elif self.geometry().y() < self.canvas.geometry().y():
        #     self.setGeometry(self.geometry().x(), self.canvas.geometry().y(), 80, 80)
        # elif self.geometry().y() > self.canvas.geometry().y() + self.canvas.height():
        #     self.setGeometry(self.geometry().x(), self.canvas.geometry().y() + self.canvas.height(), 80, 80)

    def rightMenu(self):
        """
        需要被重载，来设置右键菜单显示的内容
        :return:
        """
        pass


if __name__ == '__main__':
    class test(QWidget):
        def __init__(self):
            super(test, self).__init__()
            self.button = myNode(self)
            self.resize(400, 300)


    app = QApplication(sys.argv)
    win = test()
    win.show()
    sys.exit(app.exec_())
