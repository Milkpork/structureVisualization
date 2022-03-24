import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QFrame, QVBoxLayout, QHBoxLayout, QApplication, QFileDialog

from CustomWidgets import Fundsettings, MyTab, MyTopBar


class MyButton(QPushButton):
    def __init__(self, text=""):
        super(MyButton, self).__init__(text)
        self.setStyleSheet(
            "MyButton{border:2px solid black;border-radius:10px;font-size:25px;font-family:%s}"
            "MyButton:hover{background-color:rgba(220,220,220,1)}" % (
                Fundsettings.font_family
            )

        )
        self.mySettings()

    def mySettings(self):
        self.setFixedSize(200, 120)


class Title(QLabel):
    def __init__(self, text):
        super(Title, self).__init__(text)
        self.setStyleSheet(
            "Title { font-size:40px;font-family:%s}" % (
                Fundsettings.font_family
            )
        )
        self.setAlignment(Qt.AlignCenter)


class WelcomeInterface(QFrame):
    def __init__(self, tab, window):
        super(WelcomeInterface, self).__init__()
        self.tab = tab
        self.myWindow = window
        self.mainLayout = QVBoxLayout()

        self.labelWidget = QWidget()
        self.labelLayout = QVBoxLayout()

        self.buttonWidget = QWidget()
        self.buttonLayout = QHBoxLayout()

        self.slogan = Title("欢迎, 点击以下按钮开始！")
        self.newButton = MyButton("新建")
        self.loadButton = MyButton("导入")

        self.myLayouts()
        self.mySettings()
        self.mySignalConnections()

    def mySettings(self):
        self.resize(800, 600)
        self.setContentsMargins(0, 0, 0, 0)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.labelWidget.setContentsMargins(0, 0, 0, 0)
        self.labelLayout.setContentsMargins(0, 0, 0, 0)
        self.buttonWidget.setContentsMargins(0, 0, 0, 0)
        self.buttonLayout.setContentsMargins(0, 0, 0, 0)

    def myLayouts(self):
        self.setLayout(self.mainLayout)
        self.mainLayout.addWidget(self.labelWidget)
        self.mainLayout.addWidget(self.buttonWidget)

        self.labelWidget.setLayout(self.labelLayout)
        self.buttonWidget.setLayout(self.buttonLayout)

        self.labelLayout.addWidget(self.slogan)

        self.buttonLayout.addWidget(self.newButton)
        self.buttonLayout.addWidget(self.loadButton)

    def mySignalConnections(self):
        self.newButton.clicked.connect(lambda: MyTab.addTab(self.tab))
        self.loadButton.clicked.connect(self.loadFunc)

    def loadFunc(self):
        try:
            fname, ok = QFileDialog.getOpenFileName(self, "选取文件", "./", "Text Files (*.stru)")
            if ok:
                orderDic = {}
                with open(fname, "r", encoding="utf8") as f:
                    content = f.readline()
                    while content:
                        order = content.rstrip("\n").split(" ", 1)
                        if len(order) < 2:
                            order += [""]
                        orderDic[order[0]] = order[1]
                        content = f.readline()

                types = orderDic['<type>']
                title = orderDic["<title>"]
                edition = orderDic["<edition>"]
                function = eval(orderDic["<functions>"])
                nodeDict = eval(orderDic["<node>"])
                connectDict = eval(orderDic["<connections>"])
                head = orderDic["<headNode>"]
                posDict = eval(orderDic["<positions>"])
                self.myWindow.nav.addTabAppoint(types, title, edition, function)
                canv = self.myWindow.nav.getNowWorkplace().canvas
                for i in nodeDict:
                    canv.addNode(nodeDict[i], posDict[i][0], posDict[i][1])
                for i in connectDict:
                    for j in connectDict[i]:
                        canv.addLine(canv.nodeDic[f"node{i}"], canv.nodeDic[f"node{j[0]}"], j[1], j[2])
                canv.setHeadNode(canv.nodeDic[f"node{head}"])
        except:
            pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = WelcomeInterface(None, None)
    win.show()
    sys.exit(app.exec_())
