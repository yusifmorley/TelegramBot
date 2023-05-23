from app import getConfig
from app.admin import BanWord


# 初始化数据库

#获取配置

def initdb(mydb):
    mycursor = mydb.cursor()
    mycursor.execute("show tables;")
    if len(mycursor.fetchall()) < 3:
        mycursor.execute(
            """create table logodata(
                    uid bigint not null,
                    flag  int default 0,
                    themepath varchar(100),
                    picpath varchar(100),
                    primary key(uid)
                  )default charset =utf8
            """
        )
        mycursor.execute("""
         create table bans(
            uid bigint not null,
            flag int default 0,
            banword varchar(30) not null,
            primary key(uid)
        )default charset =utf8
        """)
        mycursor.execute("""
        
                 create table banword(
                 id int primary key auto_increment,
                 word varchar(10) not null)""")

        mydb.commit()
    print("数据库表已创建")


def getpicpath(mydb, id):
    mycursor = mydb.cursor()
    mycursor.execute("select picpath from logodata where uid ={}".format(id))
    return mycursor.fetchone()


def getthemepath(mydb, id):
    mycursor = mydb.cursor()
    mycursor.execute("select themepath from logodata where uid ={}".format(id))
    return mycursor.fetchone()


def getflag(mydb, id):
    mycursor = mydb.cursor()
    mycursor.execute("select flag from logodata where uid ={}".format(id))
    return mycursor.fetchone()

def updathemeadata(mydb, themepath, id):
    mycursor = mydb.cursor()
    mycursor.execute("update  logodata set themepath='{}' where uid={} ".format(themepath, id))
    # print(mycursor.rowcount)
    mydb.commit()


def updatpicdata(mydb, picpath, id):
    mycursor = mydb.cursor()
    mycursor.execute("update  logodata set picpath='{}' where uid={} ".format(picpath, id))
    # print(mycursor.rowcount)
    mydb.commit()


def deletelog(mydb, id):
    mycursor = mydb.cursor()
    mycursor.execute("delete from logodata where uid={}".format(id))
    # print(mycursor.rowcount)
    mydb.commit()


def createMysql(mydb, id, flag):  # 不管有没有 都 重置
    mycursor = mydb.cursor()
    mycursor.execute("replace into  logodata ( uid,flag )values({},{})".format(id, flag))
    mydb.commit()
    # print(mycursor.rowcount)


def getbannum(mydb, id):
    mycursor = mydb.cursor()
    mycursor.execute("select flag from bans where uid={}".format(id))
    num = mycursor.fetchone()
    if num is not None:
        return num[0]
    else:
        return 0


def upbanuser(mydb, id, banword):
    mycursor = mydb.cursor()
    mycursor.execute("update bans set flag=flag+1 , banword=concat(banword,'-{}') where uid={}".format(banword, id))
    mydb.commit()


def creatbanuser(mydb, id, banword):
    mycursor = mydb.cursor()
    mycursor.execute("insert into bans (uid, banword) values({},'{}')".format(id, banword))
    mydb.commit()


def getbanwords(mydb, id):
    mycursor = mydb.cursor()
    mycursor.execute("select banword from bans where uid={}".format(id))
    return mycursor.fetchone()[0]


def deleteban(mydb, id):
    mycursor = mydb.cursor()
    mycursor.execute("delete from bans where uid={}".format(id))
    mydb.commit()


def getBanWordObject(mydb):
    return BanWord.banword(mydb)

# if __name__=="__main__":
#     mydb = getConfig.getMysqlConfig()
#     initdb(mydb)
#     # mycursor = mydb.cursor()
#     # mycursor.execute("show tables;")
#     # print(mycursor.fetchall())
#     ban= BanWord.banword(mydb)
#     print(ban.select())

