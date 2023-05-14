from jnius import autoclass
import ast
from app.theme.dicsetting import getDic


def gethex(s):  # 获取渲染 数据
    if s == "0":
        return "{" + "\"fill\":\"" + "#fff" + "\" ,\"fill-opacity\":\"0\"}"

    if ("#" != list(s)[0]):
        sixteen = autoclass("java.lang.Integer").toHexString(int(s))
    else:
        sixteen = str(list(s)[1:])
    if len(sixteen) > 6:
        a = "".join(list(sixteen)[0:2])
        ai = int(a, 16)

        return "{" + "\"fill\":\"" + "#" + sixteen[2:] + "\" ,\"fill-opacity\":\"" + str(float(ai) / 255.0) + "\"}"

    else:
        if len(sixteen) < 6:
            return "{" + "\"fill\":\"" + "#ffffff" + "\" ,\"fill-opacity\":\"0\"}"
        return "{" + "\"fill\":\"" + "#" + str(sixteen) + "\" ,\"fill-opacity\":\"0\"" + "}"


# a=gethex("-80000")
# h=ast.literal_eval(a)
# print(h["fill"])
#


def getfill(cla, b):
    dic = getDic(b)  # 返回主题字典
    if cla in dic:
        p = dic[cla]
    else:
        p = "0"
    w = gethex(p)

    h = ast.literal_eval(w)
    return h["fill"]


def getfillopacity(cla, b):
    dic = getDic(b)
    if cla in dic:
        p = dic[cla]
    else:
        p = "0"

    w = gethex(p)
    h = ast.literal_eval(w)
    return h["fill-opacity"]
