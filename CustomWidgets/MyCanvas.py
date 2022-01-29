"""
将Node和Canvas整合到同一个文件中
"""
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor, QFont, QPalette, QColor
from PyQt5.QtWidgets import QPushButton, QFrame, QMenu, QAction


class MyNode(QPushButton):
    def __init__(self, widget=None, text=None):
        super(MyNode, self).__init__(widget)
        self.setStyleSheet(
            "MyNode{border-radius:40px;border:2px solid black;background-color:#fff;}"  # 本身的样式
        )
        self.text = text
        self.m_flag = False
        self.canvas = widget
        self.radius = 80  # 直径

        self.menu = QMenu(self)

        self.mySettings()
        self.mySignalConnections()

    def mySettings(self):
        self.setSize(self.radius)  # 设置大小
        self.setFont(QFont('楷体', 40))  # 设置字体
        self.setText(self.text)
        self.setContextMenuPolicy(Qt.CustomContextMenu)  # 开放右键策略
        self.customContextMenuRequested.connect(self.rightMenuShow)
        self.rightMenu()  # 右键菜单布局

    def mySignalConnections(self):
        self.menu.triggered.connect(self.menuSlot)

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

    def moveEvent(self, event):
        if self.pos().x() < 0:
            self.setGeometry(0, self.pos().y(), self.radius, self.radius)
        elif self.pos().x() > self.canvas.width() - self.width():
            self.setGeometry(self.canvas.width() - self.width(), self.pos().y(), self.radius, self.radius)
        elif self.pos().y() < 0:
            self.setGeometry(self.pos().x(), 0, self.radius, self.radius)
        elif self.pos().y() > self.canvas.height() - self.height():
            self.setGeometry(self.pos().x(), self.canvas.height() - self.height(), self.radius, self.radius)

    def rightMenuShow(self):
        self.menu.exec_(QCursor.pos())

    def setSize(self, width, heigh=-1):
        if heigh < 0:
            heigh = width
        self.setMinimumSize(width, heigh)
        self.setMaximumSize(width, heigh)

    def rightMenu(self):
        """
        need to be reloaded
        """
        # 右键菜单
        self.menu.addAction(QAction('删除', self))
        self.menu.addSeparator()
        self.menu.addAction(QAction('连线', self))

    def menuSlot(self, ac):
        """
        need to be reloaded
        通过act.text()来判断选中了哪个选项
        """
        print(ac.text())
        pass

    def mouseDoubleClickEvent(self, event):
        """
        随便reloaded 不 reloaded
        """
        # 弹出数据对话框
        # v, ok = QInputDialog.getInt(self, '整数输入框', '请输入值(0-100)', min=0, max=100)
        # if v and ok:
        #     self.value = v
        #     self.setText(str(v))
        pass


class MyCanvas(QFrame):
    def __init__(self):
        super(MyCanvas, self).__init__()
        self.setStyleSheet(
            "QMenu{background:LightSkyBlue; border:1px solid lightgray; border-color:green;}"  # 选项背景颜色
            "QMenu::item{padding:0px 5px 0px 5px;}"  # 以文字为标准，右边距文字40像素，左边同理
            "QMenu::item{height:20px;}"  # 显示菜单选项高度
            "QMenu{background:white;}"  # 选项背景
            "QMenu::item{margin:1px 1px 1px 1px;}"  # 每个选项四边的边界厚度，上，右，下，左

            "QMenu::item:selected:enabled{background:lightgray;}"
            "QMenu::item:selected:!enabled{background:transparent;}"  # 鼠标在上面时，选项背景为不透明

            "QMenu::separator{height:1px;}"  # 要在两个选项设置self.groupBox_menu.addSeparator()才有用
            "QMenu::separator{width:50px;}"
            "QMenu::separator{background:blue;}"
            "QMenu::separator{margin:0px 0px 0px 0px;}"
        )
        self.title = "测试用例"
        self.nodeDic = {}
        self.nodeCount = 0

        self.menu = QMenu(self)  # 右键菜单

        self.myStyles()
        self.mySettings()
        self.myLayouts()
        self.mySignalConnections()

    def mySettings(self):
        self.setMaximumSize(600, 600)
        self.resize(800, 800)
        self.setLineWidth(0)  # 设置外线宽度
        self.setMidLineWidth(0)  # 设置中线宽度
        self.setFrameStyle(QFrame.StyledPanel | QFrame.Plain)
        self.setContextMenuPolicy(Qt.CustomContextMenu)

    def myLayouts(self):
        self.rightMenu()  # 右键菜单的布局

    def myStyles(self):
        self.setAutoFillBackground(True)
        palette = QPalette()
        palette.setBrush(QPalette.Background, QColor(220, 220, 220))
        self.setPalette(palette)

    def mySignalConnections(self):
        self.customContextMenuRequested.connect(self.rightMenuShow)
        self.menu.triggered.connect(self.menuSlot)

    def rightMenuShow(self):
        self.menu.exec_(QCursor.pos())

    def addNode(self):
        self.nodeDic["button" + str(self.nodeCount)] = MyNode(self, str(self.nodeCount))
        self.nodeDic["button" + str(self.nodeCount)].move(20 * self.nodeCount, 0)
        return self.nodeDic["button" + str(self.nodeCount)]

    def rightMenu(self):
        """
        need to be reloaded
        """
        self.menu.addAction(QAction('新建', self))
        self.menu.addSeparator()
        self.menu.addAction(QAction('test', self))

    def menuSlot(self, ac):
        """
        need to be reloaded
        """
        print(ac.text())
        if ac.text() == '新建':
            self.addNode().setVisible(True)
            self.nodeCount += 1


if __name__ == '__main__':
    from PyQt5.QtWidgets import QMainWindow, QApplication
    import sys


    class test(QMainWindow):
        def __init__(self):
            super(test, self).__init__()
            self.setCentralWidget(MyCanvas())


    app = QApplication(sys.argv)
    win = test()
    win.show()
    sys.exit(app.exec_())
