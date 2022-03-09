import re
import sys

from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QSizePolicy
from CustomWidgets import MyInfo, MyLogInfo, MyRunButton
from Structures.BinaryTree.BinaryTree_Canvas import Canvas_BinaryTree


class Info_LinearList(MyInfo):
    def __init__(self, title='test', edition='testEdition'):
        super(Info_LinearList, self).__init__(title, edition)


class LogInfo_LinearList(MyLogInfo):
    def __init__(self, canvas):
        super(LogInfo_LinearList, self).__init__(canvas)

    def proOrder(self, order):
        ls = order.split()
        if ls[0] == 'insert':
            self.getWorkplace().canvas.insert(ls[1:])  # 需要用到画板的插入函数
        elif ls[0] == 'help':
            self.append('\n1.(insert [num] [num] ... ) can insert')
            self.append('\n2.more are going to append...')
        else:
            self.append('\nno such order')


# insert 1 2 3 null null null null

class RunButton_LinearList(MyRunButton):
    def __init__(self, workplace):
        super(RunButton_LinearList, self).__init__(workplace)
        self.changeItems(['新建', '先序遍历', '中序遍历', '后序遍历'])

    def menuSlot(self, t):
        if self.flag == 0:
            self.flag = 1
            return
        if t == '先序遍历':
            self.getWorkplace().canvas.ergodic(1)
        elif t == '中序遍历':
            self.getWorkplace().canvas.ergodic(2)
        elif t == '后序遍历':
            self.getWorkplace().canvas.ergodic(3)
        elif t == '新建':
            self.getWorkplace().canvas.scene.addItem(self.getWorkplace().canvas.addNode())
            self.getWorkplace().canvas.nodeCount += 1


class WorkPlace(QWidget):

    def __init__(self, t='Canvas', te='二叉树'):  # 参数为text和textEdition
        super(WorkPlace, self).__init__()

        self.title = t
        self.textEdition = te

        # 组件
        self.info = Info_LinearList(self.title, self.textEdition)
        self.canvas = Canvas_BinaryTree(self)
        self.runButton = RunButton_LinearList(self)
        self.logInfo = LogInfo_LinearList(self)

        self.mainWidget = QWidget()
        self.mainLayout = QHBoxLayout()  # 主布局，分割输入框

        self.myWidget2 = QWidget()
        self.layout2 = QVBoxLayout()  # 二层布局，分割画布

        self.myWidget3 = QWidget()
        self.layout3 = QHBoxLayout()  # 三级布局，分割按钮和信息

        # 函数
        self.myLayouts()
        self.mySettings()

    def myLayouts(self):
        self.setLayout(self.mainLayout)

        self.mainLayout.addWidget(self.myWidget2)
        self.myWidget2.setLayout(self.layout2)
        self.mainLayout.addWidget(self.logInfo)
        self.mainLayout.setSpacing(30)

        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(7)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.myWidget2.sizePolicy().hasHeightForWidth())
        self.myWidget2.setSizePolicy(sizePolicy)

        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(3)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.logInfo.sizePolicy().hasHeightForWidth())
        self.logInfo.setSizePolicy(sizePolicy1)

        self.layout2.addWidget(self.myWidget3)
        self.myWidget3.setLayout(self.layout3)
        self.layout2.addWidget(self.canvas)
        self.layout2.setSpacing(20)

        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.myWidget3.sizePolicy().hasHeightForWidth())
        self.myWidget3.setSizePolicy(sizePolicy)

        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(7)
        sizePolicy1.setHeightForWidth(self.canvas.sizePolicy().hasHeightForWidth())
        self.canvas.setSizePolicy(sizePolicy1)

        self.layout3.addWidget(self.info)
        self.layout3.addWidget(self.runButton)

    def mySettings(self):
        self.resize(800, 600)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.layout2.setContentsMargins(20, 0, 0, 20)
        self.layout3.setContentsMargins(0, 0, 0, 0)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = WorkPlace('canvas', 'BinaryTree')
    win.show()
    sys.exit(app.exec_())
