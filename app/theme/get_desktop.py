import os
import random

set_desktop=[]

def init_desktop():
    global set_desktop
    set_desktop = os.listdir("src/Theme/desktop-theme")
    random.shuffle(set_desktop)
def get_desktop_theme():   #获取随机主题链接
    global set_desktop
     #每一次都随即打乱
    if len(set_desktop) ==0:
        init_desktop()
    return set_desktop.pop()

init_desktop()