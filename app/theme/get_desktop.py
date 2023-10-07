import os
import random

from app.util import get_preview

set_desktop=[]

current=""
def init_desktop():
    global set_desktop
    set_desktop = os.listdir("src/Theme/desktop-theme")
    random.shuffle(set_desktop)
def get_desktop_theme():   #获取随机主题链接
    global set_desktop
     #每一次都随即打乱
    if len(set_desktop) ==0:
        init_desktop()
    global current
    current=set_desktop.pop()

    return set_desktop.pop()

def get_desktop_preview(theme_name, fd):
    res = get_preview.get_from("desktop", theme_name, fd)
    if res is not None:
        return res

    return None

init_desktop()