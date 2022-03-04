import re
import sys

from PyQt5.QtCore import Qt, QTimeLine
from PyQt5.QtGui import QCursor, QPen, QColor
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QSizePolicy
from CustomWidgets import MyInfo, MyLogInfo, MyRunButton, MyNode, MyLine, MyView, MyCanvas


class Node_LinearList(MyNode):
    in_limit = 1  # 入边最大值
    out_limit = 1  # 出边最大值

    def __init__(self, a, b, t, c, n):  # 分别为，位置x，位置y，文字，父画板
        super(Node_LinearList, self).__init__(a, b, t, c, n)
        self.lineList = {'next': [], 'previous': []}

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        self.init_pos = self.pos()
        for i in self.lineList:
            for j in self.lineList[i]:
                j.changePos()
        self.canvas.view.viewport().update()

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
        if len(self.lineList['next']) == 1:
            del self.canvas.lineDic[self.lineList['next'][0].name]
            self.canvas.scene.removeItem(self.lineList['next'][0])
            self.lineList['next'][0].endNode.lineList['previous'] = []
        self.canvas.scene.removeItem(self)  # 删除自身


class Line_LinearList(MyLine):
    def __init__(self, sn=None, en=None, c=None, n=None):
        super(Line_LinearList, self).__init__(sn, en, c, n)

    def addNodeLine(self):
        self.startNode.lineList['next'].append(self)
        self.endNode.lineList['previous'].append(self)

    def rightMenu(self):
        self.menu.addAction('删除')
        self.menu.addSeparator()
        self.menu.addAction('反转')

    def menuSlot(self, ac):
        if ac.text() == '删除':
            self.delete()

    def delete(self):
        # 删除画布字典中的自己
        del self.canvas.lineDic[self.name]
        self.startNode.lineList['next'] = []
        self.endNode.lineList['previous'] = []
        self.canvas.scene.removeItem(self)  # 删除自身


class View_LinearList(MyView):
    def __init__(self, sc, canv):
        super(View_LinearList, self).__init__(sc, canv)


class Canvas_LinearList(MyCanvas):
    def __init__(self, workplace=None):
        super(Canvas_LinearList, self).__init__(Node_LinearList, Line_LinearList, View_LinearList, workplace)

    def addLine(self):
        if self.tempSt == self.tempEd:
            return

        if len(self.tempSt.lineList['next']) == 1 or len(
                self.tempEd.lineList['previous']) == 1:
            self.workplace.logInfo.append('out of limit\n>>> ')
            self.setCursor(QCursor(Qt.ArrowCursor))
            self.tempSt = None
            self.tempEd = None
            return

        self.lineDic["line" + str(self.lineCount)] = self.lineType(self.tempSt, self.tempEd, self,
                                                                   "line" + str(self.lineCount))
        self.scene.addItem(self.lineDic["line" + str(self.lineCount)])
        self.tempSt = None
        self.tempEd = None
        self.lineCount += 1

        self.setCursor(QCursor(Qt.ArrowCursor))

    def ergodic(self):
        # 遍历
        if self.headNode is None:  # 没有头节点
            print("no head node!")
            return

        nowNode = self.headNode
        queue = []
        self.workplace.logInfo.append("result : ")
        while True:
            # 插入动画
            self.workplace.logInfo.append(nowNode.text.text() + " ")
            queue.append(nowNode)
            if len(nowNode.lineList['next']) > 0:
                queue.append(nowNode.lineList['next'][0])
                nowNode = nowNode.lineList['next'][0].endNode
                # 循环链表防止死循环
                if nowNode == self.headNode:
                    break
            else:
                break
        self.workplace.logInfo.append("\n>>> ")

        # animation

        def anim(frame, allframe):
            index = frame // allframe
            queue[index].myAnimation(frame, allframe)

            # queue[index - 1].frame = -1

        nums = len(queue)
        singleFrame = 100
        singleTime = 1000
        timeline = QTimeLine(nums * singleTime, self)  # 实例化一个时间轴，持续时间为5秒
        timeline.setFrameRange(0, singleFrame * nums)  # 设置帧率范围，该值表示在规定的时间内将要执行多少帧
        timeline.frameChanged.connect(lambda frame: anim(frame - 1, singleFrame))  # 帧数变化时发出信号
        timeline.setLoopCount(1)  # 传入0代表无限循环运行.传入正整数会运行相应次数，传入负数不运行
        timeline.setCurveShape(QTimeLine.LinearCurve)
        timeline.start()  # 启动动画

        def fini():
            for i in queue:
                i.frame = -1
                i.resume()

        timeline.finished.connect(fini)

        # 多线程
        # def fun(queues):
        #     nums = len(queue)
        #     t1 = time.perf_counter()
        #     for i in range(nums):
        #         while True:
        #             # 需要线程
        #             if time.perf_counter() - t1 >= 1:
        #                 queues[i].myAnimation()
        #                 t1 = time.perf_counter()
        #                 break
        #
        # # 动画部分
        # t = Thread(target=lambda: fun(queue))
        # t.start()

    def insert(self, ls):
        gap = 20  # 节点间的间隔
        maxSize = (self.width() - MyNode.size) // gap + 1  # 一行最多结点个数
        minPadding = 5  # 防止上方溢出
        st = self.nodeCount
        for i in ls:
            self.nodeDic["node" + str(self.nodeCount)] = Node_LinearList(gap * (self.nodeCount % maxSize),
                                                                         minPadding + gap * (
                                                                                 self.nodeCount // maxSize),
                                                                         i, self, "node" + str(self.nodeCount))
            self.scene.addItem(self.nodeDic["node" + str(self.nodeCount)])
            self.nodeCount += 1

        for i in range(st, self.nodeCount - 1):
            self.lineDic["line" + str(self.lineCount)] = Line_LinearList(self.nodeDic["node" + str(i)],
                                                                         self.nodeDic["node" + str(i + 1)], self,
                                                                         "line" + str(self.lineCount))
            self.scene.addItem(self.lineDic["line" + str(self.lineCount)])
            self.tempSt = None
            self.tempEd = None
            self.lineCount += 1

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
