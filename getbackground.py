def getbackground(a): #Theme/ 开头
    with open(a, "rb") as hup:
        file = hup.read()
        ai = file.find(b'WPS')
        hup.seek(ai, 0)
        file=hup.read()
        pic = file.replace(b'WPS\n', b'').replace(b'\nWPE\n', b'')
        b=a.replace("attheme","jpg").replace("temptheme/","")
        with open("background/"+b, "wb") as ui:
            ui.write(pic)
        return "background/"+b



