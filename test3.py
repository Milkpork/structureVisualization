import sys
from PyQt5.QtCore import QTimeLine
from PyQt5.QtWidgets import QApplication, QWidget, QLabel


class Demo(QWidget):
    def __init__(self):
        super(Demo, self).__init__()
        self.resize(600, 600)

        self.label = QLabel('Hello PyQt5', self)
        self.label.move(-100, 100)

        self.timeline = QTimeLine(5000, self)  # 实例化一个时间轴，持续时间为5秒
        self.timeline.setFrameRange(0, 700)  # 设置帧率范围，该值表示在规定的时间内将要执行多少帧
        self.timeline.frameChanged.connect(self.set_frame_func)  # 帧数变化时发出信号
        # 当动画开始后，帧数就会发生改变，每次帧数发生变化，就会发出frameChanged信号(该信号发送时附带当前所在帧数)
        self.timeline.setLoopCount(0)  # 传入0代表无限循环运行.传入正整数会运行相应次数，传入负数不运行
        self.timeline.start()  # 启动动画

    def set_frame_func(self, frame):  # 参数：接受到的帧数
        self.label.move(-100 + frame, 100)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = Demo()
    demo.show()
    sys.exit(app.exec_())
