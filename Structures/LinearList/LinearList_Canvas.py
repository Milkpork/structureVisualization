from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor, QPen, QColor

from CustomWidgets import MyNode, MyLine, MyView, MyCanvas


class Node_LinearList(MyNode):
    in_limit = 1
    out_limit = 1

    def __init__(self, a, b, t, c, n):  # 分别为，位置x，位置y，文字，父画板
        super(Node_LinearList, self).__init__(a, b, t, c, n)
        self.lineList = {'next': [], 'previous': []}

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        if self.canvas.cursor() == QCursor(Qt.CrossCursor):
            self.canvas.tempEd = self
            self.canvas.addLine(self.canvas.tempSt, self.canvas.tempEd, 'next', 'previous')

    def rightMenu(self):
        self.menu.addAction('删除')
        self.menu.addSeparator()
        self.menu.addAction('连线')
        self.menu.addSeparator()
        self.menu.addAction('设置头节点')

    def menuSlot(self, ac):
        if ac.text() == '连线':
            self.canvas.setCursor(QCursor(Qt.CrossCursor))
            self.canvas.tempSt = self
        elif ac.text() == '设置头节点':
            self.canvas.setHeadNode(self)
        elif ac.text() == '删除':
            self.delete()

    # !!!
    def delete(self):
        if self == self.canvas.headNode:
            self.canvas.headNode = None
        # 删除画布字典中的自己
        del self.canvas.nodeDic[self.name]

        if len(self.lineList['previous']) == 1:
            del self.canvas.lineDic[self.lineList['previous'][0].name]
            self.canvas.scene.removeItem(self.lineList['previous'][0])
            self.lineList['previous'][0].startNode.lineList['next'] = []
        if len(self.lineList['next']) == 1:
            del self.canvas.lineDic[self.lineList['next'][0].name]
            self.canvas.scene.removeItem(self.lineList['next'][0])
            self.lineList['next'][0].endNode.lineList['previous'] = []
        self.canvas.scene.removeItem(self)  # 删除自身


class Line_LinearList(MyLine):
    def __init__(self, sn=None, en=None, c=None, n=None, stlistName=None, edlistName=None):
        super(Line_LinearList, self).__init__(sn, en, c, n, stlistName, edlistName)

    def rightMenu(self):
        self.menu.addAction('删除')
        self.menu.addSeparator()
        self.menu.addAction('反转')

    def menuSlot(self, ac):
        if ac.text() == '删除':
            self.delete()


class View_LinearList(MyView):
    def __init__(self, sc, canv):
        super(View_LinearList, self).__init__(sc, canv)


class Canvas_LinearList(MyCanvas):
    def __init__(self, workplace=None):
        super(Canvas_LinearList, self).__init__(Node_LinearList, Line_LinearList, View_LinearList, workplace)

    def ergodic(self):
        # 遍历
        if self.headNode is None:  # 没有头节点
            self.workplace.logInfo.append('\nno head node！\n>>> ')
            return

        nowNode = self.headNode
        queue = []
        self.workplace.logInfo.append("result : ")
        while True:
            # 插入动画
            self.workplace.logInfo.append(f'{nowNode.text.text()} ')
            queue.append(nowNode)
            if len(nowNode.lineList['next']) <= 0:
                break
            queue.append(nowNode.lineList['next'][0])
            nowNode = nowNode.lineList['next'][0].endNode
            # 循环链表防止死循环
            if nowNode == self.headNode:
                break
        self.workplace.logInfo.append("\n>>> ")

        self.playAnim(queue)

    def insert(self, ls):
        st = self.nodeCount
        for i in ls:
            self.addNode(i)
        for i in range(st, self.nodeCount - 1):
            self.addLine(self.nodeDic[f"node{str(i)}"],
                         self.nodeDic[f"node{str(i + 1)}"],
                         "next",
                         "previous")

    def clear(self, nodeList=None, lineList=None):
        # 恢复最初样式
        if lineList is None:
            lineList = []
        if nodeList is None:
            nodeList = []
        self.setCursor(QCursor(Qt.ArrowCursor))
        self.tempSt = None
        self.tempEd = None
        for node in nodeList:
            node.setPen(QPen(Qt.black, 2))
            node.setScale(1)
        for line in lineList:
            pen = QPen()
            pen.setColor(Qt.black)
            pen.setWidth(2)
            line.setPen(pen)
        if self.headNode is not None:
            self.headNode.setPen(QPen(QColor(255, 165, 0), 2))

    def format(self):
        flag = 1
        nowPos = [0, 0]
        if self.headNode is None:
            return
        nowNode = self.headNode
        while True:
            nowNode.setPos(*nowPos)
            nowNode.init_pos = nowNode.pos()
            if flag == 1:
                nowPos[0] = nowPos[0] + flag * self.nodeType.size * 2
                if nowPos[0] > self.size:
                    flag = -1
                    nowPos[0] = nowPos[0] + flag * self.nodeType.size * 2
                    nowPos[1] = nowPos[1] - flag * self.nodeType.size * 2
            elif flag == -1:
                nowPos[0] = nowPos[0] + flag * self.nodeType.size * 2
                if nowPos[0] < 0:
                    flag = 1
                    nowPos[0] = nowPos[0] + flag * self.nodeType.size * 2
                    nowPos[1] = nowPos[1] + flag * self.nodeType.size * 2

            for i in nowNode.lineList:
                for j in nowNode.lineList[i]:
                    j.changePos()
            self.view.viewport().update()
            if len(nowNode.lineList['next']) == 0:
                break
            else:
                nowNode = nowNode.lineList['next'][0].endNode
