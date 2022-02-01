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
        #
        # pen.setStyle(Qt.DashLine)
        # painter.setPen(pen)
        # painter.drawLine(20, 50, 250, 50)
        #
        # pen.setStyle(Qt.DashDotDotLine)
        # painter.setPen(pen)
        # painter.drawLine(20, 60, 250, 60)
        #
        # pen.setStyle(Qt.DotLine)
        # painter.setPen(pen)
        # painter.drawLine(20, 70, 250, 70)
        #
        # pen.setStyle(Qt.CustomDashLine)  # 自定义线类型
        # pen.setDashPattern([1, 4, 8, 4])  # 分别代表 长度1 ，间隔1，长度2，间隔2，循环
        # painter.setPen(pen)
        # painter.drawLine(20, 80, 250, 80)

        painter.end()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = DrawLines()
    main.show()
    sys.exit(app.exec_())
