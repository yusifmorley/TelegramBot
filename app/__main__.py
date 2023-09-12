import os

import PIL
from PIL import Image
import sqlalchemy.exc
import telegram
from telegram import Update, Bot, File, InlineKeyboardButton, InlineKeyboardMarkup,Message,Chat
from telegram.ext import Updater, ContextTypes, CallbackContext, CallbackQueryHandler, DispatcherHandlerStop
import logging
from telegram.ext import MessageHandler, Filters
from telegram.ext import CommandHandler
import mysql.connector
from urllib3.exceptions import NewConnectionError

from app.admin.person import MonitorPerson
from app.config import get_config
from app.config.get_config import get_myid
from app.db import mysqlop
from app.theme import get_radom_link, get_android, get_desktop
from app.admin import admin_function, ban_word
from  app.theme import get_ios
from app.util.create_atheme import get_attheme_color_pic,get_kyb,get_attheme
from io import BytesIO
from app.model.models import init_session, CreateThemeLogo, BanUserLogo
from sqlalchemy.orm.session import Session
from typing import IO
my_id=get_myid()
myapi = get_config.getTelegramId()  # 机器人api
# public_IO:IO|None=None #供用户发送 document 形式的　图片用　
session:Session=init_session()

request_kwargs={}
if os.environ.get('ENV')=='dev':
    request_kwargs={
    'proxy_url': 'http://127.0.0.1:10810/'}
    myapi='6520279001:AAFlM8bPclv-dZvSERAbLihBNlMNVz2KRK0' #测试机器人

updater = Updater(token=myapi, use_context=True,request_kwargs=request_kwargs)
commands = [
    telegram.BotCommand('getrandomtheme', '随机获取一个安卓或桌面种类的主题链接(有时主题可能不适用于您的设备)'),
    telegram.BotCommand('getandroidtheme', '随机获取一个安卓主题文件'),
    telegram.BotCommand('getdesktoptheme', '随机获取一个桌面主题文件'),
    telegram.BotCommand('getiostheme', '随机获取一个IOS主题链接'),
    telegram.BotCommand('create_attheme_base_pic', ' 基于图片创建attheme主题')

]


bot:Bot=updater.bot
bot.set_my_commands(commands)

dispatcher = updater.dispatcher
logging.basicConfig(filename="log/mylog.txt", format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)  # 日志
logger = logging.getLogger(__name__)
mydb = get_config.getMysqlConfig()
#初始化数据库
mysqlop.initdb(mydb)
#获取 banword 对象
BanWordObject = ban_word.banword(mydb)
#获取所有违禁词
banword = admin_function.getbanword(BanWordObject)

mon_per=MonitorPerson(10) #监控10个人

strinfo="您可以输入以下命令：\n"+\
        "/getrandomtheme , '随机获取一个随机种类的主题链接(有时主题可能不适用于您的设备)\n'"+\
        "/getandroidtheme', '随机获取一个安卓主题文件\n"+\
        "/getdesktoptheme', '随机获取一个桌面主题文件\n"+\
        "/getiostheme', '随机获取一个IOS主题链接"
exception_occurred = False
# 合并主题和背景
def on_join(update: Update, context: CallbackContext):
    # print(update.effective_chat)
    context.bot.delete_message(chat_id=update.effective_chat.id, message_id=update.effective_message.message_id)


def admin_handle(update: Update, context: CallbackContext):  # 管理员

    text = update.effective_message.text
    user = update.effective_message.from_user
    mon_per.run(user.id, user.first_name + " " + user.first_name, text, update, context,banword,logger)


def get_ran_theme(update: Update, context: CallbackContext):
   # context.bot.delete_message(message_id=update.effective_message.message_id, chat_id=update.effective_chat.id)
    path = get_radom_link.get_random_theme()

    context.bot.send_message(chat_id=update.effective_chat.id, text=path.rstrip("\n"))
    context.bot.send_message(chat_id=update.effective_chat.id, text="这是您的主题文件，亲～")


def write_ban_word(update: Update, context: CallbackContext):
    if update.message.from_user.id != 507467074:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="您不是管理员！\n" +strinfo )
        return
    global banword
    admin_function.writeBanWord(BanWordObject, context.args[0])
    banword = admin_function.getbanword(BanWordObject)
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="成功添加新的违禁词：" + context.args[0])
    context.bot.delete_message(message_id=update.effective_message.message_id, chat_id=update.effective_chat.id)


def combin_theme(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="您不是管理员！\n" +strinfo)

def error_hander(update: Update, context: CallbackContext):
    global exception_occurred ,mydb
    try:
        raise context.error
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
    except mysql.connector.errors.OperationalError as e:  # 连接断开 重新链接
        logger.warning(f"数据库链接发生错误: {e}")
        mydb = get_config.getMysqlConfig()
        exception_occurred=True
    except sqlalchemy.exc.PendingRollbackError as e:
        session.rollback()  #回滚
        logger.warning(f"数据库提交发生错误: {e}")
        exception_occurred = True
    except telegram.error.BadRequest as e:
        logger.warning(f"错误请求: {e}")
        exception_occurred = True
    except ConnectionError|NewConnectionError as e:
        logger.warning(f"网络错误: {e}")
    finally:
        if exception_occurred:
            # 异常发生时的清理操作
            context.bot.send_message(chat_id=my_id, text=f"出错了 {context.error}")
            exception_occurred=False


def get_android_theme(update: Update, context: CallbackContext):
    path=get_android.get_android_theme()
    fd= open("src/Theme/android-theme/" + path, "rb")
    data=fd.read()
    fd.close()
    preview_bytes=get_android.get_android_preview(path,data)
    context.bot.send_document(chat_id=update.effective_chat.id, document=data,filename=path)
    if preview_bytes:
        context.bot.send_photo(chat_id=update.effective_chat.id,photo=preview_bytes)
    context.bot.send_message(chat_id=update.effective_chat.id, text="这是您的主题文件，亲～")


def get_desktop_theme(update: Update, context: CallbackContext):
    path = get_desktop.get_desktop_theme()
    fd = open("src/Theme/desktop-theme/" + path, "rb")
    data = fd.read()
    fd.close()
    preview_bytes = get_desktop.get_desktop_preview(path, data)
    context.bot.send_document(chat_id=update.effective_chat.id, document=data,filename=path)
    if preview_bytes:
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=preview_bytes)
    context.bot.send_message(chat_id=update.effective_chat.id, text="这是您的主题文件，亲～")

def get_ios_theme(update: Update, context: CallbackContext):
    path = get_ios.get_random_theme()
    context.bot.send_message(chat_id=update.effective_chat.id, text=path.rstrip("\n"))
    context.bot.send_message(chat_id=update.effective_chat.id, text="这是您的主题文件，亲～")


def create_attheme(update: Update, context: CallbackContext):
    same_primary_key = update.effective_user.id
    existing_user: CreateThemeLogo | None = session.get(CreateThemeLogo, same_primary_key)
    if existing_user:
        existing_user.flag=1
    else:
        new_user = CreateThemeLogo(uid=same_primary_key,flag=1)
        session.add(new_user)

    context.bot.send_message(chat_id=update.effective_chat.id, text="请发送您的图片")

#用户发送图片
def base_photo(update: Update, context: CallbackContext,doucment_pt:str|None=None):
   pic_file : File|None=None
   picbytes = None
   picp= None
   same_primary_key = update.effective_user.id
   existing_user: CreateThemeLogo | None = session.get(CreateThemeLogo, same_primary_key)

   if not existing_user:
       return

   if existing_user and existing_user.flag == 0:
       return

   if update.message.document:
        if doucment_pt:
           fd= open(doucment_pt,'rb')
           picbytes= fd.read()
           fd.close()
           picp=doucment_pt
   else:

       pid= update.effective_message.photo[-1].file_id  #最后一个是完整图片
       pic_file:File=bot.get_file(pid)
       user_id=update.effective_user.id
       #io重用
       bio=BytesIO()
       #写入图片
       picp="src/Photo/"+str(user_id)+".png"
       fp =open(picp,"wb")

       pic_file.download(out=bio)
       fp.write(bio.getvalue())
       fp.close()
       #更新数据库

       picbytes = bio.getvalue()
       bio.close()

   content: list = get_attheme_color_pic(picbytes)
   #生成键盘
   ky = get_kyb(content[0])

   reply_markup = InlineKeyboardMarkup(ky)
   call_message: Message = update.message.reply_photo(content[1], caption="首先，请选择主题的背景颜色",
                                                         reply_markup=reply_markup)

   # 如果记录已存在，执行 变更 picpath
   existing_user.pic_path=picp
   existing_user.color_1=  None
   existing_user.color_2 = None
   existing_user.color_3 = None
   existing_user.callback_id = call_message.message_id


   session.commit()

   # pic_file.download("src/Photo/"+file_id+".jpg")
#解决 颜色三个状态
def button_update(update: Update, context: CallbackContext):
    color_arr:list|None=None
    query = update.callback_query

    user_id = update.effective_user.id
    original_reply_markup = query.message.reply_markup
    same_primary_key = user_id
    existing_user:CreateThemeLogo|None = session.get(CreateThemeLogo,same_primary_key)
    #如果是全部随机
    if len(query.data)>15:
       color_arr= query.data.split(",")
       query.message.delete()
       # 2 创建 主题 发送主题
       picp = "src/Photo/" + str(user_id) + ".png"
       fp = open(picp, "rb")
       by = fp.read()
       fp.close()
       lis =color_arr
       data = get_attheme(by, lis)
       usr_file = str(user_id) + ".attheme"
       context.bot.send_document(chat_id=update.effective_chat.id, document=data, filename=usr_file)
       context.bot.send_message(chat_id=update.effective_chat.id, text="这是您的主题文件，亲～")
       existing_user.flag = 0  # 置0
       session.commit()
       return

    if existing_user and query.message.message_id == existing_user.callback_id:
       if existing_user.color_1:
           if existing_user.color_2:
               existing_user.color_3=query.data

               # 1 删除call back
               query.message.delete()
               # 2 创建 主题 发送主题
               picp="src/Photo/"+str(user_id)+".png"
               fp=open(picp,"rb")
               by=fp.read()
               fp.close()
               lis= [existing_user.color_1, existing_user.color_2, existing_user.color_3]
               data= get_attheme(by,lis)
               usr_file=str(user_id)+".attheme"
               context.bot.send_document(chat_id=update.effective_chat.id, document=data, filename=usr_file)
               context.bot.send_message(chat_id=update.effective_chat.id, text="这是您的主题文件，亲～")
               existing_user.flag=0 #置0
           else:
               existing_user.color_2=query.data
               query.edit_message_caption(caption="好的！请设置 次要 字体颜色",reply_markup=original_reply_markup)

       else:
           existing_user.color_1=query.data
           query.edit_message_caption(caption="嗯！请设置主要字体颜色",reply_markup=original_reply_markup)

       session.commit()
    else:
        query.answer("此键盘不属于你，点击无效呢！")

#所有文件
def filter_private(update: Update, context: CallbackContext):
    if update.effective_chat.type==Chat.PRIVATE:
        existing_user: BanUserLogo | None = session.get(BanUserLogo, update.effective_user.id)
        if  existing_user:
            logger.warning("非法私聊用户,禁止使用机器人")
            raise DispatcherHandlerStop()

def parse_document(update: Update, context: CallbackContext):
    same_primary_key = update.effective_user.id
    existing_user: CreateThemeLogo | None = session.get(CreateThemeLogo, same_primary_key)

    if not existing_user:
        return

    if existing_user and existing_user.flag == 0:
        return

    document = update.message.document
    # 获取文档的文件名
    file_name:str = document.file_name
    if  '.jpg' not  in file_name and 'png' not  in file_name :
        return

    try:

       file_obj:File= document.get_file()
       file_path:str='src/Photo/'+document.file_name
       public_IO:IO= file_obj.download(file_path)
       Image.open(public_IO)
    except Exception :
       # 如果无法打开图像，它不是一个有效的图像文件
       update.message.reply_text(f"您发送了非法文件")
       return
    update.message.reply_text("嗯嗯！这确实是一个图片")
    base_photo(update,context,file_path)

def start(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id,text=strinfo)
    logger.info("可能为私聊 {}".format(str(update)))

if __name__ == "__main__":

    dispatcher.add_handler(MessageHandler(Filters.all, filter_private),group=-1)

    dispatcher.add_handler(MessageHandler(Filters.document,parse_document))

        #基于图片创建 attheme主题
    dispatcher.add_handler(CommandHandler('create_attheme_base_pic', create_attheme))
    dispatcher.add_handler(MessageHandler(Filters.photo, base_photo))
    dispatcher.add_handler(CallbackQueryHandler(button_update))

        #随机获取主题
    dispatcher.add_handler(CommandHandler('getandroidtheme', get_android_theme))
    dispatcher.add_handler(CommandHandler('getiostheme', get_ios_theme))
    dispatcher.add_handler(CommandHandler('getdesktoptheme', get_desktop_theme))
    dispatcher.add_handler(CommandHandler('getrandomtheme', get_ran_theme))

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('report', write_ban_word))

    dispatcher.add_handler(CommandHandler('combinthemeandphoto', combin_theme))
    dispatcher.add_handler(CommandHandler('getbackground', combin_theme))

    dispatcher.add_handler(MessageHandler(Filters.text, admin_handle))
    dispatcher.add_handler(MessageHandler(Filters.status_update.new_chat_members, on_join))

    dispatcher.add_error_handler(error_hander)
    updater.start_polling()
