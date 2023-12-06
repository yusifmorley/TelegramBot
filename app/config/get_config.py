import os

import yaml
import mysql

# 装载配置

with open("setup.cfg", "r") as f:
    data = yaml.load(f, yaml.FullLoader)
    MysqlData = data["mysql"]

    if os.environ.get('ENV') == 'dev':
        MysqlData["password"] = 'root'


def get_engine_str():
    passw: str = MysqlData["password"]
    passw = passw.replace("@", "%40")
    return "mysql://{}:{}@127.0.0.1/{}".format(MysqlData["user"], passw, data["database_name"])


def get_mysql_config():
    mydb = mysql.connector.connect(
        host=MysqlData["host"],
        user=MysqlData["user"],
        password=MysqlData["password"],
        database=data["database_name"],
    )
    return mydb


def get_telegram_id():
    return data["telegram_bot_id"]


def get_myid():
    return data['myid']
