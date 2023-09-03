import requests
from urllib.parse import quote
import ast
import base64

from telegram import InlineKeyboardButton

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


def get_attheme(pic_byte: bytes,color_list:list):
    head = {
        'Content-Type': 'application/json'
    }
    picb = str(base64.b64encode(pic_byte),encoding='utf-8')
    #picObj = {'picb': picb, 'colors': color_list},
    picObj={'picb': picb, 'colors': color_list}
    # content = requests.post(url1, data=picObj,headers=head).content

    content = requests.post(url1, json=ast.literal_eval(str(picObj)), headers=head).content
    if content != b'fail':
        return content  # 返回内容
    else:
        return None

def get_kyb(arr:list):
    if len(arr)==5:
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
                # InlineKeyboardButton("全部随机", callback_data='default'),
             ],
        ]
        return keyboard
    else:
        return None

if __name__=='__main__':
    fo= open('../../src/background/Green Mystery.jpg', 'rb').read()
    # map=ast.literal_eval(get_attheme(fo).decode('utf-8'))
    # print(map['arr'])
    # print(base64.b64decode(map['photo']))
    list=['#706664', '#e3dbd2', '#2b2c37']
    print(get_attheme(fo,list))

