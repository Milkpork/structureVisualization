from PyQt5.QtGui import QFont, QTextCursor
from PyQt5.QtWidgets import QTextEdit, QApplication, QMainWindow
import sys


class MyLogInfo(QTextEdit):
    def __init__(self):
        super(MyLogInfo, self).__init__()
        self.mySettings()
        self.fresh()
        self.textChanged.connect(self.a)
        # self.cursorPositionChanged.connect(self.a)

    def a(self):
        if len(self.toPlainText()) == 0:
            self.fresh()
            return
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

    def mySettings(self):
        self.resize(300, 600)
        self.setFont(QFont('楷体', 18))

    def cursorToEnd(self):
        cursor = self.textCursor()
        cursor.movePosition(QTextCursor.End)
        self.setTextCursor(cursor)


if __name__ == '__main__':
    class test(QMainWindow):
        def __init__(self):
            super(test, self).__init__()
            # self.setWindowFlags(Qt.FramelessWindowHint)
            self.a = MyLogInfo()
            self.a.setParent(self)
            self.resize(400, 400)


    app = QApplication(sys.argv)
    win = test()
    win.show()
    sys.exit(app.exec_())
