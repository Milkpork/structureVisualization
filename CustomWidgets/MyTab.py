import sys

from PyQt5.QtCore import QPropertyAnimation, QSize
from PyQt5.QtGui import QPalette, QColor, QIcon, QFont
from PyQt5.QtWidgets import QFrame, QPushButton, QApplication, QVBoxLayout, QMainWindow, QToolTip

from CustomWidgets.Fundsettings import Fundsettings, FundColor
from CustomWidgets.MyNewWindow import MyNewWindow
from Structures import LinearList, BinaryTree, Graph


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
    bc_color = FundColor.singleTabBackgroundColor
    hover_color = FundColor.singleTabHoverColor  # 未使用
    press_color = FundColor.singleTabPressColor
    select_color = FundColor.singleTabSelectColor

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
            "SingleTabButton{margin:-1px 0;background-color:%s;height:40px;font-size:16px;border:1px solid transparent}"
            "SingleTabButton{font-size:16px;font_family:楷体;text-align:left;color:white}"
            "SingleTabButton:pressed{background-color:%s}" % (
                str(self.nowColor), str(self.press_color)
            )
        )
        if self.state == 0:
            self.setText(f'{self.title[:1]}…')
            self.setIcon(QIcon("E:/structureVisualization/mySources/pic/minimizeButton.png"))
            self.resize(self.fold_width, self.myHeight)
        elif self.state == 1:
            self.resize(self.unfold_width, self.myHeight)
            self.setText(self.title)
            self.setIcon(QIcon("E:/structureVisualization/mySources/pic/minimizeButton.png"))

    def resume(self):
        self.nowColor = self.bc_color
        self.myStyles()

    def select(self):
        self.nowColor = self.select_color
        self.myStyles()
        self.workplace.raise_()

    def setWorkplace(self, workplace):
        self.workplace = workplace


class MyAddButton(QPushButton):
    size = 20
    hover_color = FundColor.addButtonHoverColor
    bc_color = FundColor.addButtonBackgroundColor

    def __init__(self, tabbar):
        super(MyAddButton, self).__init__()
        self.setStyleSheet(
            "MyAddButton{background-color:%s;border-image: url(:pic/plus2.png);border-radius: %dpx;}"
            "MyAddButton:hover{background-color:%s}" % (
                self.bc_color, self.size // 2, self.hover_color)
        )
        self.tabBar = tabbar
        self.mySettings()

    def mySettings(self):
        self.setFixedSize(self.size, self.size)
        self.setContentsMargins(0, 0, 0, 0)


class MyTab(QFrame):
    size_width = 40
    size_height = 1000
    animDuring = 200
    bc_color = FundColor.tabBackgroundColor

    def __init__(self):
        super(MyTab, self).__init__()
        self.setStyleSheet(
            "QFrame{border:1px solid white;background-color:%s;}" % (
                self.bc_color
            )
        )
        self.mainLayout = QVBoxLayout()
        self.addButton = MyAddButton(self)
        self.workplace = None  # 记录添加区

        self.nowWorkPlace = None  # 记录当前工作区

        self.index = 1

        self.mySettings()
        self.myLayouts()
        self.mySignalConnections()

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

    def addTab(self):
        QToolTip.setFont(QFont('SansSerif', 12))

        def addFunc(dic, w):
            w.close()
            tab = SingleTabButton(dic['title'])
            tab.setToolTip(dic['detail'])
            self.index += 1
            self.mainLayout.insertWidget(self.index, tab)
            tab.setVisible(True)
            tab.clicked.connect(self.selectTab)
            wp = None
            if dic['name'] == '线性表':
                wp = LinearList(dic['title'], dic['class'], dic['options'])
            elif dic['name'] == '二叉树':
                wp = BinaryTree(dic['title'], dic['class'], dic['options'])
            elif dic['name'] == '图':
                wp = Graph(dic['title'], dic['class'], dic['options'])
            tab.setWorkplace(wp)
            wp.setParent(self.workplace)
            wp.resize(self.workplace.width(), self.workplace.height())
            wp.setVisible(True)

            if self.nowWorkPlace is not None:
                self.nowWorkPlace.resume()
            self.nowWorkPlace = tab
            self.nowWorkPlace.select()

        windows = MyNewWindow()
        windows.ok.connect(lambda dic: addFunc(dic, windows))

    def selectTab(self):
        if self.nowWorkPlace is not None:
            self.nowWorkPlace.resume()
        self.nowWorkPlace = self.sender()
        self.nowWorkPlace.select()

    def setWorkplace(self, workplace):
        self.workplace = workplace

    def getNowWorkplace(self):
        try:
            return self.nowWorkPlace.workplace
        except AttributeError:
            return None

    def addTabAppoint(self, types, title, edition, funcList):
        tab = SingleTabButton(title)
        self.index += 1
        self.mainLayout.insertWidget(self.index, tab)
        tab.setVisible(True)
        tab.clicked.connect(self.selectTab)

        wp = None
        # detail 还未使用
        if types == '线性表':
            wp = LinearList(title, edition, funcList)
        elif types == '二叉树':
            wp = BinaryTree(title, edition, funcList)
        elif types == "图":
            wp = Graph(title, edition, funcList)
        tab.setWorkplace(wp)
        wp.setParent(self.workplace)
        wp.resize(self.workplace.width(), self.workplace.height())
        wp.setVisible(True)

        if self.nowWorkPlace is not None:
            self.nowWorkPlace.resume()
        self.nowWorkPlace = tab
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
