import sys

from PyQt5.QtGui import QPalette, QColor, QFont
from PyQt5.QtWidgets import QLabel, QWidget, QMainWindow, QApplication, QVBoxLayout


class MyInfo(QWidget):
    def __init__(self, title='test', edition='testEdition'):
        super(MyInfo, self).__init__()

        self.titleWidget = QLabel(title)
        self.editionWidget = QLabel(edition)
        self.mainLayout = QVBoxLayout()

        self.mySettings()
        self.myLayouts()
        # self.myStyles()

    def mySettings(self):
        self.titleWidget.setFont(QFont('楷体', 50))
        self.editionWidget.setFont(QFont('楷体', 14))
        self.mainLayout.setSpacing(0)

        self.titleWidget.setContentsMargins(0, 0, 0, 0)
        self.editionWidget.setContentsMargins(50, 0, 0, 0)

    def myLayouts(self):
        self.setMaximumHeight(120)
        self.setLayout(self.mainLayout)
        self.mainLayout.addWidget(self.titleWidget)
        self.mainLayout.addWidget(self.editionWidget)

    def myStyles(self):
        self.setAutoFillBackground(True)
        palette = QPalette()
        palette.setBrush(QPalette.Background, QColor(20, 90, 90))
        self.setPalette(palette)


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
