from telegram import  Update,Chat
from telegram.ext import ContextTypes
from sqlalchemy.orm.session import Session
from app.model.models import init_session, CreateThemeLogo, UserUseRecord
from sqlalchemy import BigInteger, Column, Date
from datetime import date
session:Session=init_session()
#用户使用监听(私聊)
def lisen(fun):
    def addlisen(update:Update,context:ContextTypes.context):
        fun(update,context)
        #如果是私聊
        if update.effective_chat.type==Chat.PRIVATE:
            same_primary_key = update.effective_user.id
            existing_user: UserUseRecord | None = session.get(UserUseRecord,
                                                              {"uid":same_primary_key,
                                                                "date":date.today()
                                                               })
            if existing_user:
            #存在
                existing_user.count_record=existing_user.count_record+1
            else:
                new_user=UserUseRecord(uid=same_primary_key,date=date.today(),count_record=1)
                session.add(new_user)
            session.commit()

    return addlisen

if __name__=="__main__":
    print("d")