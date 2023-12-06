from mysql.connector.abstracts import MySQLConnectionAbstract


def mysql_w(fun):
    def add_commit(mydb: MySQLConnectionAbstract, *args):
        fun(mydb, *args)
        mydb.commit()
        # 组或者超级组

    return add_commit
