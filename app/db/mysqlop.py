import mysql
import yaml

from app.admin import ban_word
from app.decorate.mysql_dr import mysql_w

@mysql_w
def initdb(mydb):
    mycursor = mydb.cursor()
    mycursor.execute("show tables;")
    if len(mycursor.fetchall()) < 3:
        #创建 主题创建信息表
        mycursor.execute(
            """create table if not exists  create_theme_logo( 
                    uid bigint not null, 
                    color_1 varchar(20) ,
                    color_2 varchar(20) ,
                    color_3 varchar(20) ,
                    pic_path varchar(100) not null,
                    callback_id bigint,
                    primary key(uid)
                  )default charset =utf8
            """
        )
        # 封禁用户记录表
    mycursor.execute("""
            create table if not exists ban_user_logo(
               uid bigint not null,
               usr_name varchar(30) not null ,
               word text not null ,
               ban_word varchar(30) not null,
               primary key(uid)
           )default charset =utf8
           """)
    # 违禁词 记录表
    mycursor.execute("""
                 create table if not exists banword(
                 id int primary key auto_increment,
                 word varchar(10) not null)""")

    print("数据库表已创建")



