from PyQt5.QtGui import QFont, QTextCursor
from PyQt5.QtWidgets import QTextEdit, QApplication, QMainWindow
import sys


class myLogInfo(QTextEdit):
    def __init__(self):
        super(myLogInfo, self).__init__()
        self.settings()
        self.fresh()
        # self.textChanged.connect(self.a)
        self.cursorPositionChanged.connect(self.a)

    def a(self):
        if self.toPlainText()[-1] == '\n':
            # self.setText(self.toPlainText()[:-1] + "\n>>> ")
            order = self.toPlainText().split('\n')[self.document().blockCount() - 2]
            self.proOrder(order.split()[1:])
            self.fresh()
        self.cursorToEnd()

    def proOrder(self, order):
        print(order)
        pass

    def fresh(self):
        self.append('>>> ')
        self.cursorToEnd()

    def settings(self):
        self.setSize(300, 500)
        self.setFont(QFont('楷体', 18))

    def setSize(self, width, height):
        """
        用来设置画布大小大接口
        :param width: int
        :param height: int
        :return: void
        """
        self.setMaximumSize(width, height)
        self.setMinimumSize(width, height)
        self.resize(width, height)

    def cursorToEnd(self):
        cursor = self.textCursor()
        cursor.movePosition(QTextCursor.End)
        self.setTextCursor(cursor)


if __name__ == '__main__':
    class test(QMainWindow):
        def __init__(self):
            super(test, self).__init__()
            # self.setWindowFlags(Qt.FramelessWindowHint)
            self.setCentralWidget(myLogInfo())
            self.resize(400, 400)


    app = QApplication(sys.argv)
    win = test()
    win.show()
    sys.exit(app.exec_())
