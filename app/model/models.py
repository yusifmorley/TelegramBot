# coding: utf-8
from sqlalchemy import BigInteger, Column, Date, Integer, text, create_engine
from sqlalchemy.dialects.mysql import ENUM, INTEGER, MEDIUMTEXT, TINYINT, VARCHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.config import get_config

# 命令行运行报错 相关MySQ python依赖没有安装 关闭系统代理
# pip install mysqlclient
# sqlacodegen mysql://root:root@localhost/bot_data  > models.py
# ubuntu 需要安装依赖  apt-get install python3.11-dev libmysqlclient-dev

Base = declarative_base()


engine = create_engine(get_config.get_engine_str(),pool_pre_ping=True)
DBSession = sessionmaker(bind=engine)
seesion = DBSession()
class BanUserLogo(Base):
    __tablename__ = 'ban_user_logo'

    uid = Column(BigInteger, primary_key=True)
    usr_name = Column(VARCHAR(30))
    word = Column(MEDIUMTEXT)
    ban_word = Column(VARCHAR(30))


class BanWord(Base):
    __tablename__ = 'ban_word'

    id = Column(Integer, primary_key=True)
    word = Column(VARCHAR(10), nullable=False)


class CreateThemeLogo(Base):
    __tablename__ = 'create_theme_logo'

    uid = Column(BigInteger, primary_key=True)
    color_1 = Column(VARCHAR(20))
    color_2 = Column(VARCHAR(20))
    color_3 = Column(VARCHAR(20))
    pic_path = Column(VARCHAR(100))
    callback_id = Column(BigInteger)
    flag = Column(TINYINT, server_default=text("'0'"))


class GroupInfo(Base):
    __tablename__ = 'group_info'

    uid = Column(BigInteger, primary_key=True, comment='群聊id')
    group_name = Column(VARCHAR(255), comment='群名')
    can_delete = Column(TINYINT, comment='机器人在此群里是否能删除消息')
    can_restrict = Column(TINYINT, comment='机器人在此群里是否能限制用户')
    link = Column(VARCHAR(255), comment='群组链接')


class ThemeUploadRecord(Base):
    __tablename__ = 'theme_upload_record'

    id = Column(INTEGER(10), primary_key=True)
    t_preview_name = Column(VARCHAR(255), nullable=False, unique=True, comment='主题名称')
    type = Column(ENUM('android', 'tdesktop', 'ios'), server_default=text("'tdesktop'"), comment='桌面 安卓 ios 三种')
    strc = Column(TINYINT(3), nullable=False, server_default=text("'000'"), comment='是文件名还是文件')


class User(Base):
    __tablename__ = 'user'

    uid = Column(BigInteger, primary_key=True, comment='用户id')
    full_name = Column(VARCHAR(255))
    link = Column(VARCHAR(255))
    language_code = Column(VARCHAR(255))


class UserUseRecord(Base):
    __tablename__ = 'user_use_record'

    uid = Column(BigInteger, primary_key=True, nullable=False)
    date = Column(Date, primary_key=True, nullable=False, comment='日期')
    count_record = Column(Integer, comment='使用次数')

def init_session():
    return seesion  # 返回seesion实例

def reflush():
    global  seesion
    seesion = DBSession()
