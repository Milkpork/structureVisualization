import sys

from PyQt5.QtCore import QRect, QPoint
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QTabWidget, QWidget, QApplication, QTabBar, QStylePainter, QStyleOptionTab, \
    QStyle
from Structures import LinearList


class MyTabBar(QTabBar):
    def __init__(self):
        super(MyTabBar, self).__init__()
        self.mySettings()

    def mySettings(self):
        self.setContentsMargins(0, 0, 0, 0)

    def tabSizeHint(self, index):
        maxWidth = 40
        maxHeight = 25
        s = QTabBar.tabSizeHint(self, index)
        s.transpose()
        # 限制长宽
        s.setWidth(maxWidth if s.width() > maxWidth else s.width())
        s.setHeight(maxHeight if s.height() > maxHeight else s.height())
        return s

    def paintEvent(self, QPaintEvent):
        painter = QStylePainter(self)
        opt = QStyleOptionTab()
        for i in range(self.count()):
            self.initStyleOption(opt, i)
            painter.drawControl(QStyle.CE_TabBarTabShape, opt)
            painter.save()

            s = opt.rect.size()
            s.transpose()
            r = QRect(QPoint(), s)

            r.moveCenter(opt.rect.center())
            opt.rect = r
            c = self.tabRect(i).center()
            painter.translate(c)
            painter.rotate(90)
            painter.translate(-c)
            painter.drawControl(QStyle.CE_TabBarTabLabel, opt)
            painter.restore()


class MyTab(QTabWidget):
    def __init__(self):
        super(MyTab, self).__init__()

        self.tabBar = MyTabBar()  # 导航条

        self.mySettings()
        self.tab_test()

    def mySettings(self):
        self.setContentsMargins(0, 0, 0, 0)
        self.setTabBar(self.tabBar)
        self.setTabPosition(QTabWidget.West)  # 在右侧显示
        self.setCurrentIndex(1)

    def tab_test(self):
        self.resize(1200, 600)
        self.currentChanged.connect(self.changeIndex)
        # self.setCornerWidget(QPushButton('hp'))
        self.addTab(QWidget(), QIcon("E:/structureVisualization/mySources/pic/plus.png"), '')
        self.addTab(LinearList(), 'h')
        self.addTab(QWidget(), 'hello22222222')

    def changeIndex(self, ac):
        if ac == 0:
            print("add now")
            self.setCurrentIndex(1)


class test(QWidget):
    def __init__(self):
        super(test, self).__init__()
        self.tab = MyTab()
        self.tab.setParent(self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = test()
    win.show()
    sys.exit(app.exec_())
