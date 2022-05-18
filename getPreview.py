import xml.etree.ElementTree as etree
from getsetting import *
from getpicbyterbase64 import *



def getPreview(b):
    # etree.Element('{http://www.w3.org/2000/svg}svg')
    tree = etree.parse("theme-preview.svg")
    root = tree.getroot()

    root.set("xmlns:xlink", "http://www.w3.org/1999/xlink")
          #提取背景
    for x in root:
        if "class" in x.attrib:
            if x.attrib["class"] == "IMG":
                x.set("xlink:href", "data:preview/jpeg;base64," + getpicbas(b))
            else:
                x.set("fill", getfill(x.attrib["class"], b))
                x.set("fill-opacity", getfillopacity(x.attrib["class"], b))
    m = b.replace("attheme", "svg").replace("Theme/", "")
    tree.write("preview/" + m)          #生成预览
    pre={"preview":"preview/" + m}
    return   pre         #返回相关信息
