from PyQt5.Qt import *
import sys

app = QApplication(sys.argv)

w = QWidget()
w.setWindowTitle("QFrame")
w.resize(300, 300)

fra = QFrame(w)
fra.resize(100, 100)
# fra.setStyleSheet("background-color:green")

fra.setLineWidth(0)  # 设置外线宽度
fra.setMidLineWidth(0)  # 设置中线宽度
fra.setFrameStyle(QFrame.WinPanel | QFrame.Raised)
fra.setFrameRect(QRect(10, 10, 80, 80))  # 这是边框x, y, width, height

w.show()

sys.exit(app.exec_())
