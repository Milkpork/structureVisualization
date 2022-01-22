import sys

from PyQt5.QtWidgets import QInputDialog

from myWidgets.myCanvas import myCanvas
from myWidgets.myNode import myNode


class NodeTest(myNode):
    def __init__(self, widget=None, v=0):
        """
        初始化: NodeTest() / NodeTest(int)
        :param v: 为该节点的值，默认为0
        """
        super(NodeTest, self).__init__(widget)
        self.value = v
        self.nextNode = None

        self.setText(str(self.value))

    def rightMenu(self):
        self.addMenuAction('连线')
        self.addMenuSpliter()
        self.addMenuAction('删除')

    def moveEvent(self, event):
        if self.pos().x() < 0:
            self.setGeometry(0, self.pos().y(), 80, 80)
        elif self.pos().x() > self.canvas.width() - self.width():
            self.setGeometry(self.canvas.width() - self.width(), self.pos().y(), 80, 80)
        elif self.pos().y() < 0:
            self.setGeometry(self.pos().x(), 0, 80, 80)
        elif self.pos().y() > self.canvas.height() - self.height():
            self.setGeometry(self.pos().x(), self.canvas.height() - self.height(), 80, 80)

    def menuSlot(self, act):
        """
        摆大烂函数2号
        :param act:
        :return:
        """
        print(act.text())
        if act.text() == '删除':
            self.setVisible(False)

    def mouseDoubleClickEvent(self, event):
        """
        暂时用这个，不太好看，凑合着用
        摆大烂
        """
        v, ok = QInputDialog.getInt(self, '整数输入框', '请输入值(0-100)', min=0, max=100)
        if v and ok:
            self.value = v
            self.setText(str(v))


class CanvasTest(myCanvas):
    def __init__(self):
        super(CanvasTest, self).__init__()
        self.title = "线性表"
        self.nodeDic = dict()
        self.nodeCount = 0

    def myRightMenu(self):
        self.menu.addMenuAction('新建')
        self.menu.addMenuSpliter()
        self.menu.addMenuAction('test')

    def showUi(self):
        self.nodeDic["button" + str(self.nodeCount)] = NodeTest(self, self.nodeCount)
        self.nodeDic["button" + str(self.nodeCount)].move(20 * self.nodeCount, 0)
        return self.nodeDic["button" + str(self.nodeCount)]

    def menuSlot(self, ac):
        if ac.text() == '新建':
            self.showUi().setVisible(True)
            self.nodeCount += 1
