import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QBoxLayout
from PyQt5.QtCore import QSize


class Label(QLabel):
    def minimumSizeHint(self):  # 建议的最小尺寸函数
        return QSize(50, 50)


class Demo(QWidget):

    def __init__(self):
        super(Demo, self).__init__()
        self.resize(300, 300)
        self.label1 = Label('标签1')
        self.label2 = QLabel('标签2')
        self.label3 = QLabel('标签3')
        self.label1.setStyleSheet('background-color: rgb(255, 0, 0)')
        self.label2.setStyleSheet('background-color: rgb(0, 255, 0)')
        self.label3.setStyleSheet('background-color: rgb(0, 0, 255)')

        layout = QBoxLayout(QBoxLayout.RightToLeft)  # 创建一个盒子布局
        # 参数1  布局方向:  --必须有
        # QBoxLayout.TopToBottom=2   从上往下
        # QBoxLayout.BottomToTop=3  从下往上
        # QBoxLayout.LeftToRight=0   从左往右
        # QBoxLayout.RightToLeft=1  从右往左

        self.setLayout(layout)  # 给self设置布局管理器

        layout.addWidget(self.label1)  # 给布局管理器添加控件
        # 这是QLayout的指令

        # layout.addSpacing(50)  #添加间距-间距
        # 参数   像素

        layout.addWidget(self.label2)
        layout.addWidget(self.label3)

        layout.setSpacing(2)  # 设置内边距---控件之间的距离
        # 这是QLayout的指令

        layout.setContentsMargins(20, 30, 40, 50)  # 设置外边距--控件到窗口边框的距离
        # 这是QLayout的指令
        # 参数1 左边距离
        # 参数2 上边距离
        # 参数3 右边距离
        # 参数4 下边距离

        self.label4 = QLabel('标签4')
        self.label4.setStyleSheet('background-color: yellow')

        layout.replaceWidget(self.label2, self.label4)  # 替换控件
        # 把self.label2替换成self.label4
        # 注意：被替换掉的控件不在受布局管理器的控制，要把它隐藏或删除或脱离或添加到别的布局管理器中
        # 这是QLayout的指令

        # self.label2.hide()  #隐藏控件
        self.label2.setParent(None)  # 脱离父对象

        # 布局的嵌套：
        self.label5 = QLabel('标签5')
        self.label5.setStyleSheet('background-color: rgb(255, 255, 0)')
        self.label6 = QLabel('标签6')
        self.label6.setStyleSheet('background-color: rgb(255, 0, 255)')
        self.label7 = QLabel('标签7')
        self.label7.setStyleSheet('background-color: rgb(0, 255, 255)')
        layout1 = QBoxLayout(QBoxLayout.BottomToTop)
        layout1.addWidget(self.label5)
        layout1.addWidget(self.label6)
        layout1.addWidget(self.label7)

        # layout.addLayout(layout1)  #添加布局管理器
        # 这是QLayout的指令

        layout.setDirection(QBoxLayout.LeftToRight)  # 设置方向
        # direction()  返回方向

        layout.insertWidget(3, self.label2)  # 插入控件
        # 参数1   位置序号

        layout.insertLayout(2, layout1)  # 插入布局
        # 参数1   位置序号

        # layout.removeWidget(self.label1)  #从布局中移除控件
        # 不是删除控件

        layout.insertSpacing(4, 50)  # 插入空白-间距
        # 参数1  位置索引--不包括已有空白
        # 参数2  空白像素

        layout.setEnabled(True)  # 是否可用
        # 默认 True


if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = Demo()
    demo.show()
    sys.exit(app.exec_())
