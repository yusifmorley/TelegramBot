import base64
from PIL import Image
from io import BytesIO


def getpicbas(a):  # 剪辑图片 并返回 base64格式
    # with open("background/"+a.replace("attheme","jpg").replace("temptheme/",""),"rb")as hu:
    img = Image.open("background/" + a.replace("attheme", "jpg").replace("Theme/", ""))
    width, height = img.size
    byy = BytesIO()
    # img2=img.crop((100,100,200,200))
    # img2.save("len2.jpg")

    if width > height:
        w = height * 8 / 11
        if w > width / 2.7:  # 溢出
            h = height
            while (True):
                h -= 1
                if h * 8 / 11 < width / 2.7:
                    break
            img2 = img.crop(
                (int(width / 2.7), int((height - h) / 2), int(h * 8 / 11 + width / 2.7), int((height - h) / 2) + h))
            img2.save(byy, format="JPEG")
        else:
            img2 = img.crop((int(width / 2.7), 0, int(width / 2.7 + w), int(height)))
            img2.save(byy, format="JPEG")

    else:
        h = width * 11 / 8
        if h > height:
            nw = width
            while (True):
                nw -= 1
                if nw * 11 / 8 < height:
                    break
            img2 = img.crop((int((width - nw) / 2), int((height - h) / 2), int((width - nw) / 2 + nw),
                             int((height - h) / 2 + nw * 11 / 8)))
            img2.save(byy, format="JPEG")

        else:
            img2 = img.crop((0, int((height - h) / 2), width, int((height - h) / 2 + h)))
            img2.save(byy, format="JPEG")
    bas = base64.b64encode(byy.getvalue())
    return bas.decode("utf-8")
