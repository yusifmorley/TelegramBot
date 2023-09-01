class banword:
    def __init__(self,mydb):
        self.mydb=mydb
        self.mycursor = mydb.cursor()

    def insert(self,text):
        self.mycursor.execute("insert into banword(word) values ('{}')".format(text))
        self.mydb.commit()

    def select(self):
        self.mycursor.execute("select word from banword ")
        return  self.mycursor.fetchall()

