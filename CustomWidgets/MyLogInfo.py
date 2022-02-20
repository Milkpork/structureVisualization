from PyQt5.QtGui import QFont, QTextCursor
from PyQt5.QtWidgets import QTextEdit, QApplication, QMainWindow, QFrame
import sys


class MyLogInfo(QTextEdit):
    def __init__(self, canvas=None):
        super(MyLogInfo, self).__init__()
        self.setStyleSheet(
            "QTextEdit{border:2px solid gray;margin:30px 20px 20px 5px;background-color:transparent;border-radius:5px;}"
            "QTextEdit:focus {border: 2px solid black;}"
        )

        self.canvas = canvas

        self.mySignalConnections()
        self.mySettings()

    def mySettings(self):
        self.fresh()
        self.resize(300, 600)
        self.setFont(QFont('楷体', 12))
        self.setMaximumWidth(300)
        # self.setReadOnly(True)

    def mySignalConnections(self):
        self.textChanged.connect(self.textchange)

    def textchange(self):
        if len(self.toPlainText()) == 0:
            self.fresh()
            return
        if self.toPlainText()[-1] == '\n':
            order = self.toPlainText().split('\n')[self.document().blockCount() - 2]
            self.proOrder(order.lstrip('>>> '))
        elif len(self.toPlainText().split('\n')[self.document().blockCount() - 1]) < 3:
            self.setText(self.toPlainText() + '>')
        elif len(self.toPlainText().split('\n')[self.document().blockCount() - 1]) == 3:
            self.setText(self.toPlainText() + ' ')
        self.cursorToEnd()


    def proOrder(self, order):
        print(order)
        pass

    def fresh(self):
        self.setText(self.toPlainText() + '>>> ')
        self.cursorToEnd()

    def cursorToEnd(self):
        cursor = self.textCursor()
        cursor.movePosition(QTextCursor.End)
        self.setTextCursor(cursor)


if __name__ == '__main__':
    class test(QMainWindow):
        def __init__(self):
            super(test, self).__init__()
            self.a = MyLogInfo()
            self.a.setParent(self)
            self.resize(300, 600)


    app = QApplication(sys.argv)
    win = test()
    win.show()
    sys.exit(app.exec_())
