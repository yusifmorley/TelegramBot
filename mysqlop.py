import mysql.connector

mydb = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="2863278679Gy@",
    database="hello",
)


def initdb(mydb):
    mycursor = mydb.cursor()
    mycursor.execute("show tables;")
    if mycursor.fetchone() is None:
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
        print("数据库表已创建")



def getpicpath(mydb,id):
    mycursor = mydb.cursor()
    mycursor.execute("select picpath from logodata where uid ={}".format(id))
    return mycursor.fetchone()

def getthemepath(mydb,id):
    mycursor = mydb.cursor()
    mycursor.execute("select themepath from logodata where uid ={}".format(id))
    return mycursor.fetchone()


def getflag(mydb,id):
    mycursor = mydb.cursor()
    mycursor.execute("select flag from logodata where uid ={}".format(id))
    return mycursor.fetchone()
   #
# def insertdata(mydb, id):  #创建 id c
#     mycursor = mydb.cursor()
#     mycursor.execute("insert into  logodata ( uid  )values({})".format(id))
#     mydb.commit()
#     print(mycursor.rowcount)

def updathemeadata(mydb,themepath,id):
    mycursor = mydb.cursor()
    mycursor.execute("update  logodata set themepath='{}' where uid={} ".format(themepath,id))
    # print(mycursor.rowcount)
    mydb.commit()


def updatpicdata(mydb,picpath,id):
    mycursor = mydb.cursor()
    mycursor.execute("update  logodata set picpath='{}' where uid={} ".format(picpath,id))
    # print(mycursor.rowcount)
    mydb.commit()

def deletelog(mydb,id):
    mycursor = mydb.cursor()
    mycursor.execute("delete from logodata where uid={}".format(id))
    # print(mycursor.rowcount)
    mydb.commit()


def createMysql(mydb, id,flag): #不管有没有 都 重置
    mycursor = mydb.cursor()
    mycursor.execute("replace into  logodata ( uid,flag )values({},{})".format(id, flag))
    mydb.commit()
    # print(mycursor.rowcount)


# createMysql(mydb,15662341558,2)
#
# #insertdata(mydb, 15424875849)
# updathemeadata(mydb,"errejidjocjvjfigobkopcf",15662341558)
#
# #createMysql(mydb,1542485849,1)
#
# deletelog(mydb,154248754)
initdb(mydb)
