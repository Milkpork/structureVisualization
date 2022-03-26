from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QCursor, QMouseEvent, QFont
from PyQt5.QtWidgets import QPushButton, QHBoxLayout, QMenu, QApplication, QMainWindow, QAction, QFileDialog, \
    QFrame
from CustomWidgets.Fundsettings import Fundsettings, FundColor
from CustomWidgets import pic


# 按钮基类
class TopBarButton(QPushButton):
    radius = 20  # 半径
    hover_color = FundColor.buttonHoverColor  # hover的颜色

    def __init__(self, window: QMainWindow = None):
        super(TopBarButton, self).__init__()
        self.window = window

        self.mySettings()

    def mySettings(self):
        self.setMaximumSize(self.radius, self.radius)
        self.setMinimumSize(self.radius, self.radius)
        self.setContentsMargins(0, 0, 0, 0)


# 首先定义右侧三个按钮 最小化/最大化/关闭
class minimizeButton(TopBarButton):
    def __init__(self, window: QMainWindow = None):
        super(minimizeButton, self).__init__(window)
        self.setStyleSheet(
            "minimizeButton{border-image: url(:pic/minimizeButton.png);border-radius: %dpx;}"
            "minimizeButton:hover{background-color:%s}" % (
                TopBarButton.radius // 2, TopBarButton.hover_color)
        )
        self.clicked.connect(self.minimize)

    # 最小化窗口
    def minimize(self):
        self.window.setWindowState(Qt.WindowMinimized)


class maximizeButton(TopBarButton):
    def __init__(self, window: QMainWindow = None):
        super(maximizeButton, self).__init__(window)
        self.setStyleSheet(
            "maximizeButton{border-image: url(:pic/maximizeButton.png);border-radius: %dpx;}"
            "maximizeButton:hover{background-color:%s}" % (
                TopBarButton.radius // 2, TopBarButton.hover_color)
        )
        self.clicked.connect(self.maximize)

    # 将窗口最大化
    def maximize(self):
        if self.window.isFullScreen():
            self.window.showNormal()
        else:
            self.window.setWindowState(Qt.WindowFullScreen)
        workplace = self.window.workplace
        for i in workplace.children():
            i.resize(workplace.width(), workplace.height())


class exitButton(TopBarButton):
    def __init__(self, window: QMainWindow = None):
        super(exitButton, self).__init__(window)
        self.setStyleSheet(
            "exitButton{border-image: url(:pic/exitButton.png);border-radius: %dpx;}"
            "exitButton:hover{background-color:%s}" % (
                TopBarButton.radius // 2, TopBarButton.hover_color)
        )
        self.clicked.connect(self.closeWindow)

    # 关闭窗口
    def closeWindow(self):
        self.window.close()


# 设置按钮
class settingButton(TopBarButton):
    def __init__(self, window: QMainWindow = None):
        super(settingButton, self).__init__(window)
        self.setStyleSheet(
            "settingButton{border-image: url(:pic/settingButton.png);border-radius: %dpx;}"
            "settingButton:hover{background-color: %s;}" % (
                TopBarButton.radius // 2, TopBarButton.hover_color)
        )


# 设置菜单
class settingsMenu(QMenu):
    font_size = 12

    def __init__(self, window: QMainWindow = None):
        super(settingsMenu, self).__init__()
        self.setStyleSheet(
            "settingsMenu{border:1px solid black;}"
            "settingsMenu::item{padding:0px 5px 0px 5px;}"
            "settingsMenu::item{height:20px;}"
            "settingsMenu::item{background:white;}"
            "settingsMenu::item:selected:enabled{background-color:rgba(200,200,200,.7);}"

            "settingsMenu::separator{height:1px;}"
            "settingsMenu::separator{background:black;}"
            "settingsMenu::separator{margin:0px 8px 0px 8px;}"
        )
        self.window = window

        self.mySettings()
        self.mySignalConnections()
        self.myMenu()

    def mySettings(self):
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint | Qt.NoDropShadowWindowHint)  # 设置无阴影背景
        self.setFont(QFont(Fundsettings.font_family, self.font_size))

    def mySignalConnections(self):
        self.triggered.connect(self.menuSlot)

    # 菜单内的选项
    def myMenu(self):
        self.addAction('新建')
        self.addSeparator()
        self.addAction('保存')
        self.addAction('导入')
        self.addSeparator()
        self.addAction('关闭')

    # 展示菜单
    def showMenu(self):
        self.exec_(QPoint(self.window.pos().x(), self.window.pos().y() + MyTopBar.fix_height - 1))  # 在setting按钮下方展示

    # 菜单对应的槽函数（事件）
    def menuSlot(self, ac: QAction):
        if ac.text() == "新建":
            self.window.nav.addTab()
        elif ac.text() == "保存":
            self.saveFunc()
        elif ac.text() == "导入":
            self.loadFunc()
        elif ac.text() == "关闭":
            self.window.close()

    def saveFunc(self):
        workplace = self.window.nav.getNowWorkplace()
        if workplace is None:
            return
        title = workplace.title
        edition = workplace.textEdition
        funcList = workplace.funcList

        canv = workplace.canvas
        node = {}
        line = {}
        hnode = None
        canvType = workplace.edition
        index = 0
        for i in canv.nodeDic:
            node[canv.nodeDic[i]] = [f"{index}", canv.nodeDic[i].text.text()]
            index += 1
        for i in canv.lineDic:
            if line.get(node[canv.lineDic[i].startNode][0], -1) == -1:
                line[node[canv.lineDic[i].startNode][0]] = []
            line[node[canv.lineDic[i].startNode][0]].append(
                [node[canv.lineDic[i].endNode][0], canv.lineDic[i].stlistName,
                 canv.lineDic[i].edlistName])
        if canv.headNode is not None:
            hnode = node[canv.headNode][0]
        pos = {}
        for i in node:
            pos[node[i][0]] = (i.pos().x(), i.pos().y())

        node_res = {}
        for i in node.values():
            node_res[i[0]] = i[1]
        resText = f"<type> {canvType}\n<title> {title}\n<edition> {edition}\n<functions> {funcList}\n<node> {node_res}\n<connections> {line}\n<headNode> {hnode}\n<positions> {pos}"
        fname, ok = QFileDialog.getSaveFileName(self, "文件保存", "./", "Text Files(*.stru)")
        if ok:
            with open(fname, 'w+', encoding='utf8') as f:
                f.write(resText)

    def loadFunc(self):
        try:
            fname, ok = QFileDialog.getOpenFileName(self, "选取文件", "./", "Text Files (*.stru)")
            if ok:
                orderDic = {}
                with open(fname, "r", encoding="utf8") as f:
                    content = f.readline()
                    while content:
                        order = content.rstrip("\n").split(" ", 1)
                        if len(order) < 2:
                            order += [""]
                        orderDic[order[0]] = order[1]
                        content = f.readline()

                types = orderDic['<type>']
                title = orderDic["<title>"]
                edition = orderDic["<edition>"]
                function = eval(orderDic["<functions>"])
                nodeDict = eval(orderDic["<node>"])
                connectDict = eval(orderDic["<connections>"])
                head = orderDic["<headNode>"]
                posDict = eval(orderDic["<positions>"])
                self.window.nav.addTabAppoint(types, title, edition, function)
                canv = self.window.nav.getNowWorkplace().canvas
                for i in nodeDict:
                    canv.addNode(nodeDict[i], posDict[i][0], posDict[i][1])
                for i in connectDict:
                    for j in connectDict[i]:
                        canv.addLine(canv.nodeDic[f"node{i}"], canv.nodeDic[f"node{j[0]}"], j[1], j[2])
                canv.setHeadNode(canv.nodeDic[f"node{head}"])

        except:
            pass


# 顶部条(主类)
class MyTopBar(QFrame):
    bc_color = FundColor.topbarBackgroundColor  # 背景颜色
    fix_height = 40  # 固定高度

    def __init__(self, wind: QMainWindow, buttonExists: list = None):
        """
        注意：使用本工具条会自动为窗口设置为FramelessWindowHint
        第一个参数用于设置该顶部条的窗口是哪个
        第二个参数True表示需要设置按钮，False为不显示设置按钮
        """
        if buttonExists is None:
            buttonExists = [1, 1, 1, 1]
        super(MyTopBar, self).__init__()
        self.setStyleSheet(
            "QFrame{background-color: %s;border:1px solid white;}" % (
                self.bc_color
            )
        )
        self.window = wind
        self.m_flag = False
        self.m_Position = None

        self.mainLayout = QHBoxLayout()
        self.miniButton = minimizeButton(self.window)
        self.maxiButton = maximizeButton(self.window)
        self.exitButton = exitButton(self.window)
        self.settingButton = settingButton(self.window)
        self.settingsMenu = settingsMenu(self.window)

        # if not settingExists:
        #     self.settingButton.setVisible(False)
        self.judge(buttonExists)  # 用于判断是有需要按钮

        self.mySettings()
        self.myLayouts()
        self.mySignalConnections()
        self.myStyles()

    def judge(self, buttonExists):
        if buttonExists[1] * buttonExists[2] == 0:
            # noinspection PyUnusedLocal
            def funtemp(event):
                pass

            # noinspection PyAttributeOutsideInit
            self.mouseDoubleClickEvent = funtemp
        button = [self.settingButton, self.miniButton, self.maxiButton, self.exitButton]
        for i in range(4):
            button[i].setVisible(buttonExists[i])

    def mySettings(self):
        # 设置固定高度
        self.setFixedHeight(self.fix_height)

    def myLayouts(self):
        self.mainLayout.setSpacing(10)
        self.mainLayout.setContentsMargins(10, 0, 10, 0)

        self.setLayout(self.mainLayout)
        self.mainLayout.addStretch(0)
        self.mainLayout.addWidget(self.settingButton)

        self.mainLayout.addStretch(1)
        self.mainLayout.addWidget(self.miniButton)
        self.mainLayout.addWidget(self.maxiButton)
        self.mainLayout.addWidget(self.exitButton)

    def mySignalConnections(self):
        self.settingButton.clicked.connect(self.settingsMenu.showMenu)

    def myStyles(self):
        # 设置窗口为无边框样式
        self.window.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)

    # press+move+release三者构成窗口可拖拽
    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.m_flag = True
            self.m_Position = event.globalPos() - self.window.pos()  # 获取鼠标相对窗口的位置
            event.accept()
            self.setCursor(QCursor(Qt.OpenHandCursor))  # 更改鼠标图标

    def mouseMoveEvent(self, event: QMouseEvent):
        if Qt.LeftButton and self.m_flag:
            if self.window.isFullScreen():
                self.window.showNormal()
                desktop = QApplication.desktop()
                flag = QCursor().pos().x() / desktop.width()  # 系数
                self.window.move(int(QCursor().pos().x() - self.window.width() * flag),
                                 QCursor().pos().y() - self.height() // 2)
                self.m_Position = event.globalPos() - self.window.pos()  # 获取鼠标相对窗口的位置
            else:
                self.window.move(event.globalPos() - self.m_Position)  # 更改窗口位置
            event.accept()
            workplace = self.window.workplace
            for i in workplace.children():
                i.resize(workplace.width(), workplace.height())

    def mouseReleaseEvent(self, event: QMouseEvent):
        self.m_flag = False
        self.setCursor(QCursor(Qt.ArrowCursor))

    # 双击改变状态
    def mouseDoubleClickEvent(self, event: QMouseEvent):
        if self.window.isFullScreen():
            self.window.showNormal()
        else:
            self.window.setWindowState(Qt.WindowFullScreen)  # 全屏
        workplace = self.window.workplace
        for i in workplace.children():
            i.resize(workplace.width(), workplace.height())


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QMainWindow


    class test(QMainWindow):
        def __init__(self):
            super(test, self).__init__()
            a = MyTopBar(self)
            self.setCentralWidget(a)
            self.resize(400, 400)


    app = QApplication(sys.argv)
    win = test()
    win.show()
    sys.exit(app.exec_())
