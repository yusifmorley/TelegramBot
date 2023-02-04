import ast


def getDic(a):  # 主题获取 属性和参数 的字典格式
    fil = open(a, "rb")
    fils = fil.readlines()
    s = b''
    for x in fils:

        if x == b'WPS\n':
            break
        s += x

    ss = b'{"' + s.rstrip(b'\n').replace(b'=', b'":"').replace(b'\n', b'",\n"') + b'"}'

    bi_gdic = ast.literal_eval(ss.decode("UTF-8"))

    return bi_gdic
