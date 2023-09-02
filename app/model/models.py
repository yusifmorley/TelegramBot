# coding: utf-8
from sqlalchemy import BigInteger, Column, Integer, String, Text, text, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.config import get_config
#命令行运行报错 相关MySQ python依赖没有安装 关闭系统代理
# sqlacodegen mysql://root:root@localhost/telegramdata  > models.py
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
    picpath = Column(String(100),nullable=False)

def init_session():
     engine = create_engine(get_config.get_engine_str())
     #自动提交事务
     DBSession = sessionmaker(bind=engine)
     return DBSession()   #返回seesion实例