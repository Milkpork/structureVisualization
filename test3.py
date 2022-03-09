import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit


class Demo(QWidget):
    def __init__(self):
        super(Demo, self).__init__()
        self.mainLayout = QVBoxLayout()

        self.buttonWidget = QWidget()
        self.buttonLayout = QHBoxLayout()

        self.button1 = QPushButton('删除')
        self.button2 = QPushButton('新建')
        self.button3 = QPushButton('关闭')

        self.inputWidget = QWidget()
        self.inputLayout = QHBoxLayout()

        self.name = QLabel('姓名')
        self.nameInput = QLineEdit()

        self.myLayouts()

    def myLayouts(self):
        self.setLayout(self.mainLayout)
        self.mainLayout.addWidget(self.buttonWidget)
        self.mainLayout.addWidget(self.inputWidget)

        self.buttonWidget.setLayout(self.buttonLayout)
        self.inputWidget.setLayout(self.inputLayout)

        self.buttonLayout.addWidget(self.button1)
        self.buttonLayout.addWidget(self.button2)
        self.buttonLayout.addWidget(self.button3)

        self.inputLayout.addWidget(self.name)
        self.inputLayout.addWidget(self.nameInput)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = Demo()
    demo.show()
    sys.exit(app.exec_())
