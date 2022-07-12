def deletetxt(txt,str):
    for x in str:
       if x in txt:
           return True
    return False



def getbanword():
    with open("banconfig/banword", "r") as fp:
         return fp.read().split("\n")




def writebanword(str):
    with open("banconfig/banword", "a") as fp:
        fp.write(str)

