import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor, QPalette, QColor
from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout, QMainWindow, QApplication, QMenu

from myWidgets.CommonHelper import CommonHelper


# 基类
class TopBarButton(QPushButton):
    def __init__(self, window=None):
        super(TopBarButton, self).__init__()
        self.window = window
        self.fundSettings()

    def fundSettings(self):
        self.setMaximumSize(20, 20)
        self.setMinimumSize(20, 20)
        self.setContentsMargins(0, 0, 0, 0)

    def setWindow(self, window):
        self.window = window


# 首先定义右侧三个按钮 最小化/最大化/关闭
class minimizeButton(TopBarButton):
    """
    最小化按钮
    初始化时需要传入参数为哪个窗口
        或者使用self.setWindow()来设置
    """

    def __init__(self, window=None):
        super(minimizeButton, self).__init__(window)

    def minimize(self):
        # 将窗口最小化
        self.window.setWindowState(Qt.WindowMinimized)


class maximizeButton(TopBarButton):
    """
    最大化按钮
    注意要判断是否最大以此来修改图像
    """

    def __init__(self, window=None):
        super(maximizeButton, self).__init__(window)

    def maximize(self):
        # 将窗口最大化
        if self.window.isFullScreen():
            self.window.showNormal()
        else:
            self.window.setWindowState(Qt.WindowFullScreen)  # 全屏


class exitButton(TopBarButton):
    """
    退出按钮
    """

    def __init__(self, window=None):
        super(exitButton, self).__init__(window)

    def exit(self):
        self.window.close()


class settingButton(QPushButton):
    def __init__(self):
        super(settingButton, self).__init__()
        self.fundSettings()

    def fundSettings(self):
        self.setMaximumSize(20, 20)
        self.setMinimumSize(20, 20)
        self.setContentsMargins(0, 0, 0, 0)


class settingsMenu(QMenu):
    def __init__(self, window=None):
        super(settingsMenu, self).__init__(window)
        self.window = window
        self.myLayout()

    def showMenu(self):
        self.exec_(QCursor.pos())

    def myLayout(self):
        self.addAction('新建')
        self.addSeparator()
        self.addAction('保存')
        self.addAction('导入')
        self.addSeparator()
        self.addAction('设置')


class myTopBar(QWidget):
    def __init__(self, wind=None, settingExists=True):
        """
        注意：使用本工具条会自动为窗口设置为FramelessWindowHint
        第一个参数用于设置该顶部条的窗口是哪个
        第二个参数True表示需要设置按钮，False为不显示设置按钮
        :param wind:
        :param settingExists:
        """
        super(myTopBar, self).__init__()
        self.window = wind
        if self.window is None:
            raise ValueError("TopBar need a parameter to state its window")
        if settingExists is False:
            self.setting.setVisible(False)
        self.m_flag = False
        self.layout = QHBoxLayout()
        self.mini = minimizeButton(self.window)
        self.maxi = maximizeButton(self.window)
        self.exitbutton = exitButton(self.window)
        self.setting = settingButton()
        self.settingsMenu = settingsMenu(self.window)
        self.myLayout()
        self.mysignalConnection()
        self.mySettings()
        self.loadQSS()
        self.setBcPic()

    def myLayout(self):
        self.setLayout(self.layout)
        self.layout.addStretch(0)
        self.layout.addWidget(self.setting)

        self.layout.addStretch(1)
        self.layout.addWidget(self.mini)
        self.layout.addWidget(self.maxi)
        # self.maxi.setVisible(False)
        self.layout.addWidget(self.exitbutton)

    def mysignalConnection(self):
        self.mini.clicked.connect(self.mini.minimize)
        self.maxi.clicked.connect(self.maxi.maximize)
        self.exitbutton.clicked.connect(self.exitbutton.exit)
        self.setting.clicked.connect(self.settingsMenu.showMenu)
        self.settingsMenu.triggered.connect(self.menuSlot)

    def mySettings(self):
        self.setMaximumHeight(40)
        self.setMinimumHeight(40)
        self.setAutoFillBackground(True)

        self.layout.setSpacing(10)
        self.layout.setContentsMargins(10, 0, 10, 0)

        self.setting.setMaximumHeight(20)
        self.setting.setMaximumWidth(20)
        self.setting.setContentsMargins(0, 0, 0, 0)
        self.setContextMenuPolicy(Qt.CustomContextMenu)

        self.window.setWindowFlags(Qt.FramelessWindowHint)  # 设置窗口为无边框样式

    def menuSlot(self, ac):
        """
        顶部菜单
        :return:
        """
        print(ac.text())
        pass

    def setBcPic(self):
        # 设置背景颜色
        palette = QPalette()
        palette.setBrush(QPalette.Background, QColor(90, 90, 90))
        self.setPalette(palette)

    def loadQSS(self):
        styleFile = 'E:/structureVisualization/myQSS/topBar.qss'
        qssStyle = CommonHelper.readQSS(styleFile)
        self.setStyleSheet(qssStyle)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.m_flag = True
            self.m_Position = event.globalPos() - self.window.pos()  # 获取鼠标相对窗口的位置
            event.accept()
            self.setCursor(QCursor(Qt.OpenHandCursor))  # 更改鼠标图标

    def mouseMoveEvent(self, QMouseEvent):
        if Qt.LeftButton and self.m_flag:
            if self.window.isFullScreen():
                self.window.showNormal()
                desktop = QApplication.desktop()
                flag = QCursor().pos().x() / desktop.width()  # 系数
                self.window.move(int(QCursor().pos().x() - self.window.width() * flag),
                                 QCursor().pos().y() - self.height() // 2)
                self.m_Position = QMouseEvent.globalPos() - self.window.pos()  # 获取鼠标相对窗口的位置
            else:
                pass
                self.window.move(QMouseEvent.globalPos() - self.m_Position)  # 更改窗口位置
            QMouseEvent.accept()

    def mouseReleaseEvent(self, QMouseEvent):
        self.m_flag = False
        self.setCursor(QCursor(Qt.ArrowCursor))

    def mouseDoubleClickEvent(self, event):
        if self.window.isFullScreen():
            self.window.showNormal()
        else:
            self.window.setWindowState(Qt.WindowFullScreen)  # 全屏


if __name__ == '__main__':
    class test(QMainWindow):
        def __init__(self):
            super(test, self).__init__()
            self.setCentralWidget(myTopBar(self))
            self.resize(400, 400)


    app = QApplication(sys.argv)
    win = test()
    win.show()
    sys.exit(app.exec_())
