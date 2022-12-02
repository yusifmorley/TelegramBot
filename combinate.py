


# 将主题与图片合并
def combinate(themePatn, PhotoPath):
    with open(themePatn, "rb") as tPath:
        aa = tPath.read()
        if b'WLS' not in aa and b'WPS' not in aa:
            aa=aa+b'WLS'
        if b'WPS' in aa:
            s=aa.find(b'WPS')
            aa = aa.replace(aa[s:], b'WLS\n')

        m = aa.find(b'WLS')

    with open(PhotoPath, "rb") as pppth:
        aa = aa.replace(aa[m:], b'WPS\n' + pppth.read())

    newThemeFileName = themePatn.replace(themePatn[:themePatn.find("/")], "")

    with open("Theme" + newThemeFileName, "wb") as newFileCreate:
        newFileCreate.write(aa)

    return "Theme" + newThemeFileName   # 并返回系新主题路径


