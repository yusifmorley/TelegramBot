import telegram
lis=[
   # ['getrandomtheme', '随机获取一个安卓或桌面种类的主题链接(有时主题可能不适用于您的设备)'],
   # ['getandroidtheme', '随机获取一个安卓主题文件'] ,
   # ['getdesktoptheme', '随机获取一个桌面主题文件'],
   ['getiostheme', '随机获取一个IOS主题链接'],
   # ['create_attheme_base_pic', ' 基于图片创建attheme主题'],
   # ['create_tdesktop_base_pic','基于图片创建 tdesktop 主题']
]

def get_command():
    command=[]
    for x in lis:
        command.append(telegram.BotCommand(x[0],x[1]))
    return command

def get_command_str():
    con_str= "您可以输入以下命令：\n"
    for x in lis:
        con_str+= "{},{} \n".format(x[0], x[1])
    return con_str
