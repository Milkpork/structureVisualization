import re
import sys

from PyQt5.QtCore import Qt, QTimeLine
from PyQt5.QtGui import QCursor, QPen, QColor
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QSizePolicy
from CustomWidgets import MyInfo, MyLogInfo, MyRunButton, MyNode, MyLine, MyView, MyCanvas


class Info_LinearList(MyInfo):
    def __init__(self, title='test', edition='testEdition'):
        super(Info_LinearList, self).__init__(title, edition)


class LogInfo_LinearList(MyLogInfo):
    def __init__(self, canvas):
        super(LogInfo_LinearList, self).__init__(canvas)

    def proOrder(self, order):
        ls = order.split()
        if ls[0] == 'insert':
            com = re.compile(r'^\d\d?$')  # 通过正则检擦是否为两位数
            for i in ls[1:]:
                if com.match(i):
                    continue
                else:
                    self.append('no match')
                    break
            else:
                self.getWorkplace().canvas.insert(ls[1:])  # 需要用到画板的插入函数
        elif ls[0] == 'help':
            self.append('\n1.(insert [num] [num] ... ) can insert')
            self.append('\n2.more are going to append...')
        else:
            self.append('\nno such order')


class RunButton_LinearList(MyRunButton):
    def __init__(self, workplace):
        super(RunButton_LinearList, self).__init__(workplace)
        self.changeItems(['新建', '先序遍历', '中序遍历', '后序遍历'])

    def menuSlot(self, t):
        if self.flag == 0:
            self.flag = 1
            return
        if t == '先序遍历':
            self.getWorkplace().canvas.ergodic(0)
        elif t == '中序遍历':
            self.getWorkplace().canvas.ergodic(1)
        elif t == '后序遍历':
            self.getWorkplace().canvas.ergodic(2)
        elif t == '新建':
            self.getWorkplace().canvas.scene.addItem(self.getWorkplace().canvas.addNode())
            self.getWorkplace().canvas.nodeCount += 1


class Node_LinearList(MyNode):
    in_limit = 1  # 入边最大值
    out_limit = 2  # 出边最大值

    def __init__(self, a, b, t, c, n):  # 分别为，位置x，位置y，文字，父画板
        super(Node_LinearList, self).__init__(a, b, t, c, n)

    def rightMenu(self):
        self.menu.addAction('删除')
        self.menu.addSeparator()
        self.menu.addAction('设置左节点')
        self.menu.addSeparator()
        self.menu.addAction('设置头节点')

    def menuSlot(self, ac):
        if ac.text() == '连线':
            self.canvas.setCursor(QCursor(Qt.CrossCursor))
            self.canvas.tempSt = self
        elif ac.text() == '设置左节点':
            self.canvas.setHeadNode(self)
        elif ac.text() == '删除':
            self.delete()


class Line_LinearList(MyLine):
    def __init__(self, sn=None, en=None, c=None, n=None):
        super(Line_LinearList, self).__init__(sn, en, c, n)

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

    def ergodic(self,mode=0):
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
            if len(nowNode.lineList['outLine']) > 0:
                queue.append(nowNode.lineList['outLine'][0])
                nowNode = nowNode.lineList['outLine'][0].endNode
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


class WorkPlace(QWidget):

    def __init__(self, t='Canvas', te='二叉树'):  # 参数为text和textEdition
        super(WorkPlace, self).__init__()

        self.title = t
        self.textEdition = te

        # 组件
        self.info = Info_LinearList(self.title, self.textEdition)
        self.canvas = Canvas_LinearList(self)
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
    win = WorkPlace('canvas', 'LinearList')
    win.show()
    sys.exit(app.exec_())
