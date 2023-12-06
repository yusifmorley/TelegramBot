# coding: utf-8

from sqlalchemy import BigInteger, Column, Date, Integer, String, Text, text, create_engine, VARCHAR
from sqlalchemy.dialects.mssql import TINYINT
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import get_config

# 命令行运行报错 相关MySQ python依赖没有安装 关闭系统代理
# sqlacodegen mysql://root:root@localhost/telegramdata  > models.py
# ubuntu 需要安装依赖  apt-get install python3.10-dev libmysqlclient-dev
Base = declarative_base()


class BanUserLogo(Base):
    __tablename__ = 'ban_user_logo'

    uid = Column(BigInteger, primary_key=True)
    usr_name = Column(String(30), nullable=False)
    word = Column(Text, nullable=False)
    ban_word = Column(String(30), nullable=False)


class BanWord(Base):
    __tablename__ = 'ban_word'

    id = Column(Integer, primary_key=True)
    word = Column(String(10), nullable=False)


class CreateThemeLogo(Base):
    __tablename__ = 'create_theme_logo'

    uid = Column(BigInteger, primary_key=True)
    color_1 = Column(String(20))
    color_2 = Column(String(20))
    color_3 = Column(String(20))
    pic_path = Column(VARCHAR(100))
    callback_id = Column(BigInteger)
    flag = Column(TINYINT, server_default=text("'0'"))


class GroupInfo(Base):
    __tablename__ = 'group_info'

    uid = Column(BigInteger, primary_key=True, comment='群聊id')
    link = Column(VARCHAR(255), comment='群组链接')
    group_name = Column(String(255), comment='群名')
    can_delete = Column(TINYINT, comment='机器人在此群里是否能删除消息')
    can_restrict = Column(TINYINT, comment='机器人在此群里是否能限制用户')


class User(Base):
    __tablename__ = 'user'

    uid = Column(BigInteger, primary_key=True, comment='用户id')
    full_name = Column(String(255))
    link = Column(String(255))
    language_code = Column(String(255))


class UserUseRecord(Base):
    __tablename__ = 'user_use_record'

    uid = Column(BigInteger, primary_key=True, nullable=False, comment='用户id')
    date = Column(Date, primary_key=True, nullable=False, comment='日期')
    count_record = Column(Integer, comment='使用次数')


engine = create_engine(get_config.get_engine_str())
DBSession = sessionmaker(bind=engine)
seesion = DBSession()


def init_session():
    return seesion  # 返回seesion实例
