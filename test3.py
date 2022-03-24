import sys

from PyQt5.QtWidgets import QMainWindow, QApplication

from Structures import LinearList


class mainWindow(QMainWindow):
    def __init__(self):
        super(mainWindow, self).__init__()
        self.temp = LinearList()
        self.temp.setParent(self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = mainWindow()
    win.show()
    sys.exit(app.exec_())
