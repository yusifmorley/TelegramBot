# 管理功能
from telegram import ChatPermissions
from app.model.models import init_session,BanUserLogo
from telegram import Update
def deletetxt(txt, str):
    for x in txt:
        if x in str:
            return x
    return None


def getbanword(banwordobject):  # 获取
    lis = []
    words = banwordobject.select()
    for x in words:
        lis.append(x[0])
    return lis


def writeBanWord(banwordObject, str):
    banwordObject.insert(str)


def blockperson(update:Update, context,ban_word):
    session=init_session()
    existing_user: BanUserLogo | None = session.get(BanUserLogo, update.effective_user.id)
    if not existing_user:
         session.add(BanUserLogo(uid=update.effective_user.id,
                            usr_name=update.effective_user.name,
                            word=update.message.text,
                            ban_word=ban_word
                            ))
    session.commit()
    context.bot.delete_message(message_id=update.effective_message.message_id, chat_id=update.effective_chat.id)
    context.bot.restrict_chat_member(chat_id=update.effective_chat.id,
                                     user_id=update.effective_user.id,
                                     permissions=ChatPermissions(can_send_messages=False,
                                                                 can_send_media_messages=False))
