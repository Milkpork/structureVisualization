import sys

from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QLabel, QWidget, QMainWindow, QApplication, QVBoxLayout
from CustomWidgets.Fundsettings import Fundsettings


# 信息展示（主类）
class MyInfo(QWidget):
    title_font_size = 50
    edition_font_size = 14

    def __init__(self, title: str = 'test', edition: str = 'testEdition'):
        super(MyInfo, self).__init__()

        self.titleWidget = QLabel(title)
        self.editionWidget = QLabel(edition)
        self.mainLayout = QVBoxLayout()

        self.mySettings()
        self.myLayouts()

    def mySettings(self):
        self.setMaximumHeight(120)
        self.titleWidget.setFont(QFont(Fundsettings.font_family, self.title_font_size))
        self.editionWidget.setFont(QFont(Fundsettings.font_family, self.edition_font_size))
        self.mainLayout.setSpacing(0)

        self.titleWidget.setContentsMargins(0, 0, 0, 0)
        self.editionWidget.setContentsMargins(50, 0, 0, 0)

    def myLayouts(self):
        self.setLayout(self.mainLayout)
        self.mainLayout.addWidget(self.titleWidget)
        self.mainLayout.addWidget(self.editionWidget)

    # 接口:修改标题文字
    def setTitleText(self, title: str):
        self.titleWidget.setText(title)


if __name__ == '__main__':
    class test(QMainWindow):
        def __init__(self):
            super(test, self).__init__()
            # self.setWindowFlags(Qt.FramelessWindowHint)
            self.a = MyInfo()
            self.a.setParent(self)
            self.resize(400, 400)


    app = QApplication(sys.argv)
    win = test()
    win.show()
    sys.exit(app.exec_())
