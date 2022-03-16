from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QCursor, QPalette, QColor, QMouseEvent, QFont
from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout, QMenu, QApplication, QMainWindow, QAction
from CustomWidgets.Fundsettings import Fundsettings


# 按钮基类
class TopBarButton(QPushButton):
    radius = 20  # 半径
    hover_color = "#999"  # hover的颜色

    def __init__(self, window: QMainWindow = None):
        super(TopBarButton, self).__init__()
        self.window = window

        self.mySettings()

    def mySettings(self):
        self.setMaximumSize(self.radius, self.radius)
        self.setMinimumSize(self.radius, self.radius)
        self.setContentsMargins(0, 0, 0, 0)


# 首先定义右侧三个按钮 最小化/最大化/关闭
class minimizeButton(TopBarButton):
    def __init__(self, window: QMainWindow = None):
        super(minimizeButton, self).__init__(window)
        self.setStyleSheet(
            "minimizeButton{border-image: url(%s/pic/minimizeButton.png);border-radius: %dpx;}"
            "minimizeButton:hover{background-color:%s}" % (
                Fundsettings.resource_path, TopBarButton.radius // 2, TopBarButton.hover_color)
        )
        self.clicked.connect(self.minimize)

    # 最小化窗口
    def minimize(self):
        self.window.setWindowState(Qt.WindowMinimized)


class maximizeButton(TopBarButton):
    def __init__(self, window: QMainWindow = None):
        super(maximizeButton, self).__init__(window)
        self.setStyleSheet(
            "maximizeButton{border-image: url(%s/pic/maximizeButton.png);border-radius: %dpx;}"
            "maximizeButton:hover{background-color:%s}" % (
                Fundsettings.resource_path, TopBarButton.radius // 2, TopBarButton.hover_color)
        )
        self.clicked.connect(self.maximize)

    # 将窗口最大化
    def maximize(self):
        if self.window.isFullScreen():
            self.window.showNormal()
        else:
            self.window.setWindowState(Qt.WindowFullScreen)


class exitButton(TopBarButton):
    def __init__(self, window: QMainWindow = None):
        super(exitButton, self).__init__(window)
        self.setStyleSheet(
            "exitButton{border-image: url(%s/pic/exitButton.png);border-radius: %dpx;}"
            "exitButton:hover{background-color:%s}" % (
                Fundsettings.resource_path, TopBarButton.radius // 2, TopBarButton.hover_color)
        )
        self.clicked.connect(self.closeWindow)

    # 关闭窗口
    def closeWindow(self):
        self.window.close()


# 设置按钮
class settingButton(TopBarButton):
    def __init__(self, window: QMainWindow = None):
        super(settingButton, self).__init__(window)
        self.setStyleSheet(
            "settingButton{border-image: url(%s/pic/settingButton.png);border-radius: %dpx;}"
            "settingButton:hover{background-color: %s;}" % (
                Fundsettings.resource_path, TopBarButton.radius // 2, TopBarButton.hover_color)
        )


# 设置菜单
class settingsMenu(QMenu):
    font_size = 12

    def __init__(self, window: QMainWindow = None):
        super(settingsMenu, self).__init__()
        self.setStyleSheet(
            "settingsMenu{border:1px solid black;}"
            "settingsMenu::item{padding:0px 5px 0px 5px;}"
            "settingsMenu::item{height:20px;}"
            "settingsMenu::item{background:white;}"
            "settingsMenu::item:selected:enabled{background-color:rgba(200,200,200,.7);}"

            "settingsMenu::separator{height:1px;}"
            "settingsMenu::separator{background:black;}"
            "settingsMenu::separator{margin:0px 8px 0px 8px;}"
        )
        self.window = window

        self.mySettings()
        self.mySignalConnections()
        self.myMenu()

    def mySettings(self):
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint | Qt.NoDropShadowWindowHint)  # 设置无阴影背景
        self.setFont(QFont(Fundsettings.font_family, self.font_size))

    def mySignalConnections(self):
        self.triggered.connect(self.menuSlot)

    # 菜单内的选项
    def myMenu(self):
        self.addAction('新建')
        self.addSeparator()
        self.addAction('保存')
        self.addAction('导入')
        self.addSeparator()
        self.addAction('设置')

    # 展示菜单
    def showMenu(self):
        self.exec_(QPoint(self.window.pos().x(), self.window.pos().y() + 40))  # 在setting按钮下方展示

    # 菜单对应的槽函数（事件）
    def menuSlot(self, ac: QAction):
        print(self.window.workplace.canvas)


# 顶部条(主类)
class MyTopBar(QWidget):
    bc_color = (90, 90, 90)  # 背景颜色
    fix_height = 40  # 固定高度

    def __init__(self, wind: QMainWindow, settingExists: bool = True):
        """
        注意：使用本工具条会自动为窗口设置为FramelessWindowHint
        第一个参数用于设置该顶部条的窗口是哪个
        第二个参数True表示需要设置按钮，False为不显示设置按钮
        """
        super(MyTopBar, self).__init__()
        self.window = wind
        self.m_flag = False
        self.m_Position = None

        self.mainLayout = QHBoxLayout()
        self.miniButton = minimizeButton(self.window)
        self.maxiButton = maximizeButton(self.window)
        self.exitButton = exitButton(self.window)
        self.settingButton = settingButton(self.window)
        self.settingsMenu = settingsMenu(self.window)

        if not settingExists:
            self.setting.setVisible(False)

        self.mySettings()
        self.myLayouts()
        self.mySignalConnections()
        self.myStyles()

    def mySettings(self):
        # 设置固定高度
        self.setFixedHeight(self.fix_height)

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
        self.settingButton.clicked.connect(self.settingsMenu.showMenu)

    def myStyles(self):
        # 设置背景颜色
        self.setAutoFillBackground(True)
        palette = QPalette()
        palette.setBrush(QPalette.Background, QColor(*self.bc_color))
        self.setPalette(palette)

        # 设置窗口为无边框样式
        self.window.setWindowFlags(Qt.FramelessWindowHint)

    # press+move+release三者构成窗口可拖拽
    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.m_flag = True
            self.m_Position = event.globalPos() - self.window.pos()  # 获取鼠标相对窗口的位置
            event.accept()
            self.setCursor(QCursor(Qt.OpenHandCursor))  # 更改鼠标图标

    def mouseMoveEvent(self, event: QMouseEvent):
        if Qt.LeftButton and self.m_flag:
            if self.window.isFullScreen():
                self.window.showNormal()
                desktop = QApplication.desktop()
                flag = QCursor().pos().x() / desktop.width()  # 系数
                self.window.move(int(QCursor().pos().x() - self.window.width() * flag),
                                 QCursor().pos().y() - self.height() // 2)
                self.m_Position = event.globalPos() - self.window.pos()  # 获取鼠标相对窗口的位置
            else:
                self.window.move(event.globalPos() - self.m_Position)  # 更改窗口位置
            event.accept()

    def mouseReleaseEvent(self, event: QMouseEvent):
        self.m_flag = False
        self.setCursor(QCursor(Qt.ArrowCursor))

    # 双击改变状态
    def mouseDoubleClickEvent(self, event: QMouseEvent):
        if self.window.isFullScreen():
            self.window.showNormal()
        else:
            self.window.setWindowState(Qt.WindowFullScreen)  # 全屏


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QMainWindow


    class test(QMainWindow):
        def __init__(self):
            super(test, self).__init__()
            a = MyTopBar(self)
            self.setCentralWidget(a)
            self.resize(400, 400)


    app = QApplication(sys.argv)
    win = test()
    win.show()
    sys.exit(app.exec_())
