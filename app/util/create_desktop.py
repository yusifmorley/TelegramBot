from typing import List

import requests
import ast
import base64
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from app.exception.my_exception import NoSuitParmException
from app.logger import t_log
from app.util.color_parse import is_light, parse_color

logger = t_log.get_logging().getLogger(__name__)
url0 = "http://127.0.0.1:5000/tdesktop-create"

# TODO 传参测试 日志
def get_tdektop(pic_byte, color_list:List[str], flag: bool):
    # 参数检测
    logger.info("get_tdektop 正在检测参数")

    logger.info(f"{color_list}")
    for x in color_list:
        if not x.startswith("#"):
            logger.error(f"错误！ color_list为 {color_list}")
            raise NoSuitParmException("错误的参数")


    url = url0
    head = {
        'Content-Type': 'application/json'
    }
    picb = str(base64.b64encode(pic_byte), encoding='utf-8')
    picObj = {'picb': picb, 'colors': color_list, 'flag': flag}

    content = requests.post(url, json=ast.literal_eval(str(picObj)), headers=head).content
    if content != b'fail':
        return content  # 返回内容
    else:
        return None


def get_desktop_kyb(arr: list[str]):
    autocolor: list = []
    autocolor1: list = []
    if len(arr) == 5:
        for x in arr:
            if not is_light(parse_color(x[1:])):  # 如果有一个是暗色
                autocolor.append(x)
                autocolor.append('#FFFFFF')
                break
        if len(autocolor) == 0:  # 全是亮色
            autocolor.append(arr[0])
            autocolor.append('#000000')

        for x in arr:
            if is_light(parse_color(x[1:])):  # 如果有一个是亮色
                autocolor1.append(x)
                autocolor1.append('#000000')
                break

        if len(autocolor1) == 0:  # 全是暗色
            autocolor1.append(arr[0])
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
                InlineKeyboardButton("随机亮色", callback_data=",".join(autocolor)),
                InlineKeyboardButton("随机暗色", callback_data=",".join(autocolor1))
            ],
        ]
        return InlineKeyboardMarkup(keyboard)
    else:
        return None
