# coding: utf-8
from sqlalchemy import BigInteger, Column, Integer, String, Text, text
from sqlalchemy.ext.declarative import declarative_base
#命令行运行报错 相关MySQ python依赖没有安装 关闭系统代理
# sqlacodegen mysql://root:root@localhost/telegramdata  > models.py
Base = declarative_base()
metadata = Base.metadata


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
    flag = Column(Integer, server_default=text("'0'"))
    themepath = Column(String(100))
    picpath = Column(String(100))
