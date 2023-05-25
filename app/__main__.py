
import telegram
from telegram.ext import Updater
import logging
from telegram.ext import MessageHandler, Filters
from telegram.ext import CommandHandler
import mysql.connector
from app.admin.person import MonitorPerson
from app.config import get_config
from app.db import mysqlop
from app.theme import get_radom_theme
from app.admin import admin_function

myapi = get_config.getTelegramId()  # 机器人api
updater = Updater(token=myapi, use_context=True)
commands = [
    telegram.BotCommand('getrandomtheme', '随机获取一个主题')
]
updater.bot.set_my_commands(commands)
dispatcher = updater.dispatcher
logging.basicConfig(filename="log/mylog", format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)  # 日志
logger = logging.getLogger(__name__)
mydb = get_config.getMysqlConfig()

mysqlop.initdb(mydb)
BanWordObject = mysqlop.getBanWordObject(mydb)
banword = admin_function.getbanword(BanWordObject)

mon_per=MonitorPerson(10) #监控10个人
# 合并主题和背景
def on_join(update, context):
    # print(update.effective_chat)
    context.bot.delete_message(chat_id=update.effective_chat.id, message_id=update.effective_message.message_id)


def admin_handle(update, context):  # 管理员

    text = update.effective_message.text
    user = update.effective_message.from_user
    mon_per.run(user.id, user.first_name + " " + user.first_name, text, update, context,banword,logger)


def get_ran_theme(update, context):
    context.bot.delete_message(message_id=update.effective_message.message_id, chat_id=update.effective_chat.id)
    path = get_radom_theme.get_random_theme()
    if not isinstance(path,str):
        context.bot.send_document(chat_id=update.effective_chat.id, document=open("Theme/" + path, "rb"))
    else:
        context.bot.send_document(chat_id=update.effective_chat.id, text=path.rstrip("\n"))

    context.bot.send_message(chat_id=update.effective_chat.id, text="这是您的主题文件，亲～")


def write_ban_word(update, context):
    if update.message.from_user.id != 507467074:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="您不是管理员！\n" +
                                      "您可以输入以下命令：\n" +
                                      "/getrandomtheme - 随机获取一个主题"
                                 )
        return
    global banword
    admin_function.writebanword(BanWordObject, context.args[0])
    banword = admin_function.getbanword(BanWordObject)
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="成功添加新的违禁词：" + context.args[0])
    context.bot.delete_message(message_id=update.effective_message.message_id, chat_id=update.effective_chat.id)


def error_hander(update, context):
    logger.error("这是update {} 出错了", str(update))


if __name__ == "__main__":

    try:
        combinssss = CommandHandler('getrandomtheme', get_ran_theme)
        dispatcher.add_handler(combinssss)

        dispatcher.add_handler(CommandHandler('report', write_ban_word))

        adminhander = MessageHandler(Filters.text, admin_handle)
        dispatcher.add_handler(adminhander)
        dispatcher.add_handler(MessageHandler(Filters.status_update.new_chat_members, on_join))

        dispatcher.add_error_handler(error_hander)
        updater.start_polling()
    except mysql.connector.errors.OperationalError:  # 连接断开 重新链接
        mydb = get_config.getMysqlConfig()
