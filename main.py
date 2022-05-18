from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update

from getPreview import getPreview

from telegram.ext import Updater, CallbackContext, CallbackQueryHandler
import logging
from  getbackground import getbackground
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

themeFileDowmloaded = False
themePhontoDownloaded = False
spuperflag = False
Securitydoor= False


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")
    keyboard = [
        [
            InlineKeyboardButton("合并主题和图片", callback_data='1'),
            InlineKeyboardButton("提取主题背景", callback_data='2'),
        ],

    ]
    reply_markup = InlineKeyboardMarkup(keyboard)  # 2
    update.message.reply_text("请选择服务", reply_markup=reply_markup)


def keyboard_callback(update, contetx):
    query = update.callback_query
    query.answer()
    # query.edit_message_text(text=f"Selected option: {query.data} ")
    global spuperflag
    global Securitydoor
    Securitydoor= True  #安全们开启
    if query.data == '1':
        query.edit_message_text(text="请发送您的主题和图片")
    else:
        query.edit_message_text(text="请发送您的主题")
        spuperflag = True



def downloadtheme(update, context):
    global themeFileDowmloaded
    global themePhontoDownloaded
    global spuperflag
    global Securitydoor
    if Securitydoor:
        context.bot.send_message(chat_id=update.effective_chat.id, text="请输入 /start 命令")
        return
    context.bot.send_message(chat_id=update.effective_chat.id, text="我以收到主题文件")
    file = context.bot.getFile(update.message.document.file_id)
    file.download("temptheme/" + update.message.document.file_name)
    themeFileDowmloaded = "temptheme/" + update.message.document.file_name
    if spuperflag :
        picpath=getbackground(themeFileDowmloaded)
        context.bot.send_document(chat_id=update.effective_chat.id,document=open(picpath, "rb"))
        spuperflag=False
        return

    if themeFileDowmloaded and themePhontoDownloaded:
        newthemepath = combinate(themeFileDowmloaded, themePhontoDownloaded)
        context.bot.send_document(chat_id=update.effective_chat.id, document=open(newthemepath, "rb"))
        context.bot.send_message(chat_id=update.effective_chat.id, text="成功！，这是合成的新主题")
        # alls = getPreview(newthemepath)
        # channelandthemepara = {"themeName": newthemepath[newthemepath.find("/"):],
        #                        "file": newthemepath}
        # alls = dict(alls, **channelandthemepara)
        # createMysql(alls)
        themeFileDowmloaded = False
        themePhontoDownloaded = False
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="我需要一张背景图片")


def handlePhoto(update, context):
    global themeFileDowmloaded
    global themePhontoDownloaded
    global spuperflag
    global Securitydoor
    if Securitydoor:
        context.bot.send_message(chat_id=update.effective_chat.id, text="请输入 /start 命令")
        return
    if spuperflag:
        return
    tim = time.localtime()
    timstr = time.strftime("%Y-%m-%d-%H-%M-%S", tim)
    context.bot.send_message(chat_id=update.effective_chat.id, text="这确实是一张图片！")
    file = context.bot.getFile(update.message.photo[2]['file_id'])
    photoPath = "tempthemephoto/" + timstr + ".jpg"
    file.download(photoPath)
    context.bot.send_message(chat_id=update.effective_chat.id, text="图片已下载")  # 下载图片
    themePhontoDownloaded = "tempthemephoto/" + timstr + ".jpg"
    if themeFileDowmloaded and themePhontoDownloaded:
        newthemepath = combinate(themeFileDowmloaded, themePhontoDownloaded)
        context.bot.send_document(chat_id=update.effective_chat.id, document=open(newthemepath, "rb"))
        context.bot.send_message(chat_id=update.effective_chat.id, text="成功！，这是合成的新主题")
        # alls = getPreview(newthemepath)  # 2p
        # channelandthemepara = {"themeName": newthemepath[newthemepath.find("/"):],
        #                        "file": newthemepath}
        # alls = dict(alls, **channelandthemepara)
        # createMysql(alls)
        # print('success!')
        themeFileDowmloaded = False
        themePhontoDownloaded = False
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="我需要一个主题文件")


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
