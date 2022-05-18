from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update

from getPreview import getPreview

from telegram.ext import Updater, CallbackContext, CallbackQueryHandler
import logging

from mysqlop import createMysql
from telegram.ext import MessageHandler, Filters
from telegram.ext import CommandHandler

from combinate import combinate
import time

myapi = "1941238169:AAG4FT5Bs1CZLLDZ5bidH6Sk4EgzsQqEgS8"
updater = Updater(token=myapi, use_context=True)
dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)  # 日志

myarr = {}

themeFileDowmloaded=False
themePhontoDownloaded=False
spuperflag=False



def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")
    keyboard = [
        [
            InlineKeyboardButton("合并主题和图片", callback_data='1'),
            InlineKeyboardButton("提取主题背景", callback_data='2'),
        ],

    ]  # 1
    reply_markup = InlineKeyboardMarkup(keyboard)  # 2
    update.message.reply_text("请选择服务", reply_markup=reply_markup)


def keyboard_callback(update,contetx): #4
    query = update.callback_query #5
    query.answer() #6
    query.edit_message_text(text=f"Selected option: {query.data} ")
    if query.data=='1':

        query.edit_message_text(text="请发送您的主题和图片")

    else:
        query.edit_message_text(text="请发送您的主题")


def downloadtheme(update, context):
        global themeFileDowmloaded
        global themePhontoDownloaded
        context.bot.send_message(chat_id=update.effective_chat.id, text="You send me a theme!")
        file = context.bot.getFile(update.message.document.file_id)
        file.download("temptheme/" + update.message.document.file_name)    #下载主题
        themeFileDowmloaded="temptheme/" + update.message.document.file_name
        if themeFileDowmloaded and themePhontoDownloaded:
            newthemepath=combinate(themeFileDowmloaded,themePhontoDownloaded)
            context.bot.send_document(chat_id=update.effective_chat.id, document=open(newthemepath, "rb"))
            context.bot.send_message(chat_id=update.effective_chat.id, text="This is your newTheme!")

            alls=getPreview(newthemepath) #2p

            channelandthemepara = {"themeName": newthemepath[newthemepath.find("/"):],
                                   "file": newthemepath}
            alls = dict(alls, **channelandthemepara)
            createMysql(alls)
            print('success!')
            context.bot.send_message(chat_id=update.effective_chat.id, text="success! query is OK!")
            themeFileDowmloaded = False
            themePhontoDownloaded = False
        else:
            context.bot.send_message(chat_id=update.effective_chat.id, text="l need a photo")


def handlePhoto(update, context):
    global themeFileDowmloaded
    global themePhontoDownloaded
    tim = time.localtime()
    timstr = time.strftime("%Y-%m-%d-%H-%M-%S", tim)
    context.bot.send_message(chat_id=update.effective_chat.id, text="This is a Photo!")
    file = context.bot.getFile(update.message.photo[2]['file_id'])
    photoPath="tempthemephoto/" + timstr + ".jpg"
    file.download(photoPath)
    context.bot.send_message(chat_id=update.effective_chat.id, text="Photo is downloaded")  #下载图片
    themePhontoDownloaded="tempthemephoto/" + timstr + ".jpg"

    if themeFileDowmloaded and themePhontoDownloaded:
        newthemepath = combinate(themeFileDowmloaded, themePhontoDownloaded)
        context.bot.send_document(chat_id=update.effective_chat.id, document=open(newthemepath, "rb"))
        context.bot.send_message(chat_id=update.effective_chat.id, text="This is your newTheme!")
        alls = getPreview(newthemepath)  # 2p
        channelandthemepara = {"themeName": newthemepath[newthemepath.find("/"):],
                               "file": newthemepath}
        alls = dict(alls, **channelandthemepara)
        createMysql(alls)
        print('success!')
        context.bot.send_message(chat_id=update.effective_chat.id, text="success! query is OK!")
        themeFileDowmloaded = False
        themePhontoDownloaded = False
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="l need a theme")





combins = CommandHandler('start', start)
dispatcher.add_handler(combins)





unknown_handler = MessageHandler(Filters.photo, handlePhoto)
dispatcher.add_handler(unknown_handler)

checkatthem = MessageHandler(Filters.document.file_extension("attheme"), downloadtheme)
dispatcher.add_handler(checkatthem)

updater.dispatcher.add_handler(CallbackQueryHandler(keyboard_callback))
updater.start_polling()

# need  file jump  preview file
# need  link  jump  preview file
