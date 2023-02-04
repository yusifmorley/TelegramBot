import mysql.connector
import yaml
# 初始化数据库

#获取配置

def initdb(mydb):
    mycursor = mydb.cursor()
    mycursor.execute("show tables;")
    if len(mycursor.fetchall()) < 2:
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
        """
                         )
        mydb.commit()
    print("数据库表logodata和bans已创建")


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


#
# def insertdata(mydb, id):  #创建 id c
#     mycursor = mydb.cursor()
#     mycursor.execute("insert into  logodata ( uid  )values({})".format(id))
#     mydb.commit()
#     print(mycursor.rowcount)

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
# createMysql(mydb,15662341558,2)
#
# #insertdata(mydb, 15424875849)
# updathemeadata(mydb,"errejidjocjvjfigobkopcf",15662341558)
#
# #createMysql(mydb,1542485849,1)
#
# deletelog(mydb,154248754)
# mycursor = mydb.cursor()
# mycursor.execute("show tables;")
# print(len(mycursor.fetchall()))
#
# initdb(mydb)
# creatbanuser(mydb,565454545,"@")
