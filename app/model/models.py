# coding: utf-8

from sqlalchemy import BigInteger, Column, Date, Integer, String, Text, text, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.mysql import TINYINT
from app.config import get_config
#命令行运行报错 相关MySQ python依赖没有安装 关闭系统代理
# sqlacodegen mysql://root:root@localhost/telegramdata  > models.py
#ubuntu 需要安装依赖  apt-get install python3.10-dev libmysqlclient-dev
Base = declarative_base()


class BanUserLogo(Base):
    __tablename__ = 'ban_user_logo'

    uid = Column(BigInteger, primary_key=True)
    usr_name = Column(String(30), nullable=False)
    word = Column(Text, nullable=False)
    ban_word = Column(String(30), nullable=False)


class Banword(Base):
    __tablename__ = 'banword'

    id = Column(Integer, primary_key=True)
    word = Column(String(10), nullable=False)


class CreateThemeLogo(Base):
    __tablename__ = 'create_theme_logo'

    uid = Column(BigInteger, primary_key=True)
    color_1 = Column(String(20))
    color_2 = Column(String(20))
    color_3 = Column(String(20))
    pic_path = Column(String(100))
    callback_id = Column(BigInteger)
    flag = Column(TINYINT, server_default=text("'0'"))

class UserUseRecord(Base):
    __tablename__ = 'user_use_record'

    uid = Column(BigInteger, primary_key=True, nullable=False, comment='用户id')
    date = Column(Date, primary_key=True, nullable=False, comment='日期')
    count_record = Column(Integer, comment='使用次数')


class User(Base):
    __tablename__ = 'user'

    uid = Column(BigInteger, primary_key=True, comment='用户id')
    full_name = Column(String(255))
    link = Column(String(255))
    language_code = Column(String(255))

engine = create_engine(get_config.get_engine_str())
# 自动提交事务
DBSession = sessionmaker(bind=engine)
seesion=DBSession()
def init_session():
     return seesion   #返回seesion实例
