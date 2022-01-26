import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor, QFont
from PyQt5.QtWidgets import QLabel, QWidget, QMainWindow, QApplication, QHBoxLayout


class myInformation(QWidget):
    def __init__(self):
        super(myInformation, self).__init__()
        self.layout = QHBoxLayout()
        self.title = QLabel()

        self.setSize(700, 100)
        self.myLayout()
        self.mySettings()
        self.setBcPic()

    def myLayout(self):
        self.setLayout(self.layout)
        self.layout.addWidget(self.title)

    def mySettings(self):
        self.setContentsMargins(0, 0, 0, 0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setAutoFillBackground(True)
        self.title.setAlignment(Qt.AlignVCenter)
        self.title.setFont(QFont("宋体", 50))

    def setSize(self, width, height):
        self.resize(width, height)
        self.setMaximumSize(width, height)
        self.setMinimumSize(width, height)

    def setBcPic(self):
        # 设置背景颜色
        palette = QPalette()
        palette.setBrush(QPalette.Background, QColor(20, 90, 90))
        self.setPalette(palette)

    def setText(self, text):
        self.title.setText(text)


if __name__ == '__main__':
    class test(QMainWindow):
        def __init__(self):
            super(test, self).__init__()
            # self.setWindowFlags(Qt.FramelessWindowHint)
            self.setCentralWidget(myInformation())
            self.resize(400, 400)


    app = QApplication(sys.argv)
    win = test()
    win.show()
    sys.exit(app.exec_())
