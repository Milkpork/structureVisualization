from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor, QPen, QColor

from CustomWidgets import MyNode, MyLine, MyView, MyCanvas


class Node_BinaryTree(MyNode):
    in_limit = 1
    out_limit = 1

    def __init__(self, a, b, t, c, n):  # 分别为，位置x，位置y，文字，父画板
        super(Node_BinaryTree, self).__init__(a, b, t, c, n)
        self.lineList = {'left': [], 'right': [], 'previous': []}

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        if self.canvas.cursor() == QCursor(Qt.CrossCursor):
            self.canvas.tempEd = self
            if self.canvas.rightConnect == -1:
                self.canvas.addLine(self.canvas.tempSt, self.canvas.tempEd, 'left', 'previous')
            elif self.canvas.rightConnect == 1:
                self.canvas.addLine(self.canvas.tempSt, self.canvas.tempEd, 'right', 'previous')

    def rightMenu(self):
        self.menu.addAction('删除')
        self.menu.addSeparator()
        self.menu.addAction('连接左节点')
        self.menu.addAction('连接右节点')
        self.menu.addSeparator()
        self.menu.addAction('设置头节点')

    def menuSlot(self, ac):
        if ac.text() == '连接左节点':
            self.canvas.setCursor(QCursor(Qt.CrossCursor))
            self.canvas.tempSt = self
            self.canvas.rightConnect = -1
        elif ac.text() == '连接右节点':
            self.canvas.setCursor(QCursor(Qt.CrossCursor))
            self.canvas.tempSt = self
            self.canvas.rightConnect = 1
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


class Line_BinaryTree(MyLine):
    def __init__(self, sn=None, en=None, c=None, n=None, stlistName=None, edlistName=None):
        super(Line_BinaryTree, self).__init__(sn, en, c, n, stlistName, edlistName)

    def rightMenu(self):
        self.menu.addAction('删除')

    def menuSlot(self, ac):
        if ac.text() == '删除':
            self.delete()


class View_BinaryTree(MyView):
    def __init__(self, sc, canv):
        super(View_BinaryTree, self).__init__(sc, canv)


class Canvas_BinaryTree(MyCanvas):
    def __init__(self, workplace=None):
        super(Canvas_BinaryTree, self).__init__(Node_BinaryTree, Line_BinaryTree, View_BinaryTree, workplace)
        self.rightConnect = 0

    def ergodic(self, mode):
        # 遍历
        if self.headNode is None:  # 没有头节点
            print("no head node!")
            return
        nowNode = self.headNode
        queue = []
        self.workplace.logInfo.append("result : ")

        def ergodic_preorder(node):
            queue.append(node)
            self.workplace.logInfo.append(f"{node.text.text()} ")
            if len(node.lineList['left']) > 0:
                queue.append(node.lineList['left'][0])
                ergodic_preorder(node.lineList['left'][0].endNode)
            if len(node.lineList['right']) > 0:
                queue.append(node.lineList['right'][0])
                ergodic_preorder(node.lineList['right'][0].endNode)

        def ergodic_middle(node):
            if len(node.lineList['left']) > 0:
                queue.append(node.lineList['left'][0])
                ergodic_middle(node.lineList['left'][0].endNode)
            queue.append(node)
            self.workplace.logInfo.append(f"{node.text.text()} ")
            if len(node.lineList['right']) > 0:
                queue.append(node.lineList['right'][0])
                ergodic_middle(node.lineList['right'][0].endNode)

        def ergodic_postorder(node):
            if len(node.lineList['left']) > 0:
                queue.append(node.lineList['left'][0])
                ergodic_postorder(node.lineList['left'][0].endNode)
            if len(node.lineList['right']) > 0:
                queue.append(node.lineList['right'][0])
                ergodic_postorder(node.lineList['right'][0].endNode)
            queue.append(node)
            self.workplace.logInfo.append(f"{node.text.text()} ")

        if mode == 1:
            ergodic_preorder(nowNode)
        elif mode == 2:
            ergodic_middle(nowNode)
        elif mode == 3:
            ergodic_postorder(nowNode)
        self.workplace.logInfo.append("\n>>> ")

        self.playAnim(queue)

    def insert(self, ls):
        exceptList = ['null', '-1', 'Null', 'None']

        def fun(node, i, isRight=1):
            no = self.addNode(ls[i])
            if node is not None:
                self.lineDic["line" + str(self.lineCount)] = self.lineType(node,
                                                                           no,
                                                                           self,
                                                                           "line" + str(self.lineCount),
                                                                           "right" if isRight == 1 else "left",
                                                                           "previous")
                self.scene.addItem(self.lineDic["line" + str(self.lineCount)])
                self.lineCount += 1
            nodeindex = self.nodeCount - 1
            if i * 2 + 1 < len(ls) and ls[i * 2 + 1] not in exceptList:
                fun(self.nodeDic["node" + str(nodeindex)], i * 2 + 1, -1)
            if i * 2 + 2 < len(ls) and ls[i * 2 + 2] not in exceptList:
                fun(self.nodeDic["node" + str(nodeindex)], i * 2 + 2, 1)

        fun(None, 0, 1)

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
        nowPos = [self.size // 2, 0]
        if self.headNode is None:
            return
        h = self.getDepth()
        miniGap = 80
        initGap = 2 ** (h - 3) * miniGap
        nowNode = self.headNode

        nowNode.setPos(nowPos[0], nowPos[1])

        def setNowNodePos(node, posx, posy, devi):
            gapy = 50
            node.setPos(posx, posy + gapy)
            node.init_pos = node.pos()
            for i in node.lineList:
                for j in node.lineList[i]:
                    j.changePos()
            self.view.viewport().update()
            if len(node.lineList['left']) > 0:
                setNowNodePos(node.lineList['left'][0].endNode, posx - devi // 2, posy + gapy, devi // 2)
            if len(node.lineList['right']) > 0:
                setNowNodePos(node.lineList['right'][0].endNode, posx + devi // 2, posy + gapy, devi // 2)

        if len(nowNode.lineList['left']) > 0:
            setNowNodePos(nowNode.lineList['left'][0].endNode, nowPos[0] - initGap, nowPos[1], initGap)
        if len(nowNode.lineList['right']) > 0:
            setNowNodePos(nowNode.lineList['right'][0].endNode, nowPos[0] + initGap, nowPos[1], initGap)

    def getDepth(self):
        # 为测试完全功能
        if self.headNode is None:
            return

        def getDepths(node):
            maxLeftDepth = 1
            maxRightDepth = 1
            if node.lineList['left']:
                maxLeftDepth = 1 + getDepths(node.lineList['left'][0].endNode)
            if node.lineList['right']:
                maxRightDepth = 1 + getDepths(node.lineList['right'][0].endNode)
            return max(maxLeftDepth, maxRightDepth)

        return getDepths(self.headNode)
