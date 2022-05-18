import mysql.connector


# create table Androidtheme ( PRIMARY KEY ('id') NOT NULL,themeName char(80),preview char(100),background char(100),file char(100));
def createMysql(dic):
  try:
    mydb = mysql.connector.connect(
        host="127.0.0.1",
        user="morleybread",
        password="2863278679Gy@",
        database="Themedata",
    )

    # mycursor=mydb.cursor()
    # mycursor.execute("insert into mytheme(type,name,preview ,link) values('ios','@bluesky','/preview/mylogo','t.me/hdsfghvgjkdr'); ")
    # mydb.commit()

    mycursor = mydb.cursor()
    mycursor.execute(
        "insert ignore into  Androidtheme (themeName,preview,background,file) values('" + dic["themeName"] + "','" + dic["preview"] +"','"+ dic["background"] +"','"+ dic["file"] + "');"
    )
    mydb.commit()
  except:
      pass

# dic={'themeName': '01 Haikyuu', 'preview': 'temptheme/01 Haikyuu(@JoinThemesWorld).attheme','background':'background/Stellar.jpg','file':'temptheme/DottorAirola.Flattt.attheme'}
# createMysql(dic)
#
# for x in mycursor:
#     print(x)
# print(mydb)

# dic=pareslink(a)
# createMysql(dic)

#
# def show(dic):
#     print( "insert into channellist(themeName,channel,link,preview) values('"+dic["themeName"]+"','"+dic["channel"]+"','"+dic["link"]+"','"+dic["preview"]+"');")
#
#
# a = "https://t.me/addtheme/LightBurbujaByROzZzMi"
# b=pareslink(a)
# b["preview"]="hello"
