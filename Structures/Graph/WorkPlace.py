import sys

from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QSizePolicy
from CustomWidgets import MyInfo, MyLogInfo, MyRunButton
from Structures.Graph.Graph_Canvas import Canvas_Graph
from Structures.Graph.UndirectedGraph_Canvas import Canvas_Graph_Undirected


class Info_Graph(MyInfo):
    def __init__(self, title='test', edition='testEdition'):
        super(Info_Graph, self).__init__(title, edition)


class LogInfo_Graph(MyLogInfo):
    def __init__(self, canvas):
        super(LogInfo_Graph, self).__init__(canvas)

    def proOrder(self, order):
        ls = order.split()
        if ls[0] == 'insert':
            self.append("\ngraph do not has insert")
        elif ls[0] == 'help':
            self.append('\n1.(insert [num] [num] ... ) can insert')
            self.append('\n2.more are going to append...')
        else:
            self.append('\nno such order')


# ['新建', '深度优先', '广度优先']
class RunButton_Graph(MyRunButton):
    def __init__(self, workplace, ls):
        super(RunButton_Graph, self).__init__(workplace)
        self.changeItems(ls)

    def menuSlot(self, t):
        if self.flag == 0:
            self.flag = 1
            return
        if t == '深度优先':
            self.getWorkplace().canvas.ergodic(0)
        elif t == "广度优先":
            self.getWorkplace().canvas.ergodic(1)
        elif t == '新建':
            self.getWorkplace().canvas.addNode(self.getWorkplace().canvas.nodeCount)


class WorkPlace(QWidget):

    def __init__(self, t='Canvas', te='有向图', ls=None):  # 参数为text和textEdition
        super(WorkPlace, self).__init__()

        if ls is None:
            ls = []
        self.edition = "图"
        self.title = t
        self.textEdition = te
        self.funcList = ls

        # 组件
        self.info = Info_Graph(self.title, self.textEdition)
        if self.textEdition == "无向图":
            self.canvas = Canvas_Graph_Undirected(self)
        elif self.textEdition == "有向图":
            self.canvas = Canvas_Graph(self)
        self.runButton = RunButton_Graph(self, ls)
        self.logInfo = LogInfo_Graph(self)

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
        self.setMinimumSize(800, 600)
        self.resize(800, 600)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.layout2.setContentsMargins(20, 0, 0, 20)
        self.layout3.setContentsMargins(0, 0, 0, 0)
        self.setAutoFillBackground(True)
        palette = QPalette()
        palette.setBrush(QPalette.Background, QColor(255, 255, 255))
        self.setPalette(palette)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = WorkPlace('canvas', '无向图', ['新建', '深度优先', '广度优先'])
    win.show()
    sys.exit(app.exec_())
