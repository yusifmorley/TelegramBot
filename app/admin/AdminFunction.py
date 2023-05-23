# 管理功能
from telegram import ChatPermissions


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


def writebanword(banwordobject, str):  #
    banwordobject.insert(str)


def blockperson(update, context):
    context.bot.delete_message(message_id=update.effective_message.message_id, chat_id=update.effective_chat.id)
    context.bot.restrict_chat_member(chat_id=update.effective_chat.id,
                                     user_id=update.effective_user.id,
                                     permissions=ChatPermissions(can_send_messages=False,
                                                                 can_send_media_messages=False))
