import sys
from CustomWidgets import MyTopBar

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPen, QBrush, QColor, QFont, QCursor, QPalette, QTextCursor, QPainter
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsEllipseItem, QApplication, QWidget, \
    QVBoxLayout, QGraphicsItem, QGraphicsSimpleTextItem, QMenu, QGraphicsLineItem, QLabel, QTextEdit, QComboBox, \
    QLineEdit, QListWidget, QListWidgetItem, QHBoxLayout, QSizePolicy


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
        self.setZValue(0)

        self.changePos()

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
        self.view.setRenderHint(QPainter.Antialiasing)  # 抗锯齿

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


class MyInfo(QWidget):
    def __init__(self, title='test', edition='testEdition'):
        super(MyInfo, self).__init__()

        self.titleWidget = QLabel(title)
        self.editionWidget = QLabel(edition)
        self.mainLayout = QVBoxLayout()

        self.mySettings()
        self.myLayouts()
        self.myStyles()

    def mySettings(self):
        self.setMaximumHeight(120)
        self.setMaximumWidth(200)
        self.titleWidget.setFont(QFont('楷体', 50))
        self.editionWidget.setFont(QFont('楷体', 14))
        self.mainLayout.setSpacing(0)

        self.titleWidget.setContentsMargins(0, 0, 0, 0)
        self.editionWidget.setContentsMargins(50, 0, 0, 0)

    def myLayouts(self):
        self.setLayout(self.mainLayout)
        self.mainLayout.addWidget(self.titleWidget)
        self.mainLayout.addWidget(self.editionWidget)

    def myStyles(self):
        self.setAutoFillBackground(True)
        palette = QPalette()
        palette.setBrush(QPalette.Background, QColor(20, 90, 90))
        self.setPalette(palette)


class MyLogInfo(QTextEdit):
    def __init__(self):
        super(MyLogInfo, self).__init__()
        self.mySettings()
        self.fresh()
        self.textChanged.connect(self.a)

    def a(self):
        if len(self.toPlainText()) == 0:
            self.fresh()
            return
        if self.toPlainText()[-1] == '\n':
            order = self.toPlainText().split('\n')[self.document().blockCount() - 2]
            self.proOrder(order.lstrip('>>> '))
            self.fresh()
        elif len(self.toPlainText().split('\n')[self.document().blockCount() - 1]) < 3:
            self.setText(self.toPlainText() + '>')
        elif len(self.toPlainText().split('\n')[self.document().blockCount() - 1]) == 3:
            self.setText(self.toPlainText() + ' ')
        # self.cursorToEnd()

    def proOrder(self, order):
        print(order)
        pass

    def fresh(self):
        self.setText(self.toPlainText() + '>>> ')
        self.cursorToEnd()

    def mySettings(self):
        self.resize(300, 600)
        self.setFont(QFont('楷体', 18))

    def cursorToEnd(self):
        cursor = self.textCursor()
        cursor.movePosition(QTextCursor.End)
        self.setTextCursor(cursor)


class MyLineEdit(QLineEdit):
    clicked = pyqtSignal(str)

    def mouseReleaseEvent(self, QMouseEvent):
        if QMouseEvent.button() == Qt.LeftButton:
            self.clicked.emit(self.text())


class MyRunButton(QComboBox):
    def __init__(self):
        super(MyRunButton, self).__init__()
        self.setStyleSheet(
            "MyRunButton{background-color:#ccc;}"
            "QComboBox::drop-down {border:1px solid black;border-radius:0 5px}"
            "MyRunButton QAbstractItemView::item{height:60px;}"  # 高度
            "MyRunButton QAbstractItemView::item:hover{background-color:#abc;color:#333;}"
        )
        self.items = ['先序遍历', '中序遍历', '后序遍历', 'test']

        self.myLineEdit()  # 设置文本框
        self.myListWidget()  # 设置下拉框
        self.mySettings()
        self.mySignalConnections()

    def mySettings(self):
        self.resize(200, 50)
        self.setContentsMargins(0, 0, 0, 0)

    def mySignalConnections(self):
        self.lineEdit().clicked.connect(self.a)
        self.currentIndexChanged.connect(lambda: self.a(self.currentText()))

    def a(self, t):
        """
        通过t.text()来判断点击哪个按钮
        :param t:
        :return:
        """
        print(t)
        pass

    def myLineEdit(self):
        le = MyLineEdit()  # 显示框右对齐
        le.setAlignment(Qt.AlignCenter)
        le.setReadOnly(True)
        self.setLineEdit(le)
        self.lineEdit().setFont(QFont('楷体', 20))

    def myListWidget(self):
        listWgt = QListWidget()  # 列表框右对齐
        for item in self.items:
            listWgtItem = QListWidgetItem(item)
            listWgtItem.setTextAlignment(Qt.AlignCenter)
            listWgtItem.setFont(QFont('楷体', 20))
            listWgt.addItem(listWgtItem)
        self.setModel(listWgt.model())
        self.setView(listWgt)


class WorkPlace(QWidget):
    title = '测试'
    textEdition = '线性表'

    def __init__(self):
        super(WorkPlace, self).__init__()
        # 组件
        self.info = MyInfo(self.title, self.textEdition)
        self.logInfo = MyLogInfo()
        self.runButton = MyRunButton()
        self.canvas = MyCanvas()

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
        self.resize(800,600)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.layout2.setContentsMargins(0, 0, 0, 0)
        self.layout3.setContentsMargins(0, 0, 0, 0)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = WorkPlace()
    win.show()
    sys.exit(app.exec_())
