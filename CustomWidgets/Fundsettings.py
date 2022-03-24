import os


class Fundsettings:
    path = os.path.abspath(__file__).split('\\')
    resource_path = '/'.join(path[:-2]) + "/mySources"  # 资源路径
    font_family = "楷体"  # font

    normalStyles = 1
    animatingStyles = 2


class FundColor:
    backgroundColor = "rgba(255, 250, 240, 1)"
    fontColor = "rgba(0, 0, 0, 1)"
    transparent = "rgba(0, 0, 0, 0)"

    # topbar button hover
    buttonHoverColor = "rgba(176, 196 ,222, .8)"

    # topbar background
    topbarBackgroundColor = "rgba(112, 128, 144, 1)"

    # runButton default color
    runButtonBackgroundColor = transparent

    # runButton click color
    runButtonClickColor = "rgba(200, 200, 200, 0.8)"

    # runButton hover color
    runButtonHoverColor = "rgba(200, 200, 200, 0.4)"

    # runButtonItem color
    runButtonItemBackgroundColor = "rgba(255, 255, 255, 1)"

    # runButtonItem hover color
    runButtonItemHoverColor = "rgba(255, 255, 255, 1)"

    # loginfo border
    loginfoBorderColor = "rgba(128, 128, 128, 1)"

    # loginfo border hover
    loginfoBorderHoverColor = "rgba(0, 0, 0, 1)"

    # singleTab background
    singleTabBackgroundColor = transparent

    # singleTab hover
    singleTabHoverColor = "rgba(150, 150, 150, 0.5)"

    # signleTab press
    singleTabPressColor = "rgba(0,0,128,.6)"

    # singleTab select
    singleTabSelectColor = "rgba(0,0,128,.6)"

    # addButton background
    addButtonBackgroundColor = transparent

    # addButton hover color
    addButtonHoverColor = "rgba(176,196,222, 1)"

    # tab background color
    tabBackgroundColor = "rgba(119,136,153, 1)"

    # submit button background
    submitButtonBackgroundColor = transparent

    # submit button press
    submitButtonPressColor = "rgba(255,222,173, 1)"

    # options background
    optionsBackgroundColor = transparent

    # option border
    optionBorderColor = "rgba(190, 190, 190, 1)"

    # option select
    optionsSelectColor = "rgba(255,165,0,1)"

    # input widget hover
    inputHoverBackgroundColor = "rgba(95,158,160 1)"

    # input border
    inputBorderColor = "rgba(139, 137, 112, 1)"

    inputSelectBorderColor = "rgba(0,0,0,1)"

    # settingDialog background
    settingDialogBackgroundColor = "rgba(	253,245,230, 1)"

    # singleClassButton background
    singleClassButtonBackgroundColor = transparent

    # singleClassButton select
    singleClassButtonSelectColor = "rgba(0,0,128,.6)"

    # classList background
    classListBackground = "rgba(119,136,153,1)"

    # node border
    nodeBorderColor = (0, 0, 0, 255)

    # node brush
    nodeBrushColor = (255, 255, 255, 255)
