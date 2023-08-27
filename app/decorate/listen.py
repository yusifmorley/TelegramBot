from telegram import  Update,Chat
from telegram.ext import ContextTypes


#监听
def lisen(fun):
    def addlisen(update:Update,context:ContextTypes.context):
        fun(update,context)
        #组或者超级组
        if update.effective_chat.type==Chat.GROUP or update.effective_chat.type==Chat.SUPERGROUP:
            print()


    return addlisen