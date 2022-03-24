import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QTextCursor, QKeyEvent
from PyQt5.QtWidgets import QTextEdit, QApplication, QMainWindow, QWidget
from CustomWidgets.Fundsettings import Fundsettings, FundColor


class MyLogInfo(QTextEdit):
    font_size = 12  # 字体大小

    def __init__(self, workplace: QWidget = None):
        super(MyLogInfo, self).__init__()
        self.setStyleSheet(
            "QTextEdit{color:%s;border:2px solid %s;margin:30px 20px 20px 5px;background-color:transparent;border-radius:5px;}"
            "QTextEdit:focus {border: 2px solid %s;}" % (
                FundColor.fontColor, FundColor.loginfoBorderColor, FundColor.loginfoBorderHoverColor
            )
        )
        self.backNum = 0
        self.workplace = workplace

        self.mySettings()

    def mySettings(self):
        self.resize(300, 600)
        self.setMaximumWidth(300)
        self.setFont(QFont(Fundsettings.font_family, self.font_size))

        # init
        self.append(">>> ")
        self.cursorToEnd()

    # 输入重载
    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:  # 如果是Enter 按钮
            order = self.toPlainText().split('\n')[-1].lstrip('>>> ')
            self.proOrder(order)
            self.cursorToEnd()
            super().keyPressEvent(event)
            self.append(">>> ")
            self.cursorToEnd()
        elif event.key() == Qt.Key_Backspace:  # 删除键
            cursor = self.textCursor()
            if cursor.columnNumber() > 4 and cursor.blockNumber() == cursor.document().blockCount() - 1:  # 只允许修改最下面一行的四位以后
                super().keyPressEvent(event)
        elif event.key() == Qt.Key_Up:  # 上
            self.backNum += 1
            ls = self.toPlainText().split('\n')
            self.setText("\n".join(ls[:-1]))  # 把最后一行去掉
            self.cursorToEnd()
            self.append("\n" + ls[-(self.backNum % len(ls)) - 1])
            super().keyPressEvent(event)
            self.cursorToEnd()
        elif event.key() == Qt.Key_Down:  # 下
            self.backNum -= 1
            ls = self.toPlainText().split('\n')
            self.setText("\n".join(ls[:-1]))  # 把最后一行去掉
            self.cursorToEnd()
            self.append("\n" + ls[-(self.backNum % len(ls)) - 1])
            super().keyPressEvent(event)
            self.cursorToEnd()
        else:
            super().keyPressEvent(event)

    def append(self, text: str):
        self.setText(self.toPlainText() + text)

    # 接口:将光标移到最后
    def cursorToEnd(self):
        cursor = self.textCursor()
        cursor.movePosition(QTextCursor.End)
        self.setTextCursor(cursor)

    # 接口:返回工作区
    def getWorkplace(self):
        return self.workplace

    # 当输入了\n后响应指令函数，需要被重载
    def proOrder(self, order: str):
        pass


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
