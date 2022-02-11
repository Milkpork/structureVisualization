import sys

from PyQt5.QtCore import Qt, QLineF, QPointF
from PyQt5.QtGui import QCursor, QPainter, QPen, QColor, QBrush, QFont, QPolygonF, QPainterPath
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QSizePolicy, QGraphicsView, QMenu, \
    QGraphicsScene, QGraphicsLineItem, QGraphicsItem, QGraphicsSimpleTextItem, QGraphicsEllipseItem
from CustomWidgets import MyInfo, MyLogInfo, MyRunButton


class Info_LinearList(MyInfo):
    def __init__(self, title='test', edition='testEdition'):
        super(Info_LinearList, self).__init__(title, edition)


class LogInfo_LinearList(MyLogInfo):
    def __init__(self):
        super(LogInfo_LinearList, self).__init__()


class RunButton_LinearList(MyRunButton):
    def __init__(self):
        super(RunButton_LinearList, self).__init__()
        self.changeItems(['遍历1', '反转'])


class MyNode(QGraphicsEllipseItem):
    size = 30

    def __init__(self, a, b, t, c):  # 分别为，位置x，位置y，文字，父画板
        self.m_pos = (a, b)
        self.canvas = c
        super(MyNode, self).__init__(self.m_pos[0], self.m_pos[1], self.size, self.size)
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

    def myStyles(self):
        self.setPen(QPen(Qt.black, 2))  # 边框
        self.setBrush(QBrush(QColor(200, 200, 200)))  # 内容填充

    def myLayouts(self):
        self.text.setPos(self.m_pos[0] + self.size / 2 - 5, self.m_pos[1] + self.size / 2 - 8)  # 设置文字在中间的位置

    def mySignalConnections(self):
        self.menu.triggered.connect(self.menuSlot)

    def mouseDoubleClickEvent(self, event):
        # 双击显示菜单,由于右击被覆盖,改用双击
        self.menu.exec(QCursor().pos())

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        if self.canvas.cursor() == QCursor(Qt.CrossCursor):
            self.canvas.tempEd = self
            self.canvas.addLine()

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        pass

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        for i in self.lineList:
            for j in self.lineList[i]:
                j.changePos()

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


class MyLine(QGraphicsLineItem):
    def __init__(self, sn=None, en=None):
        super(MyLine, self).__init__()

        self.startNode = sn  # 头节点
        self.endNode = en  # 尾结点

        self.startPos = QPointF()
        self.endPos = QPointF()
        self.line = QLineF()

        self.startNode.lineList['outLine'].append(self)
        self.endNode.lineList['inLine'].append(self)

        self.mySettings()

    def mySettings(self):
        pen = QPen()  # 建立画笔
        color = QColor(10, 10, 10)  # 建立一个色彩对象
        pen.setColor(color)  # 为画笔加上颜色
        pen.setWidth(4)  # 设置画笔宽度
        self.setPen(pen)

        self.changePos()
        self.setZValue(0)

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
        self.line.setLength(self.line.length() - 28)

        self.setLine(self.startNode.rect().x() + self.startNode.rect().width() // 2 + self.startNode.pos().x(),
                     self.startNode.rect().y() + self.startNode.rect().height() // 2 + self.startNode.pos().y(),
                     self.endNode.rect().x() + self.endNode.rect().width() // 2 + self.endNode.pos().x(),
                     self.endNode.rect().y() + self.endNode.rect().height() // 2 + self.endNode.pos().y())

    def paint(self, QP, QStyleOptionGraphicsItem, QWidget_widget=None):
        if self.startNode.collidesWithItem(self.endNode):  # 判断图形项是否存在相交
            return
        # setPen
        pen = QPen()
        pen.setWidth(2)
        pen.setJoinStyle(Qt.MiterJoin)
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


class Canvas_LinearList(QWidget):
    def __init__(self):
        super(Canvas_LinearList, self).__init__()

        self.nodeCount = 0
        self.nodeDic = {}
        self.lineDic = {}
        self.headNode = None
        self.tempSt = None
        self.tempEd = None

        # 基础组件和布局
        self.mainLayout = QVBoxLayout(self)
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        self.menu = QMenu()
        self.mainLayout.addWidget(self.view)

        self.mySettings()
        self.mySignalConnections()

    def mySettings(self):
        self.rightMenu()  # 右击菜单
        self.resize(400, 400)
        self.view.setAlignment(Qt.AlignLeft | Qt.AlignTop)  # 取消居中
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.view.contextMenuEvent = self.rightMenuShow  # 重载函数
        self.setContextMenuPolicy(Qt.CustomContextMenu)  # 好像用不着
        self.view.setRenderHint(QPainter.Antialiasing)

    def mySignalConnections(self):
        self.menu.triggered.connect(self.menuSlot)

    def rightMenu(self):
        self.menu.addAction('新建')
        self.menu.addSeparator()
        self.menu.addAction('遍历')

    def rightMenuShow(self, event):
        # 右击菜单
        super().contextMenuEvent(event)
        self.menu.exec(QCursor().pos())

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
                                                            str(self.nodeCount), self)
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

        self.lineDic["line" + str(self.nodeCount)] = MyLine(self.tempSt, self.tempEd)
        self.scene.addItem(self.lineDic["line" + str(self.nodeCount)])
        self.tempSt = None
        self.tempEd = None

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
        if self.headNode is None:
            print("no head node!")
            return
        nowNode = self.headNode
        while True:
            print(nowNode.text.text())
            if len(nowNode.lineList['outLine']) > 0:
                nowNode = nowNode.lineList['outLine'][0].endNode
                # 循环链表防止死循环
                if nowNode == self.headNode:
                    break
            else:
                break
        print('endnow')


class WorkPlace(QWidget):
    title = '测试'
    textEdition = '线性表'

    def __init__(self):
        super(WorkPlace, self).__init__()
        # 组件
        self.info = Info_LinearList(self.title, self.textEdition)
        self.logInfo = LogInfo_LinearList()
        self.runButton = RunButton_LinearList()
        self.canvas = Canvas_LinearList()

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
        self.layout2.setContentsMargins(0, 0, 0, 0)
        self.layout3.setContentsMargins(0, 0, 0, 0)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = WorkPlace()
    win.show()
    sys.exit(app.exec_())
