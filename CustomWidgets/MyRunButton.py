import sys

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QComboBox, QWidget, QApplication, QLineEdit, QListWidget, QListWidgetItem
from CustomWidgets.Fundsettings import Fundsettings, FundColor


# 输入框，即运行按钮的最前部按钮
class MyLineEdit(QLineEdit):
    default_style_color = FundColor.runButtonBackgroundColor
    click_style_color = FundColor.runButtonClickColor
    hover_style_color = FundColor.runButtonHoverColor

    clicked = pyqtSignal(str)

    def mouseReleaseEvent(self, QMouseEvent):
        self.setStyleSheet(
            "QLineEdit{background-color:%s;}" % self.hover_style_color
        )
        self.clicked.emit(self.text())

    def enterEvent(self, event):
        super().enterEvent(event)
        self.setStyleSheet(
            "QLineEdit{background-color:%s;}" % self.hover_style_color
        )

    def leaveEvent(self, event):
        super().leaveEvent(event)
        self.setStyleSheet(
            "QLineEdit{background-color:%s;}" % self.default_style_color
        )

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        self.setStyleSheet(
            "QLineEdit{background-color:%s;}" % self.click_style_color
        )

    def mouseDoubleClickEvent(self, QMouseEvent):
        super().mousePressEvent(QMouseEvent)
        self.setStyleSheet(
            "QLineEdit{background-color:%s;}" % self.click_style_color
        )

    # 右击，用于屏蔽右击菜单
    def contextMenuEvent(self, QContext):
        pass


# 运行按钮（主类）
class MyRunButton(QComboBox):
    font_size = 20  # 字体大小

    def __init__(self, workplace: QWidget = None):
        super(MyRunButton, self).__init__()
        self.setStyleSheet(
            "MyRunButton{border:1px solid black;border-radius:5px;background-color:transparent;}"
            "MyRunButton::drop-down {border-left:1px solid black;width: 40px;margin:0;}"  # 箭头宽度需要设置按钮的边框才生效
            "MyRunButton::down-arrow {image: url(:pic/down.png);height:30px;width:20px;}"
            "MyRunButton QAbstractItemView{outline:0px;border:1px solid black;background-color: %s;}"
            "MyRunButton QAbstractItemView::item{height:60px;outline:0px;}"  # 高度
            "MyRunButton QAbstractItemView::item:selected{background-color:%s;color:black}"  # 选中样式
            "MyRunButton QAbstractItemView::item:hover{background-color:%s;color:black;border-top:1px solid black;border-bottom:1px solid black}" % (
                FundColor.runButtonItemBackgroundColor, FundColor.runButtonItemHoverColor,
                FundColor.runButtonItemHoverColor)
        )
        self.flag = 0
        self.items = ['test1', 'test2', 'test3', 'test4']
        self.workplace = workplace
        self.myLineEdit()  # 设置文本框
        self.myListWidget()  # 设置下拉框

        self.mySettings()
        self.mySignalConnections()

    def mySettings(self):
        self.resize(150, 40)
        self.setMaximumSize(150, 40)
        self.setContentsMargins(0, 0, 0, 0)
        self.view().window().setWindowFlags(Qt.Popup | Qt.FramelessWindowHint | Qt.NoDropShadowWindowHint)  # 无边框/无阴影
        self.view().window().setAttribute(Qt.WA_TranslucentBackground)  # 透明

    def mySignalConnections(self):
        self.lineEdit().clicked.connect(self.menuSlot)
        self.currentIndexChanged.connect(lambda: self.menuSlot(self.currentText()))

    # 对输入框的修改
    def myLineEdit(self):
        le = MyLineEdit()
        le.setAlignment(Qt.AlignCenter)
        le.setReadOnly(True)
        self.setLineEdit(le)
        self.lineEdit().setFont(QFont(Fundsettings.font_family, self.font_size))

    # 对下拉菜单的设置
    def myListWidget(self):
        listWgt = QListWidget()  # 列表框右对齐
        for item in self.items:
            listWgtItem = QListWidgetItem(item)
            listWgtItem.setTextAlignment(Qt.AlignCenter)
            listWgtItem.setFont(QFont(Fundsettings.font_family, self.font_size))
            listWgt.addItem(listWgtItem)
        self.setModel(listWgt.model())
        self.setView(listWgt)

    # 触发选项，需要被重载
    def menuSlot(self, t: str):
        pass

    # 接口:用于修改列表的内容
    def changeItems(self, items: list):
        self.items = items
        self.myListWidget()

    # 接口:返回工作区
    def getWorkplace(self):
        return self.workplace


if __name__ == '__main__':
    class test(QWidget):
        def __init__(self):
            super(test, self).__init__()
            self.a = MyRunButton()
            self.a.setParent(self)


    app = QApplication(sys.argv)
    win = test()
    win.show()
    sys.exit(app.exec_())
