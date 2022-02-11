import sys

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QComboBox, QWidget, QApplication, QLineEdit, QListWidget, QListWidgetItem


class MyLineEdit(QLineEdit):
    clicked = pyqtSignal(str)

    def mouseReleaseEvent(self, QMouseEvent):
        if QMouseEvent.button() == Qt.LeftButton:
            self.clicked.emit(self.text())


class MyRunButton(QComboBox):
    def __init__(self):
        super(MyRunButton, self).__init__()
        self.setStyleSheet(
            "MyRunButton{background-color:#ccc;}"
            "QComboBox::drop-down {border:1px solid black;border-radius:0 5px}"
            "MyRunButton QAbstractItemView::item{height:60px;}"  # 高度
            "MyRunButton QAbstractItemView::item:hover{background-color:#abc;color:#333;}"
        )
        self.items = ['先序遍历', '中序遍历', '后序遍历', 'test']

        self.myLineEdit()  # 设置文本框
        self.myListWidget()  # 设置下拉框
        self.mySettings()
        self.mySignalConnections()

    def mySettings(self):
        self.resize(200, 50)
        self.setContentsMargins(0, 0, 0, 0)

    def mySignalConnections(self):
        self.lineEdit().clicked.connect(self.a)
        self.currentIndexChanged.connect(lambda: self.a(self.currentText()))

    def a(self, t):
        """
        通过t.text()来判断点击哪个按钮
        :param t:
        :return:
        """
        pass

    def myLineEdit(self):
        le = MyLineEdit()  # 显示框右对齐
        le.setAlignment(Qt.AlignCenter)
        le.setReadOnly(True)
        self.setLineEdit(le)
        self.lineEdit().setFont(QFont('楷体', 20))

    def myListWidget(self):
        listWgt = QListWidget()  # 列表框右对齐
        for item in self.items:
            listWgtItem = QListWidgetItem(item)
            listWgtItem.setTextAlignment(Qt.AlignCenter)
            listWgtItem.setFont(QFont('楷体', 20))
            listWgt.addItem(listWgtItem)
        self.setModel(listWgt.model())
        self.setView(listWgt)

    def changeItems(self,items):
        self.items = items
        self.myListWidget()


class test(QWidget):
    def __init__(self):
        super(test, self).__init__()
        self.a = MyRunButton()
        self.a.setParent(self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = test()
    win.show()
    sys.exit(app.exec_())
