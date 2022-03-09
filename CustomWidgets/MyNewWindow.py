import sys

from PyQt5.QtCore import QRect
from PyQt5.QtGui import QIcon, QPalette, QColor
from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QLineEdit, QMainWindow, QApplication, QFrame, \
    QVBoxLayout, QHBoxLayout, QGridLayout

from CustomWidgets import Fundsettings


class demo(QPushButton):
    def __init__(self):
        super(demo, self).__init__()


class SettingDialog(QWidget):
    # 对话框基类
    def __init__(self):
        super(SettingDialog, self).__init__()
        self.mainLayout = QVBoxLayout()

        self.titleLayout = QHBoxLayout()
        self.titleWidget = QWidget()
        self.titleLabel = QLabel("title")
        self.titleInput = QLineEdit()

        self.detailLayout = QHBoxLayout()
        self.detailWidget = QWidget()
        self.detailLabel = QLabel("details")
        self.detailInput = QLineEdit()

        self.childOptionListWidget = QWidget()
        self.childOptionListLayout = QGridLayout()

        self.childOption = QLabel('childOption')

        self.operationOptionsWidget = QWidget()
        self.operationOptionsLayout = QGridLayout()

        self.mySettings()
        self.myLayouts()

        # test
        self.addChildClass('hello')
        self.addChildClass('hello')
        self.addChildClass('hello')
        self.addChildClass('hello')
        self.addChildClass('hello')
        self.addChildClass('hello')

    def mySettings(self):
        self.resize(400, 500)

    def myLayouts(self):
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.mainLayout)

        self.mainLayout.addStretch(0)

        self.titleWidget.setContentsMargins(0, 0, 0, 0)
        self.titleLayout.setContentsMargins(0, 0, 0, 0)
        self.titleWidget.setLayout(self.titleLayout)
        self.titleLayout.addWidget(self.titleLabel)
        self.titleLayout.addWidget(self.titleInput)
        self.titleLayout.setStretch(0, 3)
        self.titleLayout.setStretch(1, 7)
        self.mainLayout.addWidget(self.titleWidget)

        self.detailWidget.setContentsMargins(0, 0, 0, 0)
        self.detailLayout.setContentsMargins(0, 0, 0, 0)
        self.detailWidget.setLayout(self.detailLayout)
        self.detailLayout.addWidget(self.detailLabel)
        self.detailLayout.addWidget(self.detailInput)
        self.detailLayout.setStretch(0, 3)
        self.detailLayout.setStretch(1, 7)
        self.mainLayout.addWidget(self.detailWidget)

        self.addHorizontalLine()

        # 加进去了但没有内容物填充
        self.childOptionListWidget.setContentsMargins(0, 0, 0, 0)
        self.childOptionListLayout.setContentsMargins(0, 0, 0, 0)
        self.childOptionListWidget.setLayout(self.childOptionListLayout)
        self.mainLayout.addWidget(self.childOptionListWidget)

        self.mainLayout.addWidget(self.childOption)

        self.operationOptionsLayout.setContentsMargins(0, 0, 0, 0)
        self.operationOptionsWidget.setContentsMargins(0, 0, 0, 0)
        self.operationOptionsWidget.setLayout(self.operationOptionsLayout)
        self.mainLayout.addWidget(self.operationOptionsWidget)

        self.mainLayout.addStretch(1)

    def addHorizontalLine(self):
        horizontalLine = QFrame()
        horizontalLine.setGeometry(QRect(0, 0, 10, 3))
        horizontalLine.setFrameShape(QFrame.HLine)
        horizontalLine.setFrameShadow(QFrame.Plain)
        horizontalLine.setContentsMargins(200, 0, 20, 0)
        self.mainLayout.addWidget(horizontalLine)

    def addChildClass(self, className):
        button = QPushButton(className)
        childNumber = len(self.childOptionListWidget.children()) - 1
        col = childNumber // 3
        row = childNumber % 3
        self.childOptionListLayout.addWidget(button, col, row)

    def addOperation(self, op):
        button = QPushButton(op)
        childNumber = len(self.childOptionListWidget.children()) - 1
        col = childNumber // 3
        row = childNumber % 3
        self.childOptionListLayout.addWidget(button, col, row)


class SingleClassButton(QPushButton):
    myWidth = 150
    myHeight = 100

    def __init__(self, title=None, workplace=None):
        super(SingleClassButton, self).__init__()
        self.title = title
        self.workplace = workplace
        self.myStyles()

    def myStyles(self):
        self.setContentsMargins(0, 0, 0, 0)
        self.resize(self.myWidth, self.myHeight)
        self.setText(self.title)
        self.setIcon(QIcon("%s/pic/minimizeButton.png" % Fundsettings.resource_path))
        self.setStyleSheet(
            "SingleClassButton{margin:-1px 0;background-color:transparent;height:40px;font-size:16px}"
            "SingleClassButton{font-size:16px;font_family:楷体;text-align:left;color:white}"
            "SingleClassButton:hover{background-color:rgba(150,150,150,0.5)}"
            "SingleClassButton:pressed{background-color:yellow}"
        )


class ClassList(QFrame):
    size_width = 150
    size_height = 600
    animDuring = 200
    bc_color = (90, 90, 90)

    def __init__(self):
        super(ClassList, self).__init__()
        self.mainLayout = QVBoxLayout()
        self.linearList_classical1 = SingleClassButton("线性表")
        self.linearList_classical2 = SingleClassButton("线性表2")

        self.linearList_classical3 = SingleClassButton("二叉树(基本)")

        self.mySettings()
        self.myLayouts()
        self.myStyles()

    def mySettings(self):
        self.resize(self.size_width, self.size_height)
        self.setContentsMargins(0, 20, 0, 0)

    def myLayouts(self):
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.mainLayout.setSpacing(0)
        self.setLayout(self.mainLayout)
        self.mainLayout.addStretch(0)
        self.mainLayout.addWidget(self.linearList_classical1)
        self.mainLayout.addWidget(self.linearList_classical2)
        self.addSpliter()
        self.mainLayout.addWidget(self.linearList_classical3)
        self.mainLayout.addStretch(1)

    def myStyles(self):
        self.setAutoFillBackground(True)
        palette = QPalette()
        palette.setBrush(QPalette.Background, QColor(*self.bc_color))
        self.setPalette(palette)

    def addSpliter(self):
        horizontalLine = QFrame()
        horizontalLine.setGeometry(QRect(0, 0, 10, 3))
        horizontalLine.setFrameShape(QFrame.HLine)
        horizontalLine.setFrameShadow(QFrame.Plain)
        horizontalLine.setContentsMargins(200, 0, 20, 0)
        self.mainLayout.addWidget(horizontalLine)


class MyNewWindow(QMainWindow):
    def __init__(self):
        super(MyNewWindow, self).__init__()
        self.setLayout(QHBoxLayout())
        self.classList = ClassList()
        self.classList.setParent(self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # win = MyNewWindow()
    win = SettingDialog()
    win.show()
    sys.exit(app.exec_())
