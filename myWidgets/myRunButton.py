import sys

from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QMainWindow, QApplication

from myWidgets.CommonHelper import CommonHelper


class moreNode(QPushButton):
    def __init__(self, wi=None):
        super(moreNode, self).__init__(wi)
        self.settings()

    def settings(self):
        self.setAutoFillBackground(True)
        self.setContentsMargins(0, 0, 0, 0)
        self.setSize(100, 50)
        self.setBcPic(98, 45, 32)

    def setSize(self, w, h):
        self.resize(w, h)
        self.setMinimumSize(w, h)
        self.setMaximumSize(w, h)

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


class MoreButtonList(QWidget):
    def __init__(self):
        self.ls = ['1', '2']  # 需要被修改
        self.nodeList = {}
        super(MoreButtonList, self).__init__()
        self.mainLayout = QVBoxLayout()
        self.settings()
        self.showList()

    def settings(self):
        self.setContentsMargins(0, 0, 0, 0)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.mainLayout.setSpacing(0)

    def showList(self):
        """
        :return:
        """
        lens = len(self.ls)
        for i in range(lens):
            self.processNode(i, self.ls[i]).setVisible(True)

    def processNode(self, i, text):
        self.nodeList['button' + str(i)] = moreNode(self)
        self.nodeList['button' + str(i)].setText(text)
        # self.mainLayout.addWidget(self.nodeList['button' + str(i)])
        self.nodeList['button' + str(i)].setContentsMargins(0, 0, 0, 0)
        self.nodeList["button" + str(i)].setGeometry(0, 50 * i - i * 2, 100, 50)  # 这里大坑！！

        return self.nodeList['button' + str(i)]


class MoreButton(QPushButton):
    def __init__(self):
        super(MoreButton, self).__init__()
        self.settings()

    def settings(self):
        self.setText('fff')
        self.setContentsMargins(0, 0, 0, 0)
        self.setSize(30, 50)
        self.setAutoFillBackground(True)
        self.setBcPic(150, 200, 250)

    def setSize(self, w, h):
        self.resize(w, h)
        self.setMinimumSize(w, h)
        self.setMaximumSize(w, h)

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


class RunButton(QPushButton):
    def __init__(self):
        super(RunButton, self).__init__()
        self.settings()

    def settings(self):
        self.setText('Run')
        self.setContentsMargins(0, 0, 0, 0)
        self.setSize(70, 50)
        self.setAutoFillBackground(True)
        self.setBcPic(150, 200, 250)

    def setSize(self, w, h):
        self.resize(w, h)
        self.setMinimumSize(w, h)
        self.setMaximumSize(w, h)

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


class FundButtonWapper(QWidget):
    # 两个按钮的容器
    def __init__(self):
        super(FundButtonWapper, self).__init__()
        self.mainLayout = QHBoxLayout()
        self.runButton = RunButton()
        self.moreButton = MoreButton()
        self.settings()
        self.layouts()

    def layouts(self):
        self.setLayout(self.mainLayout)
        self.mainLayout.addWidget(self.runButton)
        self.mainLayout.addWidget(self.moreButton)

    def settings(self):
        self.mainLayout.setSpacing(0)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.setContentsMargins(0, 0, 0, 0)
        self.setAutoFillBackground(True)
        self.setBcPic(200, 200, 200)
        self.setSize(100, 50)

    def setSize(self, w, h):
        self.resize(w, h)
        self.setMinimumSize(w, h)
        self.setMaximumSize(w, h)

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


class myRunButton(QWidget):
    # 最外层容器
    def __init__(self):
        super(myRunButton, self).__init__()
        self.mainLayout = QVBoxLayout()

        self.button_wapper = FundButtonWapper()
        self.more_wapper = MoreButtonList()
        self.more_wapper.setVisible(False)
        self.button_wapper.moreButton.clicked.connect(self.a)
        self.settings()
        self.layouts()
        self.loadQSS()

    def a(self):
        self.more_wapper.setVisible(True)
        self.setSize(100, 150)

    def layouts(self):
        self.setLayout(self.mainLayout)
        self.mainLayout.addWidget(self.button_wapper)
        self.mainLayout.addWidget(self.more_wapper)

    def settings(self):
        self.setContentsMargins(0, 0, 0, 0)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.setAutoFillBackground(True)
        self.setBcPic()
        self.setSize(100, 50)

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

    def setSize(self, w, h):
        self.resize(w, h)
        self.setMinimumSize(w, h)
        self.setMaximumSize(w, h)

    def loadQSS(self):
        styleFile = 'E:/structureVisualization/myQSS/runButton.qss'
        qssStyle = CommonHelper.readQSS(styleFile)
        self.setStyleSheet(qssStyle)


class test(QMainWindow):
    def __init__(self):
        super(test, self).__init__()
        self.setCentralWidget(myRunButton())
        self.resize(200, 300)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = test()
    win.show()
    sys.exit(app.exec_())
