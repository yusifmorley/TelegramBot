import base64
import os
import traceback

from PIL import Image
import sqlalchemy.exc
import telegram
from telegram import Update, Bot, File, InlineKeyboardMarkup, Message, Chat
from telegram.ext import Updater, CallbackContext, CallbackQueryHandler
from telegram.ext import MessageHandler, Filters
from telegram.ext import CommandHandler
import mysql.connector
from urllib3.exceptions import NewConnectionError
import app.model.models
from app.admin.person_monitor import MonitorPerson
from app.callback import callback_android, callback_desktop
from app.config import get_config
from app.config.command_list import get_command, get_command_str
from app.config.get_config import get_myid
from app.db import mysqlop
from app.decorate.listen import listen
from app.logger import t_log
from app.theme_file import get_radom_link, get_android, get_desktop
from app.admin import admin_function, ban_word
from app.theme_file import get_ios
from app.util.create_atheme import get_attheme_color_pic, get_kyb, get_attheme, get_transparent_ky
from io import BytesIO
from app.model.models import init_session, CreateThemeLogo, BanUserLogo
from sqlalchemy.orm.session import Session
from typing import IO

from app.util.create_desktop import get_desktop_kyb
from app.util.db_op import clear
from app.util.sync_public_attheme import sunc_ap
from app.util.sync_public_desk import sync_dp

my_github: str = ("欢迎使用主题生成机器人\n")

my_id = get_myid()
myapi = get_config.get_telegram_id()  # 机器人api
# public_IO:IO|None=None #供用户发送 document 形式的　图片用　
session: Session = init_session()

request_kwargs = {}
if os.environ.get('ENV') == 'dev':
    request_kwargs = {
        'proxy_url': 'http://127.0.0.1:10810/'}
    myapi = '6520279001:AAFlM8bPclv-dZvSERAbLihBNlMNVz2KRK0'  # 测试机器人id

updater = Updater(token=myapi, use_context=True, request_kwargs=request_kwargs)
commands =get_command()
bot: Bot = updater.bot
bot.set_my_commands(commands)
dispatcher = updater.dispatcher

# 日志
logger = t_log.get_logger()

# 数据库
mydb = get_config.get_mysql_config()
# 初始化数据库
mysqlop.initdb(mydb)

# 获取 banword 对象
BanWordObject = ban_word.BanWord(mydb)

# 获取所有违禁词
ban_words = admin_function.get_ban_word(BanWordObject)

# 监控10个人
mon_per = MonitorPerson(10)

strinfo = get_command_str()
# 合并主题和背景
def on_join(update: Update, context: CallbackContext):
    # 如果没有权限
    if app.admin.admin_function.bot_delete_permission(update, context) == 0:
        return

    context.bot.delete_message(chat_id=update.effective_chat.id, message_id=update.effective_message.message_id)


def admin_handle(update: Update, context: CallbackContext):  # 管理员

    if update.effective_message.chat.id !=-1001313322278:
        return

    text = update.effective_message.text
    if 'addtheme' in text:
        theme_link = update.message.text
        chat_id = update.message.chat_id
        # 下载主题文件
        bot = context.bot
        theme_file = bot.get_file(theme_link)
        # 发送主题文件给用户
        bot.send_document(chat_id=chat_id, document=theme_file.file_id)
        return
    user = update.effective_message.from_user
    
    if update.effective_message.chat.type == Chat.GROUP or update.effective_message.chat.type == Chat.SUPERGROUP:
        if hasattr(user, "id"):
            mon_per.run(user.id, user.first_name + " " + user.first_name, text, update, context, ban_words, logger)
    else:
        return



@listen
def get_ran_theme(update: Update, context: CallbackContext):
    path = get_radom_link.get_random_theme()

    context.bot.send_message(chat_id=update.effective_chat.id, text=path.rstrip("\n"))
    context.bot.send_message(chat_id=update.effective_chat.id, text="这是您的主题文件，亲～")


def write_ban_word(update: Update, context: CallbackContext):
    if update.message.from_user.id != 507467074:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="您不是管理员！\n" + strinfo)
        return
    global ban_words
    admin_function.write_ban_word(BanWordObject, context.args[0])
    ban_words = admin_function.get_ban_word(BanWordObject)
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="成功添加新的违禁词：" + context.args[0])
    context.bot.delete_message(message_id=update.effective_message.message_id, chat_id=update.effective_chat.id)


def combin_theme(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="您不是管理员！\n" + strinfo)


# 错误处理
def error_handler(update: Update, context: CallbackContext):
    global  mydb
    try:
        raise context.error

    except mysql.connector.errors.OperationalError as e:  # 连接断开 重新链接
        logger.warning(f"数据库链接发生错误: {e}")
        mydb = get_config.get_mysql_config()

    except sqlalchemy.exc.PendingRollbackError as e:
        session.rollback()  # 回滚
        logger.warning(f"数据库提交发生错误: {e}")

    except telegram.error.BadRequest as e:
        logger.warning(f"错误请求: {e}")

    except (ConnectionError, NewConnectionError) as e:
        logger.warning(f"网络错误: {e}")

    finally:
        session.close()
        app.model.models.reflush()
        logger.warning("已经重置 session ")
            # 异常发生时的清理操作
        info = traceback.format_exc()
        context.bot.send_message(chat_id=my_id, text=f"出错了 {context.error},\n{update} \n{info}")

@listen
def get_android_theme(update: Update, context: CallbackContext):
    path = get_android.get_android_theme()
    fd = open("src/Theme/android-theme/" + path, "rb")
    data = fd.read()
    fd.close()
    preview_bytes = get_android.get_android_preview(path, data)
    context.bot.send_document(chat_id=update.effective_chat.id, document=data, filename=path)
    if preview_bytes:
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=preview_bytes)
    context.bot.send_message(chat_id=update.effective_chat.id, text="这是您的主题文件，亲～")


@listen
def get_desktop_theme(update: Update, context: CallbackContext):
    path = get_desktop.get_desktop_theme()
    fd = open("src/Theme/desktop-theme/" + path, "rb")
    data = fd.read()
    fd.close()
    preview_bytes = get_desktop.get_desktop_preview(path, data)
    context.bot.send_document(chat_id=update.effective_chat.id, document=data, filename=path)
    if preview_bytes:
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=preview_bytes)
    context.bot.send_message(chat_id=update.effective_chat.id, text="这是您的主题文件，亲～")


@listen
def get_ios_theme(update: Update, context: CallbackContext):
    path = get_ios.get_random_theme()
    context.bot.send_message(chat_id=update.effective_chat.id, text=path.rstrip("\n"))
    context.bot.send_message(chat_id=update.effective_chat.id, text="这是您的主题文件，亲～")


@listen
def create_attheme(update: Update, context: CallbackContext):
    same_primary_key = update.effective_user.id
    existing_user: CreateThemeLogo | None = session.get(CreateThemeLogo, same_primary_key)
    if existing_user:
        clear(existing_user)
        existing_user.flag = 1

    else:
        new_user = CreateThemeLogo(uid=same_primary_key, flag=1)
        session.add(new_user)

    session.commit()
    context.bot.send_message(chat_id=update.effective_chat.id, text="请发送您的图片")


@listen
def create_tdesktop(update: Update, context: CallbackContext):
    same_primary_key = update.effective_user.id
    existing_user: CreateThemeLogo | None = session.get(CreateThemeLogo, same_primary_key)
    if existing_user:
        clear(existing_user)
        existing_user.flag = 4
    else:
        new_user = CreateThemeLogo(uid=same_primary_key, flag=4)
        session.add(new_user)

    session.commit()
    context.bot.send_message(chat_id=update.effective_chat.id, text="请发送您的图片")


# 用户发送图片
def base_photo(update: Update, context: CallbackContext, doucment_pt: str | None = None):
    # 只有图片
    if update.effective_message.chat.type == Chat.CHANNEL:
        return

    pic_bytes = None
    same_primary_key = update.effective_user.id
    if hasattr(update.message, "caption"):
        text = update.message.caption
        if text:
            user = update.effective_user
            boo = mon_per.run(user.id, user.first_name + " " + user.first_name, text, update, context, ban_words,
                              logger)
            if boo:
                return

    existing_user: CreateThemeLogo | None = session.get(CreateThemeLogo, same_primary_key)
    if not existing_user:
        return

    if existing_user and existing_user.flag == 0:
        return

    if update.message.document:
        if doucment_pt:
            fd = open(doucment_pt, 'rb')
            pic_bytes = fd.read()
            fd.close()
            existing_user.pic_path = doucment_pt
    else:
        pid = update.effective_message.photo[-1].file_id  # 最后一个是完整图片
        pic_file = bot.get_file(pid)
        user_id = update.effective_user.id
        # io重用
        bio = BytesIO()
        # 写入图片
        pic_p = "src/Photo/" + str(user_id) + ".png"
        fp = open(pic_p, "wb")

        pic_file.download(out=bio)
        fp.write(bio.getvalue())
        fp.close()
        # 更新数据库

        pic_bytes = bio.getvalue()
        bio.close()

        existing_user.pic_path = pic_p

    content: list = get_attheme_color_pic(pic_bytes)
    # 生成键盘

    if existing_user.flag != 4:

        reply_markup = get_kyb(content[0])
        call_message: Message = update.message.reply_photo(content[1], caption="首先，请选择主题的背景颜色",
                                                           reply_markup=reply_markup)
    else:
        reply_markup = get_desktop_kyb(content[0])
        call_message: Message = update.message.reply_photo(content[1], caption="首先，请选择主题的背景颜色",
                                                           reply_markup=reply_markup)

    # 如果记录已存在，执行 变更 picpath

    existing_user.callback_id = call_message.message_id
    session.commit()

    # pic_file.download("src/Photo/"+file_id+".jpg")


# 解决 颜色三个状态
def button_update(update: Update, context: CallbackContext):
    same_primary_key = update.effective_user.id
    existing_user: CreateThemeLogo | None = session.get(CreateThemeLogo, same_primary_key)
    query = update.callback_query
    # 检查
    if not existing_user or query.message.message_id != existing_user.callback_id:
        query.answer("此键盘不属于你，点击无效呢！")
        return

    if existing_user.flag == 1:
        callback_android.callback_android_handle(update, context)

    if existing_user.flag == 4:
        callback_desktop.callback_desktop_handle(update, context)



def parse_document(update: Update, context: CallbackContext):
    same_primary_key = update.effective_user.id
    existing_user: CreateThemeLogo | None = session.get(CreateThemeLogo, same_primary_key)

    # 文档里带图片

    if not existing_user:
        return

    if existing_user and existing_user.flag == 0:
        return

    if not hasattr(update.message, "document"):
        base_photo(update, context)
        return

    document = update.message.document
    # 获取文档的文件名

    file_name: str = document.file_name
    if '.jpg' not in file_name and 'png' not in file_name:
        return

    try:

        file_obj: File = document.get_file()
        file_path: str = "src/Photo/" + str(update.effective_user.id) + ".png"
        public_IO: IO = file_obj.download(file_path)
        Image.open(public_IO)

    except Exception:
        # 如果无法打开图像，它不是一个有效的图像文件
        update.message.reply_text(f"您发送了非法文件")
        return
    update.message.reply_text("嗯嗯！这确实是一个图片")

    base_photo(update, context, file_path)


def start(update: Update, context: CallbackContext):
    args = context.args
    if args:
        path = base64.b64decode(args[0]).decode()
        if path.endswith("tdesktop-theme"):
            with open("src/myserver_bot_public/desk/" + path, "rb") as fd:
                data = fd.read()
                ppath = path.replace("tdesktop-theme", "jpg")
                with open("src/myserver_bot_public/desk/" + ppath, "rb") as pd:  # 图片加载
                    preview_bytes = pd.read()
                    context.bot.send_document(chat_id=update.effective_chat.id, document=data, filename=path)
                    if preview_bytes:
                        context.bot.send_photo(chat_id=update.effective_chat.id, photo=preview_bytes)
                    context.bot.send_message(chat_id=update.effective_chat.id, text="这是您的主题文件，亲～")

        if path.endswith("attheme"):
            with open("src/myserver_bot_public/attheme/" + path, "rb") as fd:
                data = fd.read()
                ppath = path.replace("attheme", "jpg")
                with open("src/myserver_bot_public/attheme/" + ppath, "rb") as pd:  # 图片加载
                    preview_bytes = pd.read()
                    context.bot.send_document(chat_id=update.effective_chat.id, document=data, filename=path)
                    if preview_bytes:
                        context.bot.send_photo(chat_id=update.effective_chat.id, photo=preview_bytes)
                    context.bot.send_message(chat_id=update.effective_chat.id, text="这是您的主题文件，亲～")
        # update.message.reply_text(f'Command arguments: {args}')
    else:
        # 优化说明显示
        context.bot.send_message(chat_id=update.effective_chat.id, text=strinfo)
        logger.info("可能为私聊 {}".format(str(update)))


if __name__ == "__main__":
    logger.info("运行本项目必须开启ThemeFactory")
    # 同步 桌面主题
    sync_dp()
    sunc_ap()
    # 同步 安卓主题
    # dispatcher.add_handler(MessageHandler(Filters.all, filter_user), group=-1)
    dispatcher.add_handler(MessageHandler(Filters.document.category("image"), parse_document))
    dispatcher.add_handler(MessageHandler(Filters.photo, base_photo))
    # 基于图片创建 attheme主题
    dispatcher.add_handler(CommandHandler('create_attheme_base_pic', create_attheme))

    dispatcher.add_handler(CallbackQueryHandler(button_update))
    # 基于图片创建 tdesktop主题
    dispatcher.add_handler(CommandHandler('create_tdesktop_base_pic', create_tdesktop))

    # 随机获取主题
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

    if os.environ.get('ENV') != 'dev':
        dispatcher.add_error_handler(error_handler)

    updater.start_polling()
