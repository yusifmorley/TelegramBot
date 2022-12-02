from telegram import ChatPermissions
from telegram.ext import Updater, CallbackContext, CallbackQueryHandler
import logging
from adminfunction import deletetxt, getbanword
from getbackground import getbackground
from mysqlop import createMysql
from telegram.ext import MessageHandler, Filters
from telegram.ext import CommandHandler
from combinate import combinate
import mysql.connector
import mysqlop
import getConfig
import getRadomTheme
import time
#主文件

myapi = getConfig.getTelegramId() # 机器人api
updater = Updater(token=myapi, use_context=True)
dispatcher = updater.dispatcher
banword = getbanword()
logging.basicConfig(filename="Log/mylog", format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)  # 日志
mydb = getConfig.getMysqlConfig()
messids={}  #存储所有用户和bot 的massage_id  不包括抽取的图片 合成的主题 和随机返回的主题

#合并主题和背景
def combinThemeAndPic(update, context):
    createMysql(mydb, update.effective_chat.id, 1)
    recordSend(update, context, "请发送您的主题和背景!")


#获取主题背景
def getThemeBackgrounds(update, context):
    createMysql(mydb, update.effective_chat.id, 2)
    recordSend(update, context, "请发送您的主题！")


#下载主题
def downloadtheme(update, context):
    flag = mysqlop.getflag(mydb, update.effective_chat.id)[0]
    if flag is not None:  # 如果数据库里有 请求记录 则下载主题 否则pass
        file = context.bot.getFile(update.message.document.file_id)
        file.download("temptheme/" + update.message.document.file_name)
        print("____________")
        recordSend(update, context, "我已收到主题文件啦！")
        print("+++++++++++++")
        themeFileDowmloaded = "temptheme/" + update.message.document.file_name
        if flag == 1:
            mysqlop.updathemeadata(mydb, themeFileDowmloaded, update.effective_chat.id)
            pic = mysqlop.getpicpath(mydb, update.effective_chat.id)[0]
            if pic is not None:
                newthemepath = combinate(themeFileDowmloaded, pic)
                context.bot.send_document(chat_id=update.effective_chat.id, document=open(newthemepath, "rb"))
                recordSend(update, context, "成功！，这是合成的新主题～")
                delete(update, context)
                mysqlop.deletelog(mydb, update.effective_chat.id)  # 删除 记录
            else:
                recordSend(update, context, "请发送图片")
        else:
            try:
                picpath = getbackground(themeFileDowmloaded)
            except:
                recordSend(update, context, "出错了，此主题文件不包含背景！")
            context.bot.send_document(chat_id=update.effective_chat.id, document=open(picpath, "rb"))
            recordSend(update, context, "这是您的背景图片～")
            delete(update, context)
            mysqlop.deletelog(mydb, update.effective_chat.id)  # 删除 记录

#获取图片
def handlePhoto(update, context):
    flag = mysqlop.getflag(mydb, update.effective_chat.id)[0]
    if flag is not None:
        if flag == 1:
            tim = time.localtime()
            timstr = time.strftime("%Y-%m-%d-%H-%M-%S", tim)
            recordSend(update, context, "这确实是一张图片！")
            print(100000000)
            print(update)
            file = context.bot.getFile(update.message.photo[2]['file_id'])
            photoPath = "tempthemephoto/" + timstr + ".jpg"
            file.download(photoPath)
            recordSend(update, context, "图片已下载")

            mysqlop.updatpicdata(mydb, photoPath, update.effective_chat.id)
            themepath = mysqlop.getthemepath(mydb, update.effective_chat.id)[0]
            if themepath is not None:
                newthemepath = combinate(themepath, photoPath)
                context.bot.send_document(chat_id=update.effective_chat.id, document=open(newthemepath, "rb"))
                recordSend(update, context, "成功！，这是合成的新主题～")
                delete(update, context)
                mysqlop.deletelog(mydb, update.effective_chat.id)  # 删除 记录
            else:
                recordSend(update, context, "请发送主题！")
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
                                         text="权限不够 无法执行呦～")
# def deletaBotMessage(update, context):
#      print(update.message.from_user.id)
#      mess=update.message.reply_text("Please delete")
#      time.sleep(2)
#      context.bot.delete_message(message_id=mess.message_id,chat_id=update.effective_chat.id)

def recordSend(update, context, txt):
    id=update.message.from_user.id
    mes= context.bot.send_message(chat_id=update.effective_chat.id,
                                         text=txt)
    if id in messids.keys():
        messids[id].append(mes)
    else:
        messids[id]=[]
        messids[id].append(mes)


def delete(update,context):
    id = update.message.from_user.id
    mes=messids[id]
    for x in mes:
        context.bot.delete_message(message_id=x.message_id, chat_id=update.effective_chat.id)
def getRanTheme(update, context):
    path=getRadomTheme.getRandomTheme()
    context.bot.send_document(chat_id=update.effective_chat.id, document=open("Theme/"+path, "rb"))
    recordSend(update, context, "这是您的主题文件，亲～")

if __name__=="__main__":
        mysqlop.initdb(mydb) #初始化 数据库
        try:
            combinss = CommandHandler('combinthemeandphoto', combinThemeAndPic)
            dispatcher.add_handler(combinss)

            combinsss = CommandHandler('getbackground', getThemeBackgrounds)
            dispatcher.add_handler(combinsss)

            combinssss = CommandHandler('getrandomtheme',getRanTheme)
            dispatcher.add_handler(combinssss)

            # combinssss = CommandHandler('delete', deletaBotMessage)
            # dispatcher.add_handler(combinssss)

            checkatthem = MessageHandler(Filters.document.file_extension("attheme"), downloadtheme)
            dispatcher.add_handler(checkatthem)

            unknown_handler = MessageHandler(Filters.photo, handlePhoto)
            dispatcher.add_handler(unknown_handler)

            adminhander = MessageHandler(Filters.text, adminhanderex)
            dispatcher.add_handler(adminhander)

            updater.start_polling()
        except mysql.connector.errors.OperationalError: #连接断开 重新链接
             mydb = getConfig.getMysqlConfig()
