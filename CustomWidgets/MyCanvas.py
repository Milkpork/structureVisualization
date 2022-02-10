import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPen, QBrush, QColor, QFont, QCursor, QPainter
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsEllipseItem, QApplication, QWidget, \
    QVBoxLayout, QGraphicsItem, QGraphicsSimpleTextItem, QMenu, QGraphicsLineItem


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

    def menuSlot(self, ac):
        if ac.text() == '连线':
            self.canvas.setCursor(QCursor(Qt.CrossCursor))
            self.canvas.tempSt = self


class MyLine(QGraphicsLineItem):
    def __init__(self, sn=None, en=None):
        super(MyLine, self).__init__()

        self.startNode = sn  # 头节点
        self.endNode = en  # 尾结点
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
        self.setLine(self.startNode.rect().x() + self.startNode.rect().width() // 2 + self.startNode.pos().x(),
                     self.startNode.rect().y() + self.startNode.rect().height() // 2 + self.startNode.pos().y(),
                     self.endNode.rect().x() + self.endNode.rect().width() // 2 + self.endNode.pos().x(),
                     self.endNode.rect().y() + self.endNode.rect().height() // 2 + self.endNode.pos().y())


class MyCanvas(QWidget):
    def __init__(self):
        super(MyCanvas, self).__init__()

        self.nodeCount = 0
        self.nodeDic = {}
        self.lineDic = {}
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
        self.menu.addAction('test')

    def rightMenuShow(self, event):
        # 右击菜单
        super().contextMenuEvent(event)
        self.menu.exec(QCursor().pos())

    def menuSlot(self, ac):
        if ac.text() == '新建':
            self.scene.addItem(self.addNode())
            self.nodeCount += 1

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
        self.lineDic["line" + str(self.nodeCount)] = MyLine(self.tempSt, self.tempEd)
        self.scene.addItem(self.lineDic["line" + str(self.nodeCount)])
        self.tempSt = None
        self.tempEd = None
        self.setCursor(QCursor(Qt.ArrowCursor))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MyCanvas()
    win.show()
    sys.exit(app.exec_())
