import sys
# from PyQt5.Qt import *
from PyQt5.QtCore import QLineF
from PyQt5.QtGui import QPen
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QGraphicsScene, QGraphicsView, QGraphicsLineItem


# ##############################预设好的框架#####################################
class MyWin(QWidget):
    def __init__(self):
        super(MyWin, self).__init__()
        super().__init__()
        self.setWindowTitle("Image Viewer")
        self.setFixedSize(1000, 600)
        self.verticalLayout = QVBoxLayout(self)

        self.gr_scene = QGraphicsScene(self)
        self.gr_view = QGraphicsView(self.gr_scene)

        self.verticalLayout.addWidget(self.gr_view)
        # ##############################预设好的框架#####################################
        # ##############################在下面实现相应功能并保存对应的笔记中#####################################
        self.gr_scene.mousePressEvent = self.scene_mousePressEvnet
        self.gr_scene.mouseMoveEvent = self.scene_mouseMoveEvnet

    def scene_mousePressEvnet(self, event):
        self.start_pos = event.scenePos()
        # self.start_pos=self.gr_view.mapToScene(pos)
        print(self.start_pos.x())
        self.line = QGraphicsLineItem()
        # self.line.setPen(QPen())
        self.gr_scene.addItem(self.line)
        # print("self.start_pos=",self.start_pos)

    def scene_mouseMoveEvnet(self, event):
        self.end_pos = event.scenePos()
        print("self.end_pos=", self.end_pos)
        self.line.setLine(QLineF(self.start_pos.x(), self.start_pos.y(), self.end_pos.x(), self.end_pos.y()))


def run_my_win():
    app = QApplication(sys.argv)
    mywin = MyWin()
    mywin.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    run_my_win()
