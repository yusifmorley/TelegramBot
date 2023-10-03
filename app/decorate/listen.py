from telegram import Update, Chat, User
from telegram.ext import ContextTypes, DispatcherHandlerStop
from sqlalchemy.orm.session import Session

import app
from app.admin.admin_function import bot_delete_permission, bot_restrict_permission
from app.model.models import init_session, CreateThemeLogo, UserUseRecord, BanUserLogo, GroupInfo
from sqlalchemy import BigInteger, Column, Date
from datetime import date
session:Session=init_session()
#用户使用监听
def lisen(fun):
    def addlisen(update:Update,context:ContextTypes.context):

        existing_user: BanUserLogo | None = session.get(BanUserLogo, update.effective_user.id)
        # 如果用户被封禁
        if existing_user:
            return
            # logger.warning("非法私聊用户,禁止使用机器人: {}".format(update))
            # raise DispatcherHandlerStop()

        #执行函数
        fun(update,context)

        #记录群组使用
        if update.effective_chat.type==Chat.GROUP or update.effective_chat.type==Chat.SUPERGROUP:
            my_chat:Chat=update.effective_chat
            existing_group_log: GroupInfo | None = session.get(app.model.models.GroupInfo,
                                                                          my_chat.id)
            can_de = bot_delete_permission(update, context)
            can_restr = bot_restrict_permission(update, context)
            if not existing_group_log:
                new_group=GroupInfo(uid=my_chat.id,link=my_chat.link,group_name=my_chat.username,can_delete=can_de,can_restrict=can_restr)
                session.add(new_group)
            else: #存在则对比数据库里的数据 看是否更
                if existing_group_log.link!=my_chat.id or existing_group_log.group_name!=my_chat.username:
                    existing_group_log.link=my_chat.id
                    existing_group_log.group_name=my_chat.username
                if  existing_group_log.can_delete!=can_de or existing_group_log.can_restrict!=can_restr:
                    existing_group_log.can_delete=can_de
                    existing_group_log.can_restrict=can_restr
        # 记录用户
        user: User = update.effective_user
        existing_user_log: app.model.models.User | None = session.get(app.model.models.User, update.effective_user.id)
        # 如果不存在
        if not existing_user_log:
            new_user = app.model.models.User(uid=user.id, full_name=user.full_name, link=user.link,
                                             language_code=user.language_code)
            session.add(new_user)

        # 如果和数据里不一样
        else:
            if user.full_name != existing_user_log.full_name:
                existing_user_log.full_name = user.full_name

            if user.link != existing_user_log.link:
                existing_user_log.link = user.link


        #记录用户使用
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