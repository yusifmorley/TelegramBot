import os

import yaml
import mysql

# 装载配置

with open("setup.cfg", "r") as f:
    data = yaml.load(f, yaml.FullLoader)
    MysqlData = data["mysql"]

    if os.environ.get('ENV') == 'dev':
        MysqlData["password"] = 'root'

    TelegramBotId = data["telegrambotid"]

def get_engine_str():
    return  "mysql://{}:{}@127.0.0.1/{}".format(MysqlData["user"],MysqlData["password"],"telegramdata")



def getMysqlConfig():
    mydb = mysql.connector.connect(
        host=MysqlData["host"],
        user=MysqlData["user"],
        password=MysqlData["password"],
        database="telegramdata",
    )
    return mydb


def getTelegramId():
    return TelegramBotId
