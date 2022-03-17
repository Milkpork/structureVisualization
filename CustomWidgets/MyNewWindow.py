import sys

from PyQt5.QtCore import QRect, Qt, pyqtSignal
from PyQt5.QtGui import QIcon, QPalette, QColor, QPainter, QFont
from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QLineEdit, QMainWindow, QApplication, QFrame, \
    QVBoxLayout, QHBoxLayout, QGridLayout, QStyleOption, QStyle

from CustomWidgets import Fundsettings, MyTopBar


# 提交按钮
class SubmitButton(QPushButton):
    def __init__(self, text: str):
        super(SubmitButton, self).__init__(text)
        self.setStyleSheet(
            "SubmitButton {color:black;background-color: #884;border:1px solid black;}"
            "SubmitButton:pressed{background-color:red}"
        )

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)


# 关闭按钮
class CloseButton(QPushButton):
    def __init__(self):
        super(CloseButton, self).__init__()


# 功能选择项
class OperationsOptionsButton(QPushButton):
    def __init__(self, text=''):
        super(OperationsOptionsButton, self).__init__(text)
        self.hasSelected = False
        self.setStyleSheet(
            "OperationsOptionsButton {border:2px solid gray;background-color:transparent;border-radius:6px}"
        )
        self.setContentsMargins(0, 0, 0, 0)
        self.setFixedSize(80, 50)

    def changeStyle(self):
        if not self.hasSelected:
            self.setStyleSheet(
                "OperationsOptionsButton {border:2px solid gray;background-color:rgba(150, 150, 150,1);border-radius:6px}"
            )
        else:
            self.setStyleSheet(
                "OperationsOptionsButton {border:2px solid gray;background-color:transparent;border-radius:6px}"
            )
        self.hasSelected = not self.hasSelected


class OperationOptionsWidget(QWidget):
    def __init__(self):
        super(OperationOptionsWidget, self).__init__()
        self.nowSelectedOption = []  # 记录了选择哪些

    def mySignalConnections(self):
        for option in self.children():
            if type(option) == OperationsOptionsButton:
                option.clicked.connect(self.changeNowOption)

    def changeNowOption(self):
        nowOption = self.sender()
        nowOption.changeStyle()
        if nowOption in self.nowSelectedOption:
            self.nowSelectedOption.remove(nowOption)
        else:
            self.nowSelectedOption.append(nowOption)


# 小类选择项
class ClassOptionsButton(QPushButton):
    def __init__(self, text=""):
        super(ClassOptionsButton, self).__init__(text)
        self.hasSelected = 0
        self.setStyleSheet(
            "ClassOptionsButton {background-color:transparent;border-radius:6px;border:2px solid gray;}"
        )
        self.setContentsMargins(0, 0, 0, 0)
        self.setFixedSize(80, 50)

    def changeStyle(self):
        if not self.hasSelected:
            self.setStyleSheet(
                "ClassOptionsButton {background-color:rgba(150, 150, 150,1);border-radius:6px;border:2px solid gray;}"
            )
        else:
            self.setStyleSheet(
                "ClassOptionsButton {background-color:transparent;border-radius:6px;border:2px solid gray;}"
            )
        self.hasSelected = not self.hasSelected


class ChildOptionListWidget(QWidget):
    def __init__(self):
        super(ChildOptionListWidget, self).__init__()
        self.nowSelectedOption = None  # 记录了选择哪项
        self.setContentsMargins(500, 0, 50, 0)
        self.mySignalConnections()

    def mySignalConnections(self):
        for option in self.children():
            if type(option) == ClassOptionsButton:
                option.clicked.connect(self.changeNowOption)

    def changeNowOption(self):
        nowOption = self.sender()
        if nowOption == self.nowSelectedOption:
            nowOption.changeStyle()
            self.nowSelectedOption = None
            return
        if self.nowSelectedOption is not None:
            self.nowSelectedOption.changeStyle()
        self.nowSelectedOption = nowOption
        nowOption.changeStyle()


# 输入框
class InputWidget(QWidget):
    def __init__(self, inputs):
        super(InputWidget, self).__init__()
        self.inputs = inputs
        self.setStyleSheet(
            "InputWidget{background:transparent;}"
            "InputWidget:hover{background:rgba(155,155,155,.7);}"
        )

    def mouseReleaseEvent(self, event):
        super(InputWidget, self).mouseReleaseEvent(event)
        self.inputs.setFocus()

    def paintEvent(self, event):
        opt = QStyleOption()
        opt.initFrom(self)
        p = QPainter(self)
        self.style().drawPrimitive(QStyle.PE_Widget, opt, p, self)

    def text(self):
        return self.inputs.text()


class InputEdit(QLineEdit):
    def __init__(self):
        super(InputEdit, self).__init__()
        self.setStyleSheet(
            "InputEdit{background-color: transparent;border:2px solid #8B8970;height:25px;}"
        )
        self.setAlignment(Qt.AlignRight)

    def focusInEvent(self, event):
        self.setStyleSheet(
            "InputEdit{background-color: transparent;border:2px solid #EEE5DE;height:25px;}"
        )

    def focusOutEvent(self, event):
        super().focusOutEvent(event)
        self.setStyleSheet(
            "InputEdit{background-color: transparent;border:2px solid #8B8970;height:25px;}"

        )


class SettingDialog(QWidget):
    submitted = pyqtSignal(dict)

    # 对话框基类
    def __init__(self):
        super(SettingDialog, self).__init__()
        self.setStyleSheet(
            "QWidget{color:rgba(224,255,255,1)}"

        )

        self.mainLayout = QVBoxLayout()

        self.titleLayout = QHBoxLayout()
        self.titleLabel = QLabel("title")
        self.titleInput = InputEdit()
        self.titleWidget = InputWidget(self.titleInput)

        self.detailLayout = QHBoxLayout()
        self.detailLabel = QLabel("details")
        self.detailInput = InputEdit()
        self.detailWidget = InputWidget(self.detailInput)

        self.childOptionWapper = QWidget()
        self.childOptionWapperLayout = QVBoxLayout()
        self.childLabel = QLabel('请选择子类')
        self.childOptionListWidget = ChildOptionListWidget()
        self.childOptionListLayout = QGridLayout()

        self.operationOptionsWapper = QWidget()
        self.operationOptionsWapperLayout = QVBoxLayout()
        self.operationLabel = QLabel('请添加需要的功能')
        self.operationOptionsWidget = OperationOptionsWidget()
        self.operationOptionsLayout = QGridLayout()

        self.buttonWapper = QWidget()
        self.buttonWapperLayout = QHBoxLayout()
        self.submitButton = SubmitButton("submit")
        self.closeButton = SubmitButton("close")

        self.mySettings()
        self.myLayouts()
        self.mySignalConnections()

    def mySettings(self):
        self.resize(450, 500)
        self.setAutoFillBackground(True)
        palette = QPalette()
        palette.setBrush(QPalette.Background, QColor(30, 34, 40))
        self.setPalette(palette)

    def myLayouts(self):
        font_size = 16  # 字体大小
        self.mainLayout.setSpacing(20)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.mainLayout)

        self.mainLayout.addStretch(0)

        self.titleLabel.setFont(QFont(Fundsettings.font_family, font_size))

        self.titleWidget.setContentsMargins(20, 0, 20, 0)
        self.titleLayout.setContentsMargins(0, 0, 0, 0)
        self.titleWidget.setLayout(self.titleLayout)
        self.titleLayout.addWidget(self.titleLabel)
        self.titleLayout.addWidget(self.titleInput)
        self.titleLayout.setStretch(0, 3)
        self.titleLayout.setStretch(1, 7)
        self.mainLayout.addWidget(self.titleWidget)

        self.detailLabel.setFont(QFont(Fundsettings.font_family, font_size))

        self.detailWidget.setContentsMargins(20, 0, 20, 0)
        self.detailLayout.setContentsMargins(0, 0, 0, 0)
        self.detailWidget.setLayout(self.detailLayout)
        self.detailLayout.addWidget(self.detailLabel)
        self.detailLayout.addWidget(self.detailInput)
        self.detailLayout.setStretch(0, 3)
        self.detailLayout.setStretch(1, 7)
        self.mainLayout.addWidget(self.detailWidget)

        self.addHorizontalLine()

        self.mainLayout.addWidget(self.childOptionWapper)
        self.childOptionWapper.setContentsMargins(20, 0, 20, 20)
        self.childOptionWapperLayout.setContentsMargins(0, 0, 0, 0)
        self.childOptionWapper.setLayout(self.childOptionWapperLayout)
        self.childOptionWapperLayout.addWidget(self.childLabel)
        self.childOptionListWidget.setContentsMargins(0, 0, 0, 0)
        self.childOptionListLayout.setContentsMargins(0, 0, 0, 0)
        self.childOptionListWidget.setLayout(self.childOptionListLayout)
        self.childOptionWapperLayout.addWidget(self.childOptionListWidget)

        self.mainLayout.addWidget(self.operationOptionsWapper)
        self.operationOptionsWapper.setContentsMargins(20, 0, 20, 20)
        self.operationOptionsWapperLayout.setContentsMargins(0, 0, 0, 0)
        self.operationOptionsWapper.setLayout(self.operationOptionsWapperLayout)
        self.operationOptionsWapperLayout.addWidget(self.operationLabel)
        self.operationOptionsWidget.setContentsMargins(0, 0, 0, 0)
        self.operationOptionsLayout.setContentsMargins(0, 0, 0, 0)
        self.operationOptionsWidget.setLayout(self.operationOptionsLayout)
        self.operationOptionsWapperLayout.addWidget(self.operationOptionsWidget)

        self.submitButton.setFixedSize(100, 50)
        self.closeButton.setFixedSize(100, 50)
        self.buttonWapper.setLayout(self.buttonWapperLayout)
        self.buttonWapper.setContentsMargins(0, 0, 0, 0)
        self.buttonWapperLayout.setContentsMargins(0, 0, 0, 0)
        self.buttonWapperLayout.addWidget(self.submitButton)
        self.buttonWapperLayout.addWidget(self.closeButton)

        self.mainLayout.addWidget(self.buttonWapper)
        self.mainLayout.addStretch(0)

    def mySignalConnections(self):
        self.submitButton.clicked.connect(self.submitButtonEvent)
        self.closeButton.clicked.connect(self.closeButtonEvent)

    def addHorizontalLine(self):
        horizontalLine = QFrame()
        horizontalLine.setGeometry(QRect(0, 0, 10, 3))
        horizontalLine.setFrameShape(QFrame.HLine)
        horizontalLine.setFrameShadow(QFrame.Plain)
        horizontalLine.setStyleSheet(
            "QFrame{margin: 0px 40px 0px 40px;color:white;}"
        )
        self.mainLayout.addWidget(horizontalLine)

    def addChildClass(self, className: str):
        maxSize = 4
        button = ClassOptionsButton(className)
        childNumber = len(self.childOptionListWidget.children()) - 1
        col = childNumber // maxSize
        row = childNumber % maxSize
        self.childOptionListLayout.addWidget(button, col, row)
        button.setParent(self.childOptionListWidget)

    def setChildrenClass(self, classNames: list):
        for i in classNames:
            self.addChildClass(i)
        self.childOptionListWidget.mySignalConnections()

    def addOperation(self, op: str):
        button = OperationsOptionsButton(op)
        childNumber = len(self.operationOptionsWidget.children()) - 1
        col = childNumber // 3
        row = childNumber % 3
        self.operationOptionsLayout.addWidget(button, col, row)
        button.setParent(self.operationOptionsWidget)

    def setOperations(self, operations: list):
        for op in operations:
            self.addOperation(op)
        self.operationOptionsWidget.mySignalConnections()

    def submitButtonEvent(self):
        self.getInfo(self)
        # wind = self.parent()
        # while type(wind) != MyNewWindow:
        #     wind = wind.parent()
        # else:
        #     wind.close()

    def closeButtonEvent(self):
        print("close")
        wind = self.parent()
        while type(wind) != MyNewWindow:
            wind = wind.parent()
        # self.parent().parent().parent().close()
        else:
            wind.close()

    def closeEvent(self, event):
        super().closeEvent(event)
        print("close2")

    def getInfo(self, dia):
        infoDic = {"title": dia.titleInput.text(),
                   "detail": dia.detailInput.text(),
                   "class": None if dia.childOptionListWidget.nowSelectedOption is None else dia.childOptionListWidget.nowSelectedOption.text(),
                   "options": [i.text() for i in dia.operationOptionsWidget.nowSelectedOption]
                   }
        self.submitted.emit(infoDic)


# #############################################################

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
            "SingleClassButton{margin:-1px 0;background-color:transparent;height:40px;border:1px solid transparent}"
            "SingleClassButton{font-size:16px;font_family:楷体;text-align:left;color:white}"
            "SingleClassButton:pressed{background-color:yellow}"
        )

    def setWorkplace(self, workplace):
        self.workplace = workplace

    def workplaceDisplay(self):
        self.setStyleSheet(
            "SingleClassButton{margin:-1px 0;background-color:yellow;height:40px;border:1px solid transparent}"
            "SingleClassButton{font-size:16px;font_family:楷体;text-align:left;color:white}"
            "SingleClassButton:pressed{background-color:yellow}"
        )
        if self.workplace is not None:
            self.workplace.raise_()

    def resumeWorkplace(self):
        self.setStyleSheet(
            "SingleClassButton{margin:-1px 0;background-color:transparent;height:40px;border:1px solid transparent}"
            "SingleClassButton{font-size:16px;font_family:楷体;text-align:left;color:white}"
            "SingleClassButton:pressed{background-color:yellow}"
        )


class ClassList(QFrame):
    size_width = 150
    size_height = 500
    animDuring = 200
    bc_color = (120, 90, 90)

    def __init__(self):
        super(ClassList, self).__init__()

        self.nowTab = None

        self.mainLayout = QVBoxLayout()
        self.mySettings()
        self.myLayouts()
        self.myStyles()

    def mySettings(self):
        self.setFixedSize(self.size_width, self.size_height)
        self.setContentsMargins(0, 20, 0, 0)

    def myLayouts(self):
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.mainLayout.setSpacing(0)
        self.setLayout(self.mainLayout)
        self.mainLayout.addStretch(0)
        self.mainLayout.addStretch(1)

    def myStyles(self):
        self.setAutoFillBackground(True)
        palette = QPalette()
        palette.setBrush(QPalette.Background, QColor(*self.bc_color))
        self.setPalette(palette)

    @staticmethod
    def addSpliter():
        horizontalLine = QFrame()
        horizontalLine.setGeometry(QRect(0, 0, 10, 3))
        horizontalLine.setFrameShape(QFrame.HLine)
        horizontalLine.setFrameShadow(QFrame.Plain)
        horizontalLine.setContentsMargins(200, 0, 20, 0)
        return horizontalLine

    def addTabButton(self, tab):
        self.mainLayout.insertWidget(0, tab)
        if type(tab) == SingleClassButton:
            tab.clicked.connect(self.funClick)

    def funClick(self):
        button = self.sender()
        if self.nowTab is not None:
            self.nowTab.resumeWorkplace()
        self.nowTab = button
        button.workplaceDisplay()


class SingleTab:
    def __init__(self, tabName, classList, operationList):
        self.tab = SingleClassButton(tabName)
        self.dialog = SettingDialog()

        self.dialog.setChildrenClass(classList)
        self.dialog.setOperations(operationList)
        self.tab.setWorkplace(self.dialog)

    def getTab(self):
        return self.tab

    def getDialog(self):
        return self.dialog


class MyNewWindow(QMainWindow):
    def __init__(self):
        super(MyNewWindow, self).__init__()
        self.setWindowModality(Qt.ApplicationModal)
        self.mainbody = QWidget()
        self.mainbodyLayout = QVBoxLayout()
        self.topbar = MyTopBar(self, [0, 0, 0, 1])

        self.mainWidget = QWidget()
        self.mainLayout = QHBoxLayout()
        self.nav = ClassList()
        self.diaWapper = QWidget()

        self.tab1 = SingleTab('线性表', ["普通线性表", "双向", "c"], ["d", 'e', 'f', 'g'])
        self.tab2 = SingleTab('线性表2', ["普通线性表2", "双向2", "c2"], ["da", 'ea', 'f', 'g'])

        self.mySettings()
        self.myLayouts()
        self.mySignalConnections()
        self.show()

    def mySettings(self):
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setFixedSize(600, 540)

    def myLayouts(self):
        self.setCentralWidget(self.mainbody)
        self.mainbody.setContentsMargins(0, 0, 0, 0)
        self.mainbodyLayout.setContentsMargins(0, 0, 0, 0)
        self.mainbody.setLayout(self.mainbodyLayout)
        self.mainbodyLayout.setSpacing(0)

        self.mainbodyLayout.addWidget(self.topbar)
        self.mainbodyLayout.addWidget(self.mainWidget)

        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.mainWidget.setLayout(self.mainLayout)
        self.mainLayout.setSpacing(0)
        self.mainLayout.setStretch(1, 3)
        self.mainLayout.addWidget(self.nav)
        self.diaWapper.setContentsMargins(0, 0, 0, 0)
        self.mainLayout.addWidget(self.diaWapper)

        # 倒着插入
        self.addDialog(self.tab1)
        self.nav.addTabButton(self.nav.addSpliter())
        self.addDialog(self.tab2)

    def mySignalConnections(self):
        self.tab1.getDialog().submitted.connect(lambda dic: self.submittedEvent(dic, self.tab1.getTab().text()))
        self.tab2.getDialog().submitted.connect(lambda dic: self.submittedEvent(dic, self.tab2.getTab().text()))

    def addDialog(self, tab):
        self.nav.addTabButton(tab.getTab())
        tab.getDialog().setParent(self.diaWapper)

    def submittedEvent(self, dic, tabname):
        print(self.sender())
        print(tabname)
        dic['name'] = tabname
        print(dic)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MyNewWindow()
    # win = SettingDialog()
    win.show()
    sys.exit(app.exec_())
