import sys

from PyQt5.QtCore import QPropertyAnimation, QSize
from PyQt5.QtGui import QPalette, QColor, QIcon
from PyQt5.QtWidgets import QFrame, QPushButton, QApplication, QVBoxLayout, QMainWindow

from CustomWidgets.Fundsettings import Fundsettings
from CustomWidgets.MyNewWindow import MyNewWindow


class SizeAnimation(QPropertyAnimation):
    def __init__(self, p, target, startValue, endValue, during):
        super(SizeAnimation, self).__init__(p)
        # 1.定义一个动画
        # animation = QPropertyAnimation(self)
        self.setTargetObject(target)
        self.setPropertyName(b'size')
        # 使用另外一种构造函数方式创建
        # animation = QPropertyAnimation(self.btn, b'pos', self)

        # 2.设置属性值
        self.setStartValue(startValue)
        self.setEndValue(endValue)

        # 3.设置时长
        self.setDuration(during)


class SingleTabButton(QPushButton):
    fold_width = 50
    unfold_width = 150
    myHeight = 100
    bc_color = (0, 0, 0, 0)
    hover_color = (150, 150, 150, 0.5)
    press_color = (255, 255, 0, 1)
    select_color = (0, 255, 255, 1)

    def __init__(self, title=None, workplace=None):
        super(SingleTabButton, self).__init__()
        self.title = title
        self.state = 0  # 状态:0表示缩略, 1表示展开
        self.nowColor = self.bc_color
        self.workplace = workplace

        self.myStyles()

    def myStyles(self):
        self.setContentsMargins(0, 0, 0, 0)
        self.setStyleSheet(
            "SingleTabButton{margin:-1px 0;background-color:rgba%s;height:40px;font-size:16px}"
            "SingleTabButton{font-size:16px;font_family:楷体;text-align:left;color:white}"
            "SingleTabButton:pressed{background-color:%s}" % (
                str(self.nowColor), str(self.press_color)
            )
        )
        if self.state == 0:
            self.setText(f'{self.title[:1]}...')
            self.setIcon(QIcon("%s/pic/minimizeButton.png" % Fundsettings.resource_path))
            self.resize(self.fold_width, self.myHeight)
        elif self.state == 1:
            self.resize(self.unfold_width, self.myHeight)
            self.setText(self.title)
            self.setIcon(QIcon("%s/pic/minimizeButton.png" % Fundsettings.resource_path))

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)

    def resume(self):
        self.nowColor = self.bc_color
        self.myStyles()
        # self.workplace.setZValue(0)

    def select(self):
        self.nowColor = self.select_color
        self.myStyles()
        # self.workplace.setZValue(1)


class MyAddButton(QPushButton):
    size = 20
    hover_color = "#999"

    def __init__(self, tabbar):
        super(MyAddButton, self).__init__()
        self.setStyleSheet(
            "MyAddButton{border-image: url(%s/pic/plus2.png);border-radius: %dpx;}"
            "MyAddButton:hover{background-color:%s}" % (
                Fundsettings.resource_path, self.size // 2, self.hover_color)
        )
        self.tabBar = tabbar
        self.mySettings()

    def mySettings(self):
        self.setFixedSize(self.size, self.size)
        self.setContentsMargins(0, 0, 0, 0)

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)


class MyTab(QFrame):
    size_width = 40
    size_height = 600
    animDuring = 200
    bc_color = (90, 90, 90)

    def __init__(self):
        super(MyTab, self).__init__()
        self.mainLayout = QVBoxLayout()
        self.addButton = MyAddButton(self)

        self.nowWorkPlace = None
        self.index = 1

        self.mySettings()
        self.myLayouts()
        self.mySignalConnections()
        self.myStyles()

    def mySettings(self):
        self.resize(self.size_width, self.size_height)
        self.setContentsMargins(0, 20, 0, 0)

    def myLayouts(self):
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.mainLayout.setSpacing(0)
        self.setLayout(self.mainLayout)
        self.mainLayout.addStretch(0)
        self.mainLayout.addWidget(self.addButton)
        self.mainLayout.addStretch(1)

    def myStyles(self):
        self.setAutoFillBackground(True)
        palette = QPalette()
        palette.setBrush(QPalette.Background, QColor(*self.bc_color))
        self.setPalette(palette)

    def mySignalConnections(self):
        self.addButton.clicked.connect(self.addTab)

    def enterEvent(self, event):
        super().enterEvent(event)
        anim = SizeAnimation(self, self, self.size(), QSize(self.size_width + 100, self.size_height), self.animDuring)
        anim.start()
        for i in self.children():
            if type(i) == SingleTabButton:
                i.state = 1
                i.myStyles()

    def leaveEvent(self, event):
        super().leaveEvent(event)
        anim = SizeAnimation(self, self, self.size(), QSize(self.size_width, self.size_height), self.animDuring)
        anim.start()
        for i in self.children():
            if type(i) == SingleTabButton:
                i.state = 0
                i.myStyles()

    # noinspection PyAttributeOutsideInit
    def addTab(self):
        self.windows = MyNewWindow()
        # self.windows.show()
        # tab = SingleTabButton(f'hello{str(self.index)}')
        # self.index += 1
        # self.mainLayout.insertWidget(self.index, tab)
        # tab.setVisible(True)
        # tab.clicked.connect(self.selectTab)

    def selectTab(self):
        if self.nowWorkPlace is not None:
            self.nowWorkPlace.resume()
        self.nowWorkPlace = self.sender()
        self.nowWorkPlace.select()


if __name__ == '__main__':
    class mainWindow(QMainWindow):
        def __init__(self):
            super(mainWindow, self).__init__()
            self.resize(400, 400)
            self.move(400, 100)
            a = MyTab()
            a.setParent(self)


    app = QApplication(sys.argv)
    win = mainWindow()
    win.show()
    sys.exit(app.exec_())
