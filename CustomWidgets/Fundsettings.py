import os


def length(ls):
    return sum(i is not None for i in ls)


class Fundsettings:
    path = os.path.abspath(__file__).split('\\')
    resource_path = '/'.join(path[:-2]) + "/mySources"  # 资源路径
    font_family = "楷体"  # 字体

    normalStyles = 1
    animatingStyles = 2

    random_Fill = 3
    appoint_Fill = 4
