# structureVisualization

structureVisualization是可以将数据结构尽可能地通过可视化的方式展现出来。

## 项目结构

-   CustomWidgets
    -   里面包含着每个小组件，包括:顶部条，信息展示框，运行按钮，画布及画布内需要的组件，输入控制台等。
-   mySources
    -   里面为项目所需要的资源文件，包含:图片等
-   Structures
    -   文件夹内包含若干个子文件夹，每一个代表着一种数据结构。(由于不同的数据结构的画板不同，所以对其进行完全重构)。
        -   每一个子文件夹下应当包含`MainWindow.py`和`WorkPlace.py`两个文件。`WorkPlace.py`为工作区，包含了信息，运行按钮，输入输出控制台及画布四部分。`MainWindow.py`为将剩余及工作区集成在一起。
-   在最外一层有着些许诸如`test.py`,`test2.py`，`main1.py`等的文件，都是临时测试文件，可删除修改。

## 代码规范

1.  命名规范：变量和函数名使用小驼峰，也可以使用`小写_小写`的形式。类名使用大驼峰的形式。尽量做到语义化，禁止使用a1,a2等变量名，临时的变量可以使用`_`或`temp什么什么的`来命名，并且做好注释。

2.  类的构造方式：以`E:\structureVisualization\CustomWidgets\MyTopBar.py`文件中的`MyTopBar`类为例：

    -   ```python
        # 实际函数被忽略，详见文件，以下注释为规范，不会出现在文件中
        class MyTopBar(QWidget):
            def __init__(self, wind, settingExists=True):
                super(MyTopBar, self).__init__()  # 第一行为调用父元素
                self.setStyleSheet("这里的参数不写了")  # 有需要设置样式表需直接在第二行设置
                
                # 设置成员变量
                self.window = wind
                self.m_flag = False
        		
                # 声明所有需要用到的组件
                self.mainLayout = QHBoxLayout()
                self.miniButton = minimizeButton(self.window)
                self.maxiButton = maximizeButton(self.window)
                self.exitButton = exitButton(self.window)
                self.settingButton = settingButton(self.window)
                self.settingsMenu = settingsMenu(self.window)
        		
                # 调用需要用到的成员函数，以下函数名固定
                self.mySettings()  # 一些参数的设置
                self.myLayouts()  # 布局设置
                self.mySignalConnections()  # 信号与槽的设置
                self.myStyles()  # 样式的设置（有些样式在第二行的样式表设置不出来）
        
            # 在函数的实现上，遵循 先写固定函数（没有可以不写）-> 重载函数 -> 自定义函数
        	# 首先是固定函数    
            def mySettings(self):
                pass
        
            def myLayouts(self):
                pass
        
            def mySignalConnections(self):
               	pass
        
            def myStyles(self):
                pass
        	# 以下是重载函数
            def mousePressEvent(self, event):
                pass
        
            def mouseMoveEvent(self, QMouseEvent):
                pass
        
            def mouseReleaseEvent(self, QMouseEvent):
                pass
        
            def mouseDoubleClickEvent(self, event):
                pass
        	# 以下是自定义函数
            def menuSlot(self, ac):
                # 本函数不完全是自定义函数，整个项目的menuSlot函数都是菜单的响应槽
                pass
        ```

        当有特殊类时（如有自定义信号发射时）可不遵循。