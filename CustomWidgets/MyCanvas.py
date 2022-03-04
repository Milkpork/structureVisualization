import sys

from PyQt5.QtCore import Qt, QPointF, QLineF
from PyQt5.QtGui import QPen, QBrush, QColor, QFont, QCursor, QPainter, QPolygonF, QPainterPath
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsEllipseItem, QApplication, \
    QVBoxLayout, QGraphicsItem, QGraphicsSimpleTextItem, QMenu, QGraphicsLineItem, QFrame
from CustomWidgets.Fundsettings import Fundsettings


class MyNode(QGraphicsEllipseItem):
    size = 40
    in_limit = 1  # 入边最大值
    out_limit = 1  # 出边最大值

    def __init__(self, a, b, t, c, n):  # 分别为，位置x，位置y，文字，父画板,name
        """
        :param a: location x
        :param b: location x
        :param t: text
        :param c: canvas
        :param n: name
        """
        super(MyNode, self).__init__(a, b, self.size, self.size)

        self.init_pos = self.pos()
        self.name = n  # 姓名
        self.m_pos = (a, b)
        self.canvas = c
        self.frame = -1
        self.lineList = {'inLine': [], 'outLine': []}  # 分为入边和出边

        self.text = QGraphicsSimpleTextItem(t)
        self.menu = QMenu()

        self.mySettings()
        self.myStyles()
        self.myTextSettings()
        self.myMenuSettings()

    def mySettings(self):
        self.setFlag(QGraphicsItem.ItemIsMovable)  # 设置为可移动
        self.setZValue(1)

    def myStyles(self):
        self.setPen(QPen(Qt.black, 2))  # 边框
        self.setBrush(QBrush(QColor(255, 255, 255)))  # 内容填充

    def myTextSettings(self):
        self.text.setFont(QFont(Fundsettings.font_family, self.size // 2))
        self.text.setParentItem(self)
        self.text.setPos(self.m_pos[0] + self.size // 3 - (len(self.text.text()) - 1) * (self.size * 0.2),
                         self.m_pos[1] + self.size // 5)  # 设置文字在中间的位置

    def myMenuSettings(self):
        self.rightMenu()  # 菜单
        self.menu.triggered.connect(self.menuSlot)
        # 设置无阴影背景
        self.menu.setWindowFlags(self.menu.windowFlags() | Qt.FramelessWindowHint | Qt.NoDropShadowWindowHint)

    # 按下重载,主要用于判断连线
    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        if self.canvas.cursor() == QCursor(Qt.CrossCursor):
            self.canvas.tempEd = self
            self.canvas.addLine()

    # 移动
    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        self.init_pos = self.pos()
        for i in self.lineList:
            for j in self.lineList[i]:
                j.changePos()
        self.canvas.view.viewport().update()

    # 右击
    def contextMenuEvent(self, event):
        super().contextMenuEvent(event)
        self.menu.exec(QCursor().pos())

    # 需要被重载:右击菜单
    def rightMenu(self):
        pass

    # 需要被重载:菜单的响应函数
    def menuSlot(self, ac):
        pass

    # 接口:修改文本
    def setText(self, t):
        self.text.setText(t)

    # 接口:删除本结点
    def delete(self):
        if self == self.canvas.headNode:
            self.canvas.headNode = None
        # 删除画布字典中的自己
        del self.canvas.nodeDic[self.name]
        if len(self.lineList['inLine']) > 0:
            del self.canvas.lineDic[self.lineList['inLine'][0].name]
            self.canvas.scene.removeItem(self.lineList['inLine'][0])
            self.lineList['inLine'][0].startNode.lineList['outLine'].remove(self.lineList['inLine'][0])
        if len(self.lineList['outLine']) > 0:
            del self.canvas.lineDic[self.lineList['outLine'][0].name]
            self.canvas.scene.removeItem(self.lineList['outLine'][0])
            self.lineList['outLine'][0].endNode.lineList['inLine'].remove(self.lineList['outLine'][0])
        self.canvas.scene.removeItem(self)  # 删除自身

    def resume(self):
        self.setRect(*self.m_pos, self.size, self.size)
        self.setPos(self.init_pos)

    # 动画
    def myAnimation(self, frame=0, allframe=100):
        if self.frame < 0:
            self.frame = frame
            return
        frameDiv = frame - self.frame
        offset = 100
        self.prepareGeometryChange()
        if frameDiv <= allframe / 2:
            # 变大
            self.setPos(self.pos().x() - offset / allframe, self.pos().y() - offset / allframe)
            self.setRect(self.rect().x(), self.rect().y(), self.rect().width() + offset / allframe * 2,
                         self.rect().height() + offset / allframe * 2)
        else:
            # 变小
            self.setPos(self.pos().x() + offset / allframe, self.pos().y() + offset / allframe)
            self.setRect(self.rect().x(), self.rect().y(), self.rect().width() - offset / allframe * 2,
                         self.rect().height() - offset / allframe * 2)
        self.text.setPos(
            self.rect().x() + self.rect().width() // 3 - (len(self.text.text()) - 1) * (self.rect().width() * 0.2),
            self.rect().y() + self.rect().height() // 5)  # 设置文字在中间的位置


class MyLine(QGraphicsLineItem):
    line_width = 3

    def __init__(self, sn=None, en=None, c=None, n=None):
        super(MyLine, self).__init__()

        self.startNode = sn  # 头节点
        self.endNode = en  # 尾结点
        self.canvas = c
        self.name = n
        self.nowStyles = Fundsettings.normalStyles
        self.proportion = 0  # 动画时的实线长度
        self.frame = -1

        self.startPos = QPointF()
        self.endPos = QPointF()
        self.line = QLineF()
        self.menu = QMenu()

        self.startNode.lineList['outLine'].append(self)
        self.endNode.lineList['inLine'].append(self)

        self.mySettings()
        self.myMenuSettings()

    def mySettings(self):
        self.changePos()
        self.setZValue(0)

    def myMenuSettings(self):
        self.rightMenu()
        self.menu.setWindowFlags(self.menu.windowFlags() | Qt.FramelessWindowHint | Qt.NoDropShadowWindowHint)
        self.menu.triggered.connect(self.menuSlot)

    # 重载绘制函数
    def paint(self, QP, QStyleOptionGraphicsItem, QWidget_widget=None):
        if self.startNode.collidesWithItem(self.endNode):  # 判断图形项是否存在相交
            return

        # setBrush
        brush = QBrush()
        brush.setColor(Qt.black)
        brush.setStyle(Qt.SolidPattern)
        QP.setBrush(brush)
        if self.nowStyles == Fundsettings.normalStyles:
            pen = QPen()
            pen.setColor(Qt.black)
            pen.setWidth(self.line_width)
            pen.setJoinStyle(Qt.MiterJoin)
            QP.setPen(pen)

            v = self.line.unitVector()
            v.setLength(10)
            v.translate(QPointF(self.line.dx(), self.line.dy()))

            n = v.normalVector()
            n.setLength(n.length() * 0.5)
            n2 = n.normalVector().normalVector()

            p1 = v.p2()
            p2 = n.p2()
            p3 = n2.p2()

            # # # 方法1
            # # QPainter.drawLine(self.line)
            # # QPainter.drawPolygon(p1, p2, p3)
            #
            # # 方法2
            arrow = QPolygonF([p1, p2, p3, p1])
            path = QPainterPath()
            path.moveTo(self.startPos)
            path.lineTo(self.endPos)
            path.addPolygon(arrow)
            # path.addText(self.startNode.pos(),QFont('楷体',20),"hello")
            QP.drawPath(path)
        elif self.nowStyles == Fundsettings.animatingStyles:
            # setPen
            pen = QPen()
            pen.setColor(Qt.black)
            pen.setWidth(self.line_width - 1)
            pen.setJoinStyle(Qt.MiterJoin)
            pen.setStyle(Qt.DotLine)
            QP.setPen(pen)

            path = QPainterPath()
            path.moveTo(self.startPos)
            path.lineTo(self.endPos)
            QP.drawPath(path)

            # setPen
            pen = QPen()
            pen.setColor(Qt.black)
            pen.setWidth(self.line_width)
            pen.setJoinStyle(Qt.MiterJoin)
            # pen.setStyle(Qt.DotLine)
            QP.setPen(pen)

            v = self.line.unitVector()
            v.setLength(10)
            v.translate(QPointF(self.line.dx(), self.line.dy()))

            n = v.normalVector()
            n.setLength(n.length() * 0.5)
            n2 = n.normalVector().normalVector()

            p1 = v.p2()
            p2 = n.p2()
            p3 = n2.p2()

            # # # 方法1
            # # QPainter.drawLine(self.line)
            # # QPainter.drawPolygon(p1, p2, p3)
            #
            # # 方法2
            arrow = QPolygonF([p1, p2, p3, p1])
            path = QPainterPath()
            path.moveTo(self.startPos)
            path.lineTo(QPointF(
                self.startPos.x() + self.proportion * (self.endPos.x() - self.startPos.x()),
                self.startPos.y() + self.proportion * (self.endPos.y() - self.startPos.y())
            ))
            path.addPolygon(arrow)
            QP.drawPath(path)

    # 屏蔽双击
    def mouseDoubleClickEvent(self, event):
        pass

    # 右击显示菜单
    def contextMenuEvent(self, event):
        super().contextMenuEvent(event)
        # self.canvas.flags = 1
        self.menu.exec(QCursor().pos())

    # 当两端结点坐标变换时，调用该函数修改连线
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

    # 右击菜单内容，需要被重载
    def rightMenu(self):
        pass

    # 右击响应函数，需要被重载
    def menuSlot(self, ac):
        pass

    # 删除本连线函数
    def delete(self):
        # 删除画布字典中的自己
        del self.canvas.lineDic[self.name]
        self.startNode.lineList['outLine'].remove(self)
        self.endNode.lineList['inLine'].remove(self)
        self.canvas.scene.removeItem(self)  # 删除自身

    def resume(self):
        pass

    # 动画
    def myAnimation(self, frame=0, allFrame=100):
        self.nowStyles = Fundsettings.animatingStyles
        if self.frame < 0:
            self.frame = frame
            return
        frameDiv = frame - self.frame
        proportion = frameDiv / allFrame
        self.proportion = proportion
        self.canvas.view.viewport().update()


class MyView(QGraphicsView):
    def __init__(self, sc, canv):
        super(MyView, self).__init__(sc)

        self.canvas = canv

        self.mySettings()

    def mySettings(self):
        self.setRenderHint(QPainter.Antialiasing)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setAlignment(Qt.AlignLeft | Qt.AlignTop)  # 取消居中

    def mousePressEvent(self, event):
        # 用于取消添加状态
        super().mousePressEvent(event)
        if self.canvas.cursor() == QCursor(Qt.CrossCursor):
            self.canvas.clear()


class MyCanvas(QFrame):
    def __init__(self, nodeType, lineType, viewType, workplace=None):
        super(MyCanvas, self).__init__()
        self.setStyleSheet(
            "QFrame{border-radius:5px;border:1px solid;background-color:transparent}"
            "QGraphicsView{border-radius:5px;border:2px solid;}"
        )
        self.workplace = workplace
        self.nodeType = nodeType
        self.lineType = lineType
        self.viewType = viewType
        self.lineCount = 0
        self.nodeCount = 0
        self.nodeDic = {}
        self.lineDic = {}
        self.headNode = None
        self.tempSt = None
        self.tempEd = None

        # 基础组件和布局
        self.mainLayout = QVBoxLayout(self)
        self.scene = QGraphicsScene()
        self.view = self.viewType(self.scene, self)
        self.mainLayout.addWidget(self.view)

        self.mySettings()

    def mySettings(self):
        self.resize(400, 400)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)

        self.setLineWidth(0)  # 设置外线宽度
        self.setMidLineWidth(0)  # 设置中线宽度
        self.setFrameShadow(QFrame.Plain)  # 设置阴影效果：凸起
        self.setFrameShape(QFrame.StyledPanel)  # 设置图形为：Box

        self.setAttribute(Qt.WA_TranslucentBackground, True)

    def addNode(self):
        gap = 20  # 节点间的间隔
        maxSize = (self.width() - MyNode.size) // gap + 1  # 一行最多结点个数
        minPadding = 5  # 防止上方溢出
        self.nodeDic["node" + str(self.nodeCount)] = self.nodeType(gap * (self.nodeCount % maxSize),
                                                                   minPadding + gap * (self.nodeCount // maxSize),
                                                                   str(self.nodeCount),
                                                                   self,
                                                                   "node" + str(self.nodeCount))
        return self.nodeDic["node" + str(self.nodeCount)]

    def addLine(self):
        if self.tempSt == self.tempEd:
            return

        if len(self.tempSt.lineList['outLine']) >= self.nodeType.out_limit or len(
                self.tempEd.lineList['inLine']) >= self.nodeType.in_limit:
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

    def setHeadNode(self, node):
        # 设置头节点接口
        if self.headNode is None:
            self.headNode = node
            node.setPen(QPen(QColor(255, 165, 0), 2))
        else:
            self.headNode.setPen(QPen(Qt.black, 2))
            self.headNode = node
            node.setPen(QPen(QColor(255, 165, 0), 2))

    # 以下是与输入框一同使用的指令
    def insert(self, ls):
        pass

    def clear(self, nodeList=None, lineList=None):
        pass

    def workplace(self):
        return self.workplace


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MyCanvas(MyNode, MyLine, MyView)
    win.show()
    sys.exit(app.exec_())
