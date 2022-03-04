def length(ls):
    count = 0
    for i in ls:
        if i is not None:
            count += 1
    return count


class Fundsettings:
    resource_path = "E:/structureVisualization/mySources"  # 资源路径
    font_family = "楷体"  # 字体

    normalStyles = 1
    animatingStyles = 2

    random_Fill = 3
    appoint_Fill = 4
