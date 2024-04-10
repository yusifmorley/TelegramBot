from telegram.constants import ChatType
from telegram.ext import CallbackContext

from app.admin import admin_function
from telegram import Update, Chat, MessageOrigin
from app.config.get_config import get_myid
from app.admin.admin_function import bot_delete_permission, bot_restrict_permission
from app.logger.t_log import get_logging

log = get_logging().getLogger(__name__)


class MonitorPerson:

    async def run(self, usr_id, user_name, text, update: Update, context: CallbackContext, banword, logger):
        # 排除 管理员 的 消息 和私聊消息
        if usr_id == get_myid() and update.effective_message.chat.type == Chat.PRIVATE:
            return False

        # 如果是我的群组
        if update.effective_message.chat.id == -1001313322278:
            # 判断是否触违禁词
            os = admin_function.delete_txt(banword, text)
            if os:  # 若存在违禁词
                if await admin_function.block_person(update, context, os):
                    logger.info("用户{},id{},触发违禁词{}被封禁".format(user_name, str(usr_id), text))  # 记录
                    return True
                else:
                    logger.warn("无权限 用户{},id{},触发违禁词{}".format(user_name, str(usr_id), text))
                    return False
        # 对@进行特殊处理
        # if '@' in text and "/" not in text:
        #     await admin_function.block_person(update, context, "@")
        #     return True

        # 对 t.me 链接特殊处理
        # if 't.me' in text:
        #     if update.effective_chat.username in text:
        #         return False

        # 判断text 是否有重复
        # if text in self.text_list:
        #     admin_function.block_person(update, context, "重复")
        #     return True
        # else:
        #     self.__contain_list__(text)
        #     return False
