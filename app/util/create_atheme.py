import requests
from urllib.parse import quote
import ast
import base64

from telegram import InlineKeyboardButton

from app.util.color_parse import is_light, parse_color

#与nodejs 交互 发送一个图片
url0= "http://127.0.0.1:3000/attheme"

url1= "http://127.0.0.1:3000/attheme-create"
def get_attheme_color_pic(byte_arr:bytes):
    head = {
        'Content-Type': 'application/octet-stream'
    }

    # if theme_type == "android":
    #    url = main_url0 + quote(theme_name)
    # else:
    #    url = main_url1 + quote(theme_name)

    content= requests.post(url0, data=byte_arr, headers=head).content

    if content != b'fail':

        map = ast.literal_eval(content.decode('utf-8'))

        return [map['arr'],base64.b64decode(map['photo'])]  #返回内容

    else:
        return None


def get_attheme(pic_byte: bytes,color_list:list,flag=False):
    url=url1
    head = {
        'Content-Type': 'application/json'
    }
    picb = str(base64.b64encode(pic_byte),encoding='utf-8')
    #picObj = {'picb': picb, 'colors': color_list},
    picObj={'picb': picb, 'colors': color_list}
    # content = requests.post(url1, data=picObj,headers=head).content

    #如果为真 就是透明主题
    if flag:
        url=url1+"/tran"

    content = requests.post(url, json=ast.literal_eval(str(picObj)), headers=head).content
    if content != b'fail':
        return content  # 返回内容
    else:
        return None

def get_kyb(arr:list[str]):
    autocolor:list=[]
    autocolor1: list = []
    if len(arr) == 5:
        for x in arr:
            if not is_light(parse_color(x[1:])): #如果有一个是暗色
                autocolor.append(x)
                autocolor.append('#FFFFFF')
                autocolor.append('#FFFFFF')
                break
        if len(autocolor) == 0:  # 全是亮色
            autocolor.append(arr[0])
            autocolor.append('#000000')
            autocolor.append('#000000')

        for x in arr:
            if  is_light(parse_color(x[1:])):  #如果有一个是亮色
                autocolor1.append(x)
                autocolor1.append('#000000')
                autocolor1.append('#000000')
                break

        if len(autocolor1) == 0:  # 全是暗色
            autocolor1.append(arr[0])
            autocolor1.append('#FFFFFF')
            autocolor1.append('#FFFFFF')

        keyboard = [
            [
                InlineKeyboardButton("1", callback_data=arr[0]),
                InlineKeyboardButton("2", callback_data=arr[1]),
                InlineKeyboardButton("3", callback_data=arr[2]),
                InlineKeyboardButton("4", callback_data=arr[3]),
                InlineKeyboardButton("5", callback_data=arr[4]),

            ],
            [
                InlineKeyboardButton("白", callback_data='#FFFFFF'),
                InlineKeyboardButton("黑", callback_data='#000000'),
                InlineKeyboardButton("随机暗色", callback_data=",".join(autocolor)),
                InlineKeyboardButton("随机亮色", callback_data=",".join(autocolor1))

             ],
        ]
        return keyboard
    else:
        return None

#获取透明键盘
def get_transparent_ky():
    keyboard = [
        [
            InlineKeyboardButton("结束编辑", callback_data="off"),
            InlineKeyboardButton("透明主题", callback_data='tran'),

        ]

    ]
    return keyboard



if __name__=='__main__':
    fo= open('../../src/background/Green Mystery.jpg', 'rb').read()
    # map=ast.literal_eval(get_attheme(fo).decode('utf-8'))
    # print(map['arr'])
    # print(base64.b64decode(map['photo']))
    list=['#706664', '#e3dbd2', '#2b2c37']
    print(get_attheme(fo,list))

