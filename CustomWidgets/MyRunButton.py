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
    def __init__(self, canvas=None):
        super(MyRunButton, self).__init__()
        self.setStyleSheet(
            "MyRunButton{background-color:#fff;border:1px solid black;}"

            "QComboBox::drop-down {border-left:1px solid black;width: 40px;margin:0;}"  # 箭头宽度需要设置按钮的边框才生效
            "QComboBox::down-arrow {image: url(E:/structureVisualization/mySources/pic/down.png);height:30px;width:20px;}"
            "MyRunButton QAbstractItemView{outline:0px;}"
            "MyRunButton QAbstractItemView::item{height:60px;border-radius:2px;outline:0px;}"  # 高度
            "MyRunButton QAbstractItemView::item:selected{background-color:#fff;color:black}"  # 选中样式
            "MyRunButton QAbstractItemView::item:hover{background-color:#fff;color:black;border:1px solid black}"
        )
        self.flag = 0
        self.items = ['test1', 'test2', 'test3', 'test4']
        self.canvas = canvas
        self.myLineEdit()  # 设置文本框
        self.myListWidget()  # 设置下拉框

        self.mySettings()
        self.mySignalConnections()
        self.myStyles()

    def mySettings(self):
        self.resize(150, 40)
        self.setMaximumSize(150, 40)
        self.setContentsMargins(0, 0, 0, 0)

    def mySignalConnections(self):
        self.lineEdit().clicked.connect(self.menuSlot)
        self.currentIndexChanged.connect(lambda: self.menuSlot(self.currentText()))

    def myStyles(self):
        self.view().window().setWindowFlags(Qt.Popup | Qt.FramelessWindowHint | Qt.NoDropShadowWindowHint)
        self.view().window().setAttribute(Qt.WA_TranslucentBackground)

    def menuSlot(self, t):
        """
        通过t来判断点击哪个按钮
        :param t:
        :return:
        """
        print(t)
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

    def changeItems(self, items):
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
