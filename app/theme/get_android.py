import os
import random

set_android=[]

def init_android():
    global set_android
    set_android = os.listdir("../../src/Theme/android-theme")
    random.shuffle(set_android)
def get_android_theme():   #获取随机主题链接
    global set_android
     #每一次都随即打乱
    if len(set_android) ==0:
        init_android()
    return set_android.pop()

init_android()