from telegram.ext import CallbackContext

from app.admin import admin_function
from telegram import Update, Chat

from app.admin.admin_function import bot_delete_permission, bot_restrict_permission


class MonitorPerson:
    def __init__(self, monitor_person_num):  # monitor_person为监听人个数
        self.monitor_person = monitor_person_num
        self.text_list = []

    def __contain_list__(self,text):
        if len(self.text_list)>self.monitor_person:
            del  self.text_list[0]  #删除首个元素
        self.text_list.append(text)

    def run(self, usr_id, user_name, text, update:Update, context: CallbackContext,banword,logger):
        #如果是组 或者超级组
        if update.effective_message.chat.type ==Chat.GROUP or  update.effective_message.chat.type ==Chat.SUPERGROUP :
        # 是否有权限删除
            if bot_delete_permission(update, context) == 0:
                return

            if bot_restrict_permission(update, context) == 0:
                return

        #排除来自频道的消息
        if hasattr(update,"message") and hasattr(update.message,"chat"):
            if update.message.chat.type==Chat.CHANNEL:
                return

        #对@进行特殊处理
        if '@' in text and "/" not in text:
            admin_function.block_person(update, context, "@")

        #对 t.me 链接特殊处理
        if  't.me' in text:
            if update.effective_chat.username in text:
                return


        #防止误删来自频道的消息
        if  "addtheme" in text:
            return

        #判断是否触违禁词
        os = admin_function.delete_txt(banword, text)
        if os:  # 若存在违禁词
            admin_function.block_person(update, context, os)
            logger.info(os)  # 记录
            return

        #判断text 是否有重复
        if text in self.text_list:
            admin_function.block_person(update, context, "重复")
        else:
            self.__contain_list__(text)
