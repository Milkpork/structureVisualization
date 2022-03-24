from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor, QPen, QColor

from CustomWidgets import MyNode, MyLine, MyView, MyCanvas


class Node_Graph(MyNode):
    in_limit = 9999
    out_limit = 9999

    def __init__(self, a, b, t, c, n):  # 分别为，位置x，位置y，文字，父画板
        super(Node_Graph, self).__init__(a, b, t, c, n)
        self.lineList = {"next": [], 'previous': []}
        self.hasVisited = False  # 未访问

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

    def delete(self):
        if self == self.canvas.headNode:
            self.canvas.headNode = None
        # 删除画布字典中的自己
        del self.canvas.nodeDic[self.name]

        if len(self.lineList['previous']) == 1:
            del self.canvas.lineDic[self.lineList['previous'][0].name]
            self.canvas.scene.removeItem(self.lineList['previous'][0])
            self.lineList['previous'][0].startNode.lineList['next'] = []
        if len(self.lineList['left']) == 1:
            del self.canvas.lineDic[self.lineList['left'][0].name]
            self.canvas.scene.removeItem(self.lineList['left'][0])
            self.lineList['left'][0].endNode.lineList['previous'] = []
        if len(self.lineList['right']) == 1:
            del self.canvas.lineDic[self.lineList['right'][0].name]
            self.canvas.scene.removeItem(self.lineList['right'][0])
            self.lineList['right'][0].endNode.lineList['previous'] = []
        self.canvas.scene.removeItem(self)  # 删除自身


class Line_Graph(MyLine):
    def __init__(self, sn=None, en=None, c=None, n=None, stlistName=None, edlistName=None):
        super(Line_Graph, self).__init__(sn, en, c, n, stlistName, edlistName)

    def rightMenu(self):
        self.menu.addAction('删除')

    def menuSlot(self, ac):
        if ac.text() == '删除':
            self.delete()


class View_Graph(MyView):
    def __init__(self, sc, canv):
        super(View_Graph, self).__init__(sc, canv)


class Canvas_Graph(MyCanvas):
    def __init__(self, workplace=None):
        super(Canvas_Graph, self).__init__(Node_Graph, Line_Graph, View_Graph, workplace)

    def ergodic(self, mode):
        # 遍历
        if self.headNode is None:  # 没有头节点
            print("no head node!")
            return
        nowNode = self.headNode
        queue = []
        tempList = []  # 广度优先零时列表
        self.workplace.logInfo.append("result : ")

        def depthFirst(node):  # 深度优先
            node.hasVisited = True
            queue.append(node)
            self.workplace.logInfo.append(f"{node.text.text()} ")
            if node.lineList["next"]:
                for line in node.lineList["next"]:
                    if not line.endNode.hasVisited:
                        queue.append(line)
                        depthFirst(line.endNode)

        def breadthFirst(node):  # 广度优先
            node.hasVisited = True
            queue.append(node)
            self.workplace.logInfo.append(f"{node.text.text()} ")
            for i in node.lineList["next"]:
                tempList.append(i)
            if tempList:
                line = tempList.pop(0)
                if not line.endNode.hasVisited:
                    queue.append(line)
                    breadthFirst(line.endNode)

        if mode == 0:
            depthFirst(nowNode)
        elif mode == 1:
            breadthFirst(nowNode)
        self.workplace.logInfo.append("\n>>> ")
        for i in queue:
            if type(i) == self.nodeType:
                i.hasVisited = False
        self.playAnim(queue)

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
