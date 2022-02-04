# 绘制直线
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class DrawLines(QWidget):
    def __init__(self):
        super(DrawLines, self).__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('画直线')
        self.resize(300, 200)

    def paintEvent(self, QPaintEvent):
        painter = QPainter(self)
        painter.begin(self)
        pen = QPen(Qt.red, 3, Qt.SolidLine)
        painter.setPen(pen)
        painter.drawLine(20, 40, 250, 40)
        painter.end()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = DrawLines()
    main.show()
    sys.exit(app.exec_())
