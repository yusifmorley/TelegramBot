class BanWord:
    def __init__(self,mydb):
        self.mydb=mydb
        self.mycursor = mydb.cursor()

    def insert(self,text):
        self.mycursor.execute("insert into ban_word(word) values ('{}')".format(text))
        self.mydb.commit()

    def select(self):
        self.mycursor.execute("select word from ban_word ")
        return  self.mycursor.fetchall()

