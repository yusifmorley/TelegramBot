#create_theme_logo 表的操作
import mysql

from app.db.mysqlop import initdb




if __name__=="__main__":
    mydb = mysql.connector.connect(
        host='127.0.0.1',
        user='root',
        password='root',
        database="telegramdata",
    )
    initdb(mydb)
    mycursor = mydb.cursor()

    mycursor.execute("show tables;")
    print(mycursor.fetchone())
#     ban= BanWord.banword(mydb)
#     print(ban.select())
