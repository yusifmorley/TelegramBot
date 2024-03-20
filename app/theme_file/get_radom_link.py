import os
import random
import sys

# 获取随机主题链接

# 获取随即主题
sets = []


# @profile
def init():
    with open("src/ThemeLink/link.txt", "r", encoding='utf8') as fp:
        global sets

        links = fp.readlines()
        sets.extend(links)
        random.shuffle(sets)
        # print(sys.getsizeof(sets))


def get_random_theme():  # 获取随机主题链接
    global sets
    # 每一次都随即打乱
    if len(sets) == 0:
        init()
    return sets.pop()


init()
