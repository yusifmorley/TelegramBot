import telegram
from telegram import ChatPermissions
from telegram.ext import Updater, CallbackContext, CallbackQueryHandler
import logging

import adminfunction
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
from adminfunction import blockperson
from PersonAdmin import MonitorPerson
myapi = getConfig.getTelegramId() # 机器人api
updater = Updater(token=myapi, use_context=True)
monitor_person=MonitorPerson(5)
commands = [
        telegram.BotCommand('combinthemeandphoto','合并主题和背景'),
        telegram.BotCommand('getbackground','抽取主题的背景'),
        telegram.BotCommand('getrandomtheme', '随机获取一个主题')
    ]
updater.bot.set_my_commands(commands)
dispatcher = updater.dispatcher
logging.basicConfig(filename="Log/mylog", format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)  # 日志
logger=logging.getLogger(__name__)
mydb = getConfig.getMysqlConfig()
BanWordObject=mysqlop.getBanWordObject(mydb)
banword = getbanword(BanWordObject)
messids={}  #存储所有用户和bot 的massage_id  不包括抽取的图片 合成的主题 和随机返回的主题

#合并主题和背景
def combinThemeAndPic(update, context):
    context.bot.delete_message(message_id=update.effective_message.message_id, chat_id=update.effective_chat.id)
    createMysql(mydb, update.effective_chat.id, 1)
    recordSend(update, context, "请发送您的主题和背景!")

#获取主题背景
def getThemeBackgrounds(update, context):
    context.bot.delete_message(message_id=update.effective_message.message_id, chat_id=update.effective_chat.id)
    createMysql(mydb, update.effective_chat.id, 2)
    recordSend(update, context, "请发送您的主题！")

#下载主题
def downloadtheme(update, context):
    flag = mysqlop.getflag(mydb, update.effective_chat.id)[0]
    if flag is not None:  # 如果数据库里有 请求记录 则下载主题 否则pass
        file = context.bot.getFile(update.message.document.file_id)
        file.download("temptheme/" + update.message.document.file_name)
        recordSend(update, context, "我已收到主题文件啦！")
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

def onjoin(update,context):
    #print(update.effective_chat)
    context.bot.delete_message(chat_id=update.effective_chat.id, message_id=update.effective_message.message_id)

def adminhanderex(update, context):  # 管理员

    text = update.effective_message.text
    user=update.effective_message.from_user
    monitor_person.run(user.id,user.first_name+" "+user.first_name,text,update,context)
    os = deletetxt(banword,text)
    if os: #若存在违禁词
        blockperson(update, context) #封禁
        logger.info(os) #记录

def recordSend(update, context, txt):
    global tempcontext
    tempcontext=context
    newmid=update.effective_message.message_id
    id=update.message.from_user.id
    mes= context.bot.send_message(chat_id=update.effective_chat.id,text=txt)
    if id in messids.keys():
        messids[id].append(mes)
    else:
        messids[id]=[]
        messids[id].append(mes)
    messids[id].append(newmid)


def delete(update,context):
    id = update.message.from_user.id
    mes=messids[id]
    for x in mes:
        context.bot.delete_message(message_id=x.message_id, chat_id=update.effective_chat.id)

def getRanTheme(update, context):
    context.bot.delete_message(message_id=update.effective_message.message_id, chat_id=update.effective_chat.id)
    path=getRadomTheme.getRandomTheme()
    context.bot.send_document(chat_id=update.effective_chat.id, document=open("Theme/"+path, "rb"))
    recordSend(update, context, "这是您的主题文件，亲～")

def writeBanWord(update,context):
    if  update.message.from_user.id!=507467074:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="您不是管理员！\n"+
                                      "您可以输入以下命令：\n"+
                                      "/combinthemeandphoto - 合并主题和背景\n"+
                                      "/getbackground - 抽取主题的背景\n"+
                                      "/getrandomtheme - 随机获取一个主题"
                                 )
        return
    global banword
    adminfunction.writebanword(BanWordObject,context.args[0])
    banword = getbanword(BanWordObject)
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="成功添加新的违禁词："+context.args[0])


if __name__=="__main__":
        mysqlop.initdb(mydb) #初始化 数据库
        try:
            combinss = CommandHandler('combinthemeandphoto', combinThemeAndPic)
            dispatcher.add_handler(combinss)

            combinsss = CommandHandler('getbackground', getThemeBackgrounds)
            dispatcher.add_handler(combinsss)

            combinssss = CommandHandler('getrandomtheme',getRanTheme)
            dispatcher.add_handler(combinssss)

            dispatcher.add_handler(CommandHandler('report', writeBanWord))
            # combinssss = CommandHandler('delete', deletaBotMessage)
            # dispatcher.add_handler(combinssss)

            checkatthem = MessageHandler(Filters.document.file_extension("attheme"), downloadtheme)
            dispatcher.add_handler(checkatthem)

            unknown_handler = MessageHandler(Filters.photo, handlePhoto)
            dispatcher.add_handler(unknown_handler)

            adminhander = MessageHandler(Filters.text, adminhanderex)
            dispatcher.add_handler(adminhander)
            dispatcher.add_handler(MessageHandler(Filters.status_update.new_chat_members,onjoin))

            updater.start_polling()
        except mysql.connector.errors.OperationalError: #连接断开 重新链接
             mydb = getConfig.getMysqlConfig()
