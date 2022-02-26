import re
import sys

from PyQt5.QtCore import Qt, QLineF, QPointF, QTimeLine
from PyQt5.QtGui import QCursor, QPainter, QPen, QColor, QBrush, QFont, QPolygonF, QPainterPath
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QSizePolicy, QGraphicsView, QMenu, \
    QGraphicsScene, QGraphicsLineItem, QGraphicsItem, QGraphicsSimpleTextItem, QGraphicsEllipseItem, QFrame
from CustomWidgets import MyInfo, MyLogInfo, MyRunButton


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
                self.canvas.insert(ls[1:])  # 需要用到画板的插入函数
        elif ls[0] == 'help':
            self.append('\n1.(insert [num] [num] ... ) can insert')
            self.append('\n2.more are going to append...')
        else:
            self.append('\nno such order')


class RunButton_LinearList(MyRunButton):
    def __init__(self, canvas):
        super(RunButton_LinearList, self).__init__(canvas)
        self.changeItems(['遍历', '反转'])

    def menuSlot(self, t):
        if self.flag == 0:
            self.flag = 1
            return
        if t == '遍历':
            self.canvas.ergodic()


class MyNode(QGraphicsEllipseItem):
    size = 40

    def __init__(self, a, b, t, c, n):  # 分别为，位置x，位置y，文字，父画板
        super(MyNode, self).__init__(a, b, self.size, self.size)
        self.name = n  # 姓名
        self.m_pos = (a, b)
        self.canvas = c
        # 用于记录连接该点的所有线
        self.lineList = {'inLine': [], 'outLine': []}  # 分为入边和出边
        self.text = QGraphicsSimpleTextItem(t)
        self.menu = QMenu()

        self.mySettings()
        self.myStyles()
        self.myLayouts()
        self.mySignalConnections()

    def mySettings(self):
        self.text.setFont(QFont('楷体', self.size // 2))
        self.text.setParentItem(self)
        self.setFlag(QGraphicsItem.ItemIsMovable)  # 设置为可移动
        self.rightMenu()  # 菜单
        self.setZValue(1)
        self.menu.setWindowFlags(
            self.menu.windowFlags() | Qt.FramelessWindowHint | Qt.NoDropShadowWindowHint)  # 设置无阴影背景

    def myStyles(self):
        self.setPen(QPen(Qt.black, 2))  # 边框
        self.setBrush(QBrush(QColor(255, 255, 255)))  # 内容填充

    def myLayouts(self):
        self.text.setPos(self.m_pos[0] + self.size // 3 - (len(self.text.text()) - 1) * (self.size * 0.2),
                         self.m_pos[1] + self.size // 5)  # 设置文字在中间的位置

    def mySignalConnections(self):
        self.menu.triggered.connect(self.menuSlot)

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        if self.canvas.cursor() == QCursor(Qt.CrossCursor):
            self.canvas.tempEd = self
            self.canvas.addLine()

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        for i in self.lineList:
            for j in self.lineList[i]:
                j.changePos()
        self.canvas.view.viewport().update()

    def contextMenuEvent(self, event):
        super().contextMenuEvent(event)
        self.canvas.flags = 1
        self.menu.exec(QCursor().pos())

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

    def setText(self, t):
        self.text.setText(t)

    def delete(self):
        # 只是看不见，内存为释放，未解决
        # 删除头节点
        if self == self.canvas.headNode:
            self.canvas.headNode = None
        # 删除画布字典中的自己
        del self.canvas.nodeDic[self.name]
        if len(self.lineList['inLine']) > 0:
            del self.canvas.lineDic[self.lineList['inLine'][0].name]
            self.canvas.scene.removeItem(self.lineList['inLine'][0])
            self.lineList['inLine'][0].startNode.lineList['outLine'] = []
        if len(self.lineList['outLine']) > 0:
            del self.canvas.lineDic[self.lineList['outLine'][0].name]
            self.canvas.scene.removeItem(self.lineList['outLine'][0])
            self.lineList['outLine'][0].endNode.lineList['inLine'] = []
        self.canvas.scene.removeItem(self)  # 删除自身

    def myAnimation(self, frame):
        self.setPen(QPen(Qt.blue, 2))  # 边框
        # self.setRect(QRectF(self.rect().x(),
        #                     self.rect().y(),
        #                     self.size+20,
        #                     self.size+20))
        self.setScale(1.2)


class MyLine(QGraphicsLineItem):
    def __init__(self, sn=None, en=None, c=None, n=None):
        super(MyLine, self).__init__()

        self.startNode = sn  # 头节点
        self.endNode = en  # 尾结点
        self.canvas = c
        self.name = n

        self.startPos = QPointF()
        self.endPos = QPointF()
        self.line = QLineF()
        self.menu = QMenu()

        self.startNode.lineList['outLine'].append(self)
        self.endNode.lineList['inLine'].append(self)

        self.mySettings()
        self.mySignalConnections()

    def mySettings(self):
        self.rightMenu()
        self.menu.setWindowFlags(
            self.menu.windowFlags() | Qt.FramelessWindowHint | Qt.NoDropShadowWindowHint)  # 设置无阴影背景

        self.changePos()
        self.setZValue(0)

    def mySignalConnections(self):
        self.menu.triggered.connect(self.menuSlot)

    def paint(self, QP, QStyleOptionGraphicsItem, QWidget_widget=None):
        if self.startNode.collidesWithItem(self.endNode):  # 判断图形项是否存在相交
            return
        # setPen
        pen = QPen()
        pen.setColor(Qt.black)
        pen.setWidth(2)
        pen.setJoinStyle(Qt.MiterJoin)
        # pen.setStyle(Qt.DotLine)
        QP.setPen(pen)

        # setBrush
        brush = QBrush()
        brush.setColor(Qt.black)
        brush.setStyle(Qt.SolidPattern)
        QP.setBrush(brush)

        v = self.line.unitVector()
        v.setLength(10)
        v.translate(QPointF(self.line.dx(), self.line.dy()))

        n = v.normalVector()
        n.setLength(n.length() * 0.5)
        n2 = n.normalVector().normalVector()

        p1 = v.p2()
        p2 = n.p2()
        p3 = n2.p2()

        # # 方法1
        # QPainter.drawLine(self.line)
        # QPainter.drawPolygon(p1, p2, p3)

        # 方法2
        arrow = QPolygonF([p1, p2, p3, p1])
        path = QPainterPath()
        path.moveTo(self.startPos)
        path.lineTo(self.endPos)
        path.addPolygon(arrow)
        QP.drawPath(path)

    def mouseDoubleClickEvent(self, event):
        print(223)

    def contextMenuEvent(self, event):
        super().contextMenuEvent(event)
        self.canvas.flags = 1
        self.menu.exec(QCursor().pos())

    def changePos(self):
        self.startPos = QPointF(
            self.startNode.rect().x() + self.startNode.rect().width() // 2 + self.startNode.pos().x(),
            self.startNode.rect().y() + self.startNode.rect().height() // 2 + self.startNode.pos().y()
        )
        self.endPos = QPointF(
            self.endNode.rect().x() + self.endNode.rect().width() // 2 + self.endNode.pos().x(),
            self.endNode.rect().y() + self.endNode.rect().height() // 2 + self.endNode.pos().y()
        )
        self.line = QLineF(self.startPos, self.endPos)
        self.line.setLength(self.line.length() - 33)

        self.setLine(self.startNode.rect().x() + self.startNode.rect().width() // 2 + self.startNode.pos().x(),
                     self.startNode.rect().y() + self.startNode.rect().height() // 2 + self.startNode.pos().y(),
                     self.endNode.rect().x() + self.endNode.rect().width() // 2 + self.endNode.pos().x(),
                     self.endNode.rect().y() + self.endNode.rect().height() // 2 + self.endNode.pos().y())

    def rightMenu(self):
        self.menu.addAction('删除')
        self.menu.addSeparator()
        self.menu.addAction('反转')

    def menuSlot(self, ac):
        if ac.text() == '删除':
            self.delete()

    def delete(self):
        pass

    def myAnimation(self, frame):
        print(self)


class MyView(QGraphicsView):
    def __init__(self, sc, canv):
        super(MyView, self).__init__(sc)

        self.canvas = canv

        self.menu = QMenu()

        self.mySettings()

    def mySettings(self):
        self.rightMenu()
        self.setRenderHint(QPainter.Antialiasing)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.menu.setWindowFlags(
            self.menu.windowFlags() | Qt.FramelessWindowHint | Qt.NoDropShadowWindowHint)  # 设置无阴影背景

    def contextMenuEvent(self, event):
        super().contextMenuEvent(event)
        if self.canvas.flags == 0:
            self.menu.exec(QCursor().pos())
        else:
            self.canvas.flags = 0

    def mousePressEvent(self, event):
        # 用于取消添加状态
        super().mousePressEvent(event)
        if self.canvas.cursor() == QCursor(Qt.CrossCursor):
            self.canvas.clear()

    def rightMenu(self):
        self.menu.addAction('新建')
        self.menu.addSeparator()
        self.menu.addAction('遍历')


class Canvas_LinearList(QFrame):
    def __init__(self):
        super(Canvas_LinearList, self).__init__()
        self.setStyleSheet(
            "QFrame{border-radius:5px;border:1px solid;background-color:transparent}"
            "QGraphicsView{border-radius:5px;border:2px solid;}"
        )
        self.lineCount = 0
        self.nodeCount = 0
        self.flags = 0  # 用于判断右击只能触发一个菜单的参数
        self.nodeDic = {}
        self.lineDic = {}
        self.color = QColor(0, 0, 0)
        self.headNode = None
        self.tempSt = None
        self.tempEd = None

        # 基础组件和布局
        self.mainLayout = QVBoxLayout(self)
        self.scene = QGraphicsScene()
        self.view = MyView(self.scene, self)
        self.mainLayout.addWidget(self.view)

        self.mySettings()
        self.mySignalConnections()

    def mySettings(self):
        self.resize(400, 400)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)

        self.setLineWidth(0)  # 设置外线宽度
        self.setMidLineWidth(0)  # 设置中线宽度
        self.setFrameShadow(QFrame.Plain)  # 设置阴影效果：凸起
        self.setFrameShape(QFrame.StyledPanel)  # 设置图形为：Box

        self.view.setAlignment(Qt.AlignLeft | Qt.AlignTop)  # 取消居中
        self.setContextMenuPolicy(Qt.CustomContextMenu)  # 好像用不着

        self.setAttribute(Qt.WA_TranslucentBackground, True)

    def mySignalConnections(self):
        self.view.menu.triggered.connect(self.menuSlot)

    def menuSlot(self, ac):
        if ac.text() == '新建':
            self.scene.addItem(self.addNode())
            self.nodeCount += 1
        elif ac.text() == '遍历':
            self.ergodic()

    def addNode(self):
        gap = 20  # 节点间的间隔
        maxSize = (self.width() - MyNode.size) // gap + 1  # 一行最多结点个数
        minPadding = 5  # 防止上方溢出
        self.nodeDic["node" + str(self.nodeCount)] = MyNode(gap * (self.nodeCount % maxSize),
                                                            minPadding + gap * (self.nodeCount // maxSize),
                                                            str(self.nodeCount), self, "node" + str(self.nodeCount))
        return self.nodeDic["node" + str(self.nodeCount)]

    def addLine(self):
        if self.tempSt == self.tempEd:
            return

        # 线性表特点
        if len(self.tempSt.lineList['outLine']) > 0 or len(self.tempEd.lineList['inLine']) > 0:
            print('LinearList only has one')
            self.setCursor(QCursor(Qt.ArrowCursor))
            self.tempSt = None
            self.tempEd = None
            return

        self.lineDic["line" + str(self.lineCount)] = MyLine(self.tempSt, self.tempEd, self,
                                                            "line" + str(self.lineCount))
        self.scene.addItem(self.lineDic["line" + str(self.lineCount)])
        self.tempSt = None
        self.tempEd = None
        self.lineCount += 1

        self.setCursor(QCursor(Qt.ArrowCursor))

    def setHeadNode(self, node):
        # 设置头节点接口
        if self.headNode is None:
            self.headNode = node
            node.setPen(QPen(QColor(255, 165, 0), 2))
        else:
            self.headNode.setPen(QPen(Qt.black, 2))
            self.headNode = node
            node.setPen(QPen(QColor(255, 165, 0), 2))

    def ergodic(self):
        # 遍历
        if self.headNode is None:  # 没有头节点
            print("no head node!")
            return

        nowNode = self.headNode
        nodeList = []
        lineList = []
        while True:
            # 插入动画
            print(nowNode.text.text())
            nodeList.append(nowNode)
            if len(nowNode.lineList['outLine']) > 0:
                lineList.append(nowNode.lineList['outLine'][0])
                nowNode = nowNode.lineList['outLine'][0].endNode
                # 循环链表防止死循环
                if nowNode == self.headNode:
                    break
            else:
                break
        singleTime = 1000  # 每一个动画持续一秒
        singleFrame = 5  # 每一个动画有5帧
        nums = (len(nodeList) + len(lineList))  # 有nums个需要执行的物体
        allTime = singleTime * nums
        allFrame = singleFrame * nums
        timeline = QTimeLine(allTime, self)  # 实例化一个时间轴，持续时间为5秒
        timeline.setFrameRange(0, allFrame)  # 设置帧率范围，该值表示在规定的时间内将要执行多少帧
        timeline.frameChanged.connect(
            lambda frame: self.ergodicAnimation(frame - 1, nodeList, lineList, singleFrame, allFrame))  # 帧数变化时发出信号
        timeline.setLoopCount(1)  # 传入0代表无限循环运行.传入正整数会运行相应次数，传入负数不运行
        timeline.start()  # 启动动画

    def ergodicAnimation(self, frame, nodeList, lineList, singleFrame, allframe):
        times = frame // singleFrame
        flags = frame % singleFrame
        if times % 2 == 0 and flags == 0:
            # 偶数为结点
            nodeList[times // 2].myAnimation(frame)
        elif times % 2 == 1 and flags == 0:
            lineList[(times - 1) // 2].myAnimation(frame)
        if frame == allframe - 1:
            self.clear(nodeList, lineList)

    def insert(self, ls):
        gap = 20  # 节点间的间隔
        maxSize = (self.width() - MyNode.size) // gap + 1  # 一行最多结点个数
        minPadding = 5  # 防止上方溢出
        st = self.nodeCount
        for i in ls:
            self.nodeDic["node" + str(self.nodeCount)] = MyNode(gap * (self.nodeCount % maxSize),
                                                                minPadding + gap * (self.nodeCount // maxSize),
                                                                i, self, "node" + str(self.nodeCount))
            self.scene.addItem(self.nodeDic["node" + str(self.nodeCount)])
            self.nodeCount += 1

        for i in range(st, self.nodeCount - 1):
            self.lineDic["line" + str(self.lineCount)] = MyLine(self.nodeDic["node" + str(i)],
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

    def __init__(self, t='Canvas', te='线性表'):  # 参数为text和textEdition
        super(WorkPlace, self).__init__()

        self.title = t
        self.textEdition = te

        # 组件
        self.info = Info_LinearList(self.title, self.textEdition)
        self.canvas = Canvas_LinearList()
        self.runButton = RunButton_LinearList(self.canvas)
        self.logInfo = LogInfo_LinearList(self.canvas)

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
