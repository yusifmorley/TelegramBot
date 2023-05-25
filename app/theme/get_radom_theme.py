import os
import  random
#获取随即主题
sets=[]
def init():
    with open("F:\Project\pycharmProject\TelegramBot\src\ThemeLink\link.txt","r") as fp:
        global sets
        sets = os.listdir("F:\Project\pycharmProject\TelegramBot\src\Theme")
        links=fp.readlines()
        sets.extend(links)
def get_random_theme():
    global sets
    random.shuffle(sets) #每一次都随即打乱
    if len(sets) ==0:
        init()
    return sets.pop()
init()
