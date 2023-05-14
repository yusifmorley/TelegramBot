import os
import  random
#获取随即主题


sets=os.listdir("../../file/Theme")
def getRandomTheme():
    global sets
    random.shuffle(sets) #每一次都随即打乱
    if len(sets) ==0:
        sets =os.listdir("../../file/Theme")
    return sets.pop()
