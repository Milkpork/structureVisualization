from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QCursor, QPalette, QColor
from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout, QMenu, QApplication


# 基类
class TopBarButton(QPushButton):
    radius = 20

    def __init__(self, window=None):
        super(TopBarButton, self).__init__()
        self.window = window

        self.mySettings()

    def mySettings(self):
        self.setMaximumSize(self.radius, self.radius)
        self.setMinimumSize(self.radius, self.radius)
        self.setContentsMargins(0, 0, 0, 0)


# 首先定义右侧三个按钮 最小化/最大化/关闭
class minimizeButton(TopBarButton):
    """
    最小化按钮
    初始化时需要传入参数为哪个窗口
    """

    def __init__(self, window=None):
        super(minimizeButton, self).__init__(window)
        self.setStyleSheet(
            "minimizeButton{border-image: url(E:/structureVisualization/mySources/pic/minimizeButton.png);border-radius: 10px;}"
            "minimizeButton:hover{background-color:#999}"
        )

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
        self.setStyleSheet(
            "maximizeButton{border-image: url(E:/structureVisualization/mySources/pic/maximizeButton.png);border-radius: 10px;}"
            "maximizeButton:hover{background-color:#999}"
        )

    def maximize(self):
        # 将窗口最大化
        if self.window.isFullScreen():
            self.window.showNormal()
        else:
            self.window.setWindowState(Qt.WindowFullScreen)


class exitButton(TopBarButton):
    """
    退出按钮
    """

    def __init__(self, window=None):
        super(exitButton, self).__init__(window)
        self.setStyleSheet(
            "exitButton{border-image: url(E:/structureVisualization/mySources/pic/exitButton.png);border-radius: 10px;}"
            "exitButton:hover{background-color:#999}"
        )

    def closeWindow(self):
        self.window.close()


class settingButton(TopBarButton):
    def __init__(self, window=None):
        super(settingButton, self).__init__(window)
        self.setStyleSheet(
            "settingButton{border-image: url(E:/structureVisualization/mySources/pic/settingButton.png);border-radius: 10px;}"
            "settingButton:hover{background-color: #999;}"
        )


class settingsMenu(QMenu):
    def __init__(self, window=None):
        super(settingsMenu, self).__init__()
        self.setStyleSheet(
            "settingsMenu{background:LightSkyBlue; border:1px solid lightgray; border-color:green;}"  # 选项背景颜色
            "settingsMenu::item{padding:0px 5px 0px 5px;}"  # 以文字为标准，右边距文字40像素，左边同理
            "settingsMenu::item{height:20px;}"  # 显示菜单选项高度
            "settingsMenu::item{background:white;}"  # 选项背景
            "settingsMenu::item{margin:1px 1px 1px 1px;}"  # 每个选项四边的边界厚度，上，右，下，左

            "settingsMenu::item:selected:enabled{background:lightgray;}"

            "settingsMenu::item:selected:!enabled{background:transparent;}"  # 鼠标在上面时，选项背景为不透明

            "settingsMenu::separator{height:1px;}"  # 要在两个选项设置self.groupBox_menu.addSeparator()才有用
            "settingsMenu::separator{width:50px;}"
            "settingsMenu::separator{background:blue;}"
            "settingsMenu::separator{margin:0px 0px 0px 0px;}"
        )  # 丑的一比，暂时用着
        self.window = window
        self.myLayouts()

    def showMenu(self):
        self.exec_(QPoint(self.window.pos().x(), self.window.pos().y() + 30))

    def myLayouts(self):
        """
        可修改，修改的是setting按钮里面的菜单
        """
        self.addAction('新建')
        self.addSeparator()
        self.addAction('保存')
        self.addAction('导入')
        self.addSeparator()
        self.addAction('设置')


class MyTopBar(QWidget):
    def __init__(self, wind, settingExists=True):
        """
        注意：使用本工具条会自动为窗口设置为FramelessWindowHint
        第一个参数用于设置该顶部条的窗口是哪个
        第二个参数True表示需要设置按钮，False为不显示设置按钮
        """
        super(MyTopBar, self).__init__()
        self.window = wind
        self.m_flag = False

        self.mainLayout = QHBoxLayout()
        self.miniButton = minimizeButton(self.window)
        self.maxiButton = maximizeButton(self.window)
        self.exitButton = exitButton(self.window)
        self.settingButton = settingButton(self.window)
        self.settingsMenu = settingsMenu(self.window)

        if settingExists is False:
            self.setting.setVisible(False)

        self.mySettings()
        self.myLayouts()
        self.mySignalConnections()
        self.myStyles()

    def mySettings(self):
        self.setMaximumHeight(40)
        self.setMinimumHeight(40)

        self.window.setWindowFlags(Qt.FramelessWindowHint)  # 设置窗口为无边框样式

    def myLayouts(self):
        self.mainLayout.setSpacing(10)
        self.mainLayout.setContentsMargins(10, 0, 10, 0)

        self.setLayout(self.mainLayout)
        self.mainLayout.addStretch(0)
        self.mainLayout.addWidget(self.settingButton)

        self.mainLayout.addStretch(1)
        self.mainLayout.addWidget(self.miniButton)
        self.mainLayout.addWidget(self.maxiButton)
        self.mainLayout.addWidget(self.exitButton)

    def mySignalConnections(self):
        self.miniButton.clicked.connect(self.miniButton.minimize)
        self.maxiButton.clicked.connect(self.maxiButton.maximize)
        self.exitButton.clicked.connect(self.exitButton.closeWindow)
        self.settingButton.clicked.connect(self.settingsMenu.showMenu)
        self.settingsMenu.triggered.connect(self.menuSlot)

    def myStyles(self):
        self.setAutoFillBackground(True)
        palette = QPalette()
        palette.setBrush(QPalette.Background, QColor(90, 90, 90))
        self.setPalette(palette)

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

    def menuSlot(self, ac):
        """
        need to be reloaded
        顶部菜单,通过ac.text()来发送选项
        :return:
        """
        print(ac.text())
        pass


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QMainWindow


    class test(QMainWindow):
        def __init__(self):
            super(test, self).__init__()
            self.setCentralWidget(MyTopBar(self))
            self.resize(400, 400)


    app = QApplication(sys.argv)
    win = test()
    win.show()
    sys.exit(app.exec_())
