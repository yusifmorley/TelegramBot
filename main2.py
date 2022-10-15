from telegram import ChatPermissions
from telegram.ext import Updater, CallbackContext, CallbackQueryHandler
import logging

from adminfunction import deletetxt, getbanword
from getbackground import getbackground
from mysqlop import createMysql
from telegram.ext import MessageHandler, Filters
from telegram.ext import CommandHandler
from combinate import combinate
import time
import mysql.connector
import mysqlop


myapi = ""  # 机器人api
updater = Updater(token=myapi, use_context=True)
dispatcher = updater.dispatcher
banword = getbanword()
logging.basicConfig(filename="Log/mylog", format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)  # 日志
mydb = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="2863278679Gy@",
    database="telegramdata",
)


def combinThemeAndPic(update, context):
    createMysql(mydb, update.effective_chat.id, 1)
    context.bot.send_message(chat_id=update.effective_chat.id, text="请发送您的主题和背景！")


def getThemeBackgrounds(update, context):
    createMysql(mydb, update.effective_chat.id, 2)
    context.bot.send_message(chat_id=update.effective_chat.id, text="请发送您的主题！")


def downloadtheme(update, context):
    flag = mysqlop.getflag(mydb, update.effective_chat.id)[0]
    if flag is not None:  # 如果数据库里有 请求记录 则下载主题 否则pass
        file = context.bot.getFile(update.message.document.file_id)
        file.download("temptheme/" + update.message.document.file_name)
        context.bot.send_message(chat_id=update.effective_chat.id, text="我已收到主题文件")
        themeFileDowmloaded = "temptheme/" + update.message.document.file_name
        if flag == 1:
            mysqlop.updathemeadata(mydb, themeFileDowmloaded, update.effective_chat.id)
            pic = mysqlop.getpicpath(mydb, update.effective_chat.id)[0]
            if pic is not None:
                newthemepath = combinate(themeFileDowmloaded, pic)
                context.bot.send_document(chat_id=update.effective_chat.id, document=open(newthemepath, "rb"))
                context.bot.send_message(chat_id=update.effective_chat.id, text="成功！，这是合成的新主题")
                mysqlop.deletelog(mydb, update.effective_chat.id)  # 删除 记录
            else:
                context.bot.send_message(chat_id=update.effective_chat.id, text="请发送图片")
        else:
            try:
                picpath = getbackground(themeFileDowmloaded)
            except:
                context.bot.send_message(chat_id=update.effective_chat.id, text="出错，此主题文件不包含背景！")
            context.bot.send_document(chat_id=update.effective_chat.id, document=open(picpath, "rb"))
            context.bot.send_message(chat_id=update.effective_chat.id, text="这是您的背景图片")
            mysqlop.deletelog(mydb, update.effective_chat.id)  # 删除 记录


def handlePhoto(update, context):
    flag = mysqlop.getflag(mydb, update.effective_chat.id)[0]
    if flag is not None:
        if flag == 1:
            tim = time.localtime()
            timstr = time.strftime("%Y-%m-%d-%H-%M-%S", tim)
            context.bot.send_message(chat_id=update.effective_chat.id, text="这确实是一张图片！")
            file = context.bot.getFile(update.message.photo[2]['file_id'])
            photoPath = "tempthemephoto/" + timstr + ".jpg"
            file.download(photoPath)
            context.bot.send_message(chat_id=update.effective_chat.id, text="图片已下载")
            mysqlop.updatpicdata(mydb, photoPath, update.effective_chat.id)
            themepath = mysqlop.getthemepath(mydb, update.effective_chat.id)[0]
            if themepath is not None:
                newthemepath = combinate(themepath, photoPath)
                context.bot.send_document(chat_id=update.effective_chat.id, document=open(newthemepath, "rb"))
                context.bot.send_message(chat_id=update.effective_chat.id, text="成功！，这是合成的新主题")
                mysqlop.deletelog(mydb, update.effective_chat.id)  # 删除 记录
            else:
                context.bot.send_message(chat_id=update.effective_chat.id, text="请发送主题！")
        else:
            pass

def adminhanderex(update, context):  # 管理员
    text = update.effective_message.text
    os = deletetxt(banword,text)

    if os: #若存在违禁词

        context.bot.delete_message(chat_id=update.effective_chat.id, message_id=update.effective_message.message_id)

        num= mysqlop.getbannum(mydb, update.effective_user.id)

        if num==0:
            mysqlop.creatbanuser(mydb,update.effective_user.id,os)

            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text="您触发了违禁词:{}".format(os))

            mysqlop.upbanuser(mydb,update.effective_user.id,os)

        elif num<=2:
            mysqlop.upbanuser(mydb,update.effective_user.id,os)
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text="您触发了违禁词:{}".format(os))
        else:
            try:
                context.bot.restrict_chat_member(chat_id=update.effective_chat.id,
                                         user_id=update.effective_user.id,
                                         permissions=ChatPermissions(can_send_messages=False,
                                                                 can_send_media_messages=False))

                textlog = "用户id :" + str(
                    update.effective_user.id) + " 用户名 :" + update.effective_user.full_name \
                          + "已被永久封禁，由于多次触发违禁词：" + \
                          mysqlop.getbanwords(mydb, update.effective_user.id) + "-" + os
                context.bot.send_message(chat_id=update.effective_chat.id, text=textlog)
                mysqlop.deletelog(mydb, update.effective_user.id)
                logging.info(textlog)
            except:
                context.bot.send_message(chat_id=update.effective_chat.id,
                                         text="权限不够 无法执行")



mysqlop.initdb(mydb) #初始化 数据库

combinss = CommandHandler('combinthemeandphoto', combinThemeAndPic)
dispatcher.add_handler(combinss)

combinsss = CommandHandler('getbackground', getThemeBackgrounds)
dispatcher.add_handler(combinsss)

checkatthem = MessageHandler(Filters.document.file_extension("attheme"), downloadtheme)
dispatcher.add_handler(checkatthem)

unknown_handler = MessageHandler(Filters.photo, handlePhoto)
dispatcher.add_handler(unknown_handler)

adminhander = MessageHandler(Filters.text, adminhanderex)
dispatcher.add_handler(adminhander)

updater.start_polling()
