def deletetxt(txt, str):
    for x in txt:
        if x in str:
            return x
    return None


def getbanword():  # 获取
    with open("banconfig/banword", "r") as fp:
        return fp.read().split("\n")


def writebanword(str): #
    with open("banconfig/banword", "a") as fp:
        fp.write(str+"\n")
