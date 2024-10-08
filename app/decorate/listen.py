import telegram
from telegram import Update, Chat, User
from telegram.ext import ContextTypes
import app
from app.logger.t_log import get_logging
from app.model.models import  UserUseRecord, BanUserLogo, GroupInfo, getSession
from datetime import date

logger = get_logging().getLogger(__name__)

# 用户使用监听
# 如果被封禁了就不可使用机器人
def listen(fun):
    async def add_listen(update: Update, context: ContextTypes.DEFAULT_TYPE):
        with getSession() as session:
            # 检测用户是否关注了频道
            # 必须把机器人引入频道 赋予管理权限
            # try:
            #     await context.bot.getChatMember('@moleydimu', update.effective_user.id)
            # except TelegramError as te:
            #     # 如果发生错误 说明用户未加入群组
            #     pass
            # 向数据库查询用户
            existing_user: BanUserLogo | None = session.get(BanUserLogo, update.effective_chat.id)
            # 如果用户被封禁
            if existing_user:
                logger.warning("非法私聊用户,禁止使用机器人 update为: {}".format(update))
                context.bot.send_message(chat_id=update.effective_chat.id, text="您使用次数过多,请访问网站查看更多主题 https://yusifmorley.com/theme")
                return

            # 执行函数
            await fun(update, context)

            # TODO 此处需要重构
            # 记录群组使用
            if update.effective_chat.type == Chat.GROUP or update.effective_chat.type == Chat.SUPERGROUP:
                my_chat: Chat = update.effective_chat
                existing_group_log: GroupInfo | None = session.get(app.model.models.GroupInfo,
                                                                   my_chat.id)
                admins = await update.effective_chat.get_administrators()
                for x in admins:
                    v: telegram.ChatMemberAdministrator = x
                    if x.__eq__(context.bot.getChatMember) and hasattr(v,"can_restrict_members")and hasattr(v,"can_delete_messages"):
                        can_restr = 1 if v.can_restrict_members else 0
                        can_de = 1 if v.can_delete_messages else 0
                        if not existing_group_log:
                            new_group = GroupInfo(uid=my_chat.id, link=my_chat.link, group_name=my_chat.effective_name, can_delete=can_de,
                                                  can_restrict=can_restr)
                            session.add(new_group)
                        else:  # 存在则对比数据库里的数据 看是否更
                            if existing_group_log.link != my_chat.id or existing_group_log.group_name != my_chat.effective_name:
                                existing_group_log.link = my_chat.id
                                existing_group_log.group_name = my_chat.effective_name
                            if existing_group_log.can_delete != can_de or existing_group_log.can_restrict != can_restr:
                                existing_group_log.can_delete = can_de
                                existing_group_log.can_restrict = can_restr
                        break
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

            # 记录用户使用
            same_primary_key = update.effective_user.id
            existing_user: UserUseRecord | None = session.get(UserUseRecord,
                                                              {"uid": same_primary_key,
                                                               "date": date.today()
                                                               })
            if existing_user:
                # 如果存在
                # 封禁恶意用户
                # 封禁
                if existing_user.count_record > 80:
                    new_ban_user = BanUserLogo(uid=same_primary_key)
                    session.add(new_ban_user)
                existing_user.count_record = existing_user.count_record + 1
            else:
                new_user = UserUseRecord(uid=same_primary_key, date=date.today(), count_record=1)
                session.add(new_user)

            session.commit()

    return add_listen
