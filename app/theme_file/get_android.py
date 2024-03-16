import os
import random
from app.util import get_preview

set_android = []


def init_android():
    global set_android
    set_android = os.listdir("src/Theme/android-theme")
    random.shuffle(set_android)


def get_android_theme():  # 获取随机主题链接
    global set_android
    # 每一次都随即打乱
    if len(set_android) == 0:
        init_android()

    global current
    current = set_android.pop()
    return current


def get_android_preview(theme_name, fd):
    res = get_preview.get_from("android", theme_name, fd)
    if res is not None:
        return res
    return None


init_android()
