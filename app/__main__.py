import tracemalloc
import os
import traceback
from threading import Thread

import requests
from PIL import Image
import sqlalchemy.exc
import telegram
from telegram import Update, Bot, File, Chat
from telegram.ext import CallbackContext, CallbackQueryHandler, ContextTypes, Application, ApplicationBuilder
from telegram.ext import MessageHandler, filters
from telegram.ext import CommandHandler
from urllib3.exceptions import NewConnectionError
import app.model.models
from app.admin.person_monitor import MonitorPerson
from app.config import get_config
from app.config.command_list import get_command, get_command_str
from app.config.get_config import get_myid
from app.constant_obj.ThemeType import get_theme_list
from app.decorate.delete_command import delete_command
from app.decorate.listen import listen
from app.decorate.some_check import some_check
from app.exception.my_exception import NoSuitParmException
from app.logger import t_log
from app.server.theme_http import run
from app.state_machine.desk_machine import get_de_modle
from app.state_machine.android_theme import get_modle
from app.theme_file import get_radom_link, get_android, get_desktop
from app.admin import admin_function, ban_word_op
from app.theme_file import get_ios
from app.util.assrt import is_attheme
from app.model.models import init_session, CreateThemeLogo
from sqlalchemy.orm.session import Session
from app.util.sync_public_attheme import sunc_ap
from app.util.sync_public_desk import sync_dp
import logging

# 日志
logging.getLogger("httpx").setLevel(logging.INFO)
logging.getLogger("httpcore").setLevel(logging.INFO)
if os.environ.get('ENV') != 'dev':
    logging.getLogger("app.state_machine.android_theme").setLevel(logging.WARNING)
    logging.getLogger("app.state_machine.desk_machine").setLevel(logging.WARNING)
    logging.getLogger("transitions.extensions.asyncio").setLevel(logging.WARNING)
logger = t_log.get_logging().getLogger(__name__)
my_github: str = "欢迎使用主题生成机器人\n"
my_id = get_myid()
myapi = get_config.get_telegram_id()  # 机器人api
# public_IO:IO|None=None #供用户发送 document 形式的　图片用　
session: Session = init_session()

proxy_url = None
if os.environ.get('ENV') == 'dev':
    proxy_url = "http://127.0.0.1:10810/"
    myapi = '6520279001:AAFlM8bPclv-dZvSERAbLihBNlMNVz2KRK0'  # 测试机器人id
commands = get_command()
# 获取 banword 对象
bwo = ban_word_op.BanWord_OP(session)
# 获取所有违禁词
ban_words = admin_function.get_ban_word(bwo)
# 监控10个人
mon_per = MonitorPerson()
str_info = get_command_str()
# lic: dict | None = None
# 获取对象
ty_lis = get_theme_list()

async def d_command(application: Application):
    await application.bot.set_my_commands(commands)


# 合并主题和背景
async def on_join(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_message.chat.id != -1001313322278:
        return

    await context.bot.delete_message(chat_id=update.effective_chat.id, message_id=update.effective_message.message_id)


async def admin_handle(update: Update, context: ContextTypes.DEFAULT_TYPE):  # 管理员

    if update.effective_message.chat.id != -1001313322278:
        return

    text = update.effective_message.text
    if 'addtheme' in text:
        theme_link = update.message.text
        chat_id = update.message.chat_id
        # 下载主题文件
        bot = context.bot
        theme_file = await bot.get_file(theme_link)
        # 发送主题文件给用户
        await bot.send_document(chat_id=chat_id, document=theme_file.file_id)
        return
    user = update.effective_message.from_user

    if update.effective_message.chat.type == Chat.GROUP or update.effective_message.chat.type == Chat.SUPERGROUP:
        if hasattr(user, "id"):
            await  mon_per.run(user.id, user.first_name + " " + user.first_name, text, update, context, ban_words,
                               logger)
    else:
        return


@delete_command
@some_check
@listen
async def get_ran_theme(update: Update, context: ContextTypes.DEFAULT_TYPE):
    path = get_radom_link.get_random_theme()

    await context.bot.send_message(chat_id=update.effective_chat.id, text=path.rstrip("\n"))
    await context.bot.send_message(chat_id=update.effective_chat.id, text="这是您的主题文件，亲～")


async def write_ban_word(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id != 507467074:
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text="您不是管理员！\n" + str_info)
        return
    global ban_words
    if context.args[0] in ban_words:
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text="违禁词已经存在：" + context.args[0])
        return

    admin_function.write_ban_word(bwo, context.args[0])
    ban_words = admin_function.get_ban_word(bwo)
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text="成功添加新的违禁词：" + context.args[0])
    await context.bot.delete_message(message_id=update.effective_message.message_id, chat_id=update.effective_chat.id)


async def combin_theme(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text="您不是管理员！\n" + str_info)


# 错误处理
async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    try:
        raise context.error

    except sqlalchemy.exc.PendingRollbackError as e:
        session.rollback()  # 回滚
        logger.warning(f"数据库提交发生错误: {e}")
        session.close()
        app.model.models.reflush()
        logger.error("已经重置 session ")
        await context.bot.send_message(chat_id=my_id, text=f"数据库错误{e}")

    except telegram.error.BadRequest as e:
        logger.warning(f"错误请求: {e}")

    except (requests.exceptions.RequestException, requests.exceptions.ConnectionError) as e:
        logger.error(f"网络错误: {e}")
        await context.bot.send_message(chat_id=my_id, text=f"出错了 主题工厂连接失败")

    except NoSuitParmException as e:
        logger.error(f"错误的参数错误: {e}")
        await context.bot.send_message(chat_id=my_id, text=f"参数错误")

    except Exception as e:
        logger.error(f"{e}")
        await context.bot.send_message(chat_id=my_id, text=f"{e}")


@delete_command
@some_check
@listen
async def get_android_theme(update: Update, context: ContextTypes.DEFAULT_TYPE):
    path = get_android.get_android_theme()
    fd = open("src/Theme/android-theme/" + path, "rb")
    data = fd.read()
    fd.close()
    preview_bytes = get_android.get_android_preview(path, data)
    await context.bot.send_document(chat_id=update.effective_chat.id, document=data, filename=path)
    if preview_bytes:
        await context.bot.send_photo(chat_id=update.effective_chat.id, photo=preview_bytes)
    await context.bot.send_message(chat_id=update.effective_chat.id, text="这是您的主题文件，亲～")


@delete_command
@some_check
@listen
async def get_desktop_theme(update: Update, context: ContextTypes.DEFAULT_TYPE):
    path = get_desktop.get_desktop_theme()
    fd = open("src/Theme/desktop-theme/" + path, "rb")
    data = fd.read()
    fd.close()
    preview_bytes = get_desktop.get_desktop_preview(path, data)
    await context.bot.send_document(chat_id=update.effective_chat.id, document=data, filename=path[30:])
    if preview_bytes:
        await context.bot.send_photo(chat_id=update.effective_chat.id, photo=preview_bytes)
    await context.bot.send_message(chat_id=update.effective_chat.id, text="这是您的主题文件，亲～")


@delete_command
@some_check
@listen
async def get_ios_theme(update: Update, context: ContextTypes.DEFAULT_TYPE):
    path = get_ios.get_random_theme()
    await context.bot.send_message(chat_id=update.effective_chat.id, text=path.rstrip("\n"))
    await context.bot.send_message(chat_id=update.effective_chat.id, text="这是您的主题文件，亲～")


@delete_command
@listen
async def create_attheme(update: Update, context: ContextTypes.DEFAULT_TYPE):
    an = get_modle(update, context, session, 0)
    await an.recive_command()


@delete_command
@listen
async def create_tdesktop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    de = get_de_modle(update, context, session, 100)
    await de.recive_command()


# 用户发送图片
async def base_photo(update: Update, context: CallbackContext, doucment_pt: str | None = None):
    # 只有图片
    if update.effective_message.chat.type == Chat.CHANNEL:
        return
    if hasattr(update, 'message') and hasattr(update.message, "sender_chat"):
        if hasattr(update.message.sender_chat, "type"):
            if update.message.sender_chat.type == Chat.CHANNEL:
                return
    same_primary_key = update.effective_user.id
    existing_user: CreateThemeLogo | None = session.get(CreateThemeLogo, same_primary_key)
    if not existing_user:
        return
    if existing_user and existing_user.flag == 0:
        return
    if existing_user.flag == 2 or existing_user.flag == 102:  # 避免重复检测图片
        # await context.bot.send_message(chat_id=update.effective_chat.id, text="图片已经发送 亲～")
        return
    flag = existing_user.flag
    if is_attheme(existing_user.flag):
        an = get_modle(update, context, session, flag)
        await  an.recive_photo()
    else:
        de = get_de_modle(update, context, session, flag)
        await de.recive_photo()


# 解决 颜色三个状态
async def button_update(update: Update, context: ContextTypes.DEFAULT_TYPE):
    same_primary_key = update.effective_user.id
    existing_user: CreateThemeLogo | None = session.get(CreateThemeLogo, same_primary_key)
    query = update.callback_query
    # 检查
    if update.effective_user.id != get_myid():
        if not existing_user or query.message.message_id != existing_user.callback_id:
            # logger.debug(f"{update}")
            logger.warning(f"当前id为{query.message.message_id} 数据库id为{existing_user.callback_id}")
            await query.answer("此键盘不属于你，点击无效呢！")
            return
    flag = existing_user.flag
    logger.info(f"当前flag为{flag} ")
    if len(query.data) > 15:
        if is_attheme(flag):
            an = get_modle(update, context, session, flag)
            await an.recive_random_color(query, existing_user)

            return
        else:
            de = get_de_modle(update, context, session, flag)
            await de.recive_random_color(query, existing_user)

            return

    if is_attheme(flag):
        an = get_modle(update, context, session, flag)
        await an.recive_color()
    else:
        de = get_de_modle(update, context, session, flag)
        await de.recive_color()


async def parse_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    same_primary_key = update.effective_user.id
    existing_user: CreateThemeLogo | None = session.get(CreateThemeLogo, same_primary_key)

    # 文档里带图片
    # 不存在用户
    if not existing_user:
        return

    #存在用户 但状态为空
    if existing_user and existing_user.flag == 0:
        return
    # 无document属性
    if not hasattr(update.message, "document"):
        # await base_photo(update, context)
        return

    document = update.message.document
    # 获取文档的文件名

    # 名称不正确
    file_name: str = document.file_name
    if '.jpg' not in file_name and 'png' not in file_name:
        return

    try:
        file_obj: File = await document.get_file()
        file_path: str = "src/Photo/" + str(update.effective_chat.id) + ".png"
        public_IO = await file_obj.download_to_drive(file_path)
        Image.open(public_IO)
    except Exception:
        # TODO 日志
        # 如果无法打开图像，它不是一个有效的图像文件
        await update.message.reply_text(f"您发送了非法文件")
        return
    await update.message.reply_text("嗯嗯！这确实是一个图片")

    flag = existing_user.flag
    if is_attheme(existing_user.flag):
        an = get_modle(update, context, session, flag)
        await  an.recive_document(file_path)
    else:
        de = get_de_modle(update, context, session, flag)
        await de.recive_document(file_path)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if args:
        ppath = args[0]
        lic = ty_lis.get_ty_list()
        type_t = lic.get(ppath)
        if ppath is None:
            logger.warning("ppath is None")
        if type_t is None:
            logger.warning("type_t is None")

        dic = ppath
        ath = ppath + "." + type_t  # 文件路径
        pth = ppath + "." + "jpg"
        if ath.endswith("tdesktop-theme"):
            ods = "src/myserver_bot_public/desk/"
            with open(os.path.join(ods, dic, ath), "rb") as fd:
                data = fd.read()
                with open(os.path.join(ods, dic, pth), "rb") as pd:  # 图片加载
                    preview_bytes = pd.read()
                    await context.bot.send_document(chat_id=update.effective_chat.id, document=data, filename=ath[30:])
                    if preview_bytes:
                        await context.bot.send_photo(chat_id=update.effective_chat.id, photo=preview_bytes)
                    await context.bot.send_message(chat_id=update.effective_chat.id, text="这是您的主题文件，亲～")

        if ath.endswith("attheme"):
            ods = "src/myserver_bot_public/attheme/"
            with open(os.path.join(ods, dic, ath), "rb") as fd:
                data = fd.read()
                with open(os.path.join(ods, dic, pth), "rb") as pd:  # 图片加载
                    preview_bytes = pd.read()
                    await context.bot.send_document(chat_id=update.effective_chat.id, document=data, filename=ath)
                    if preview_bytes:
                        await context.bot.send_photo(chat_id=update.effective_chat.id, photo=preview_bytes)
                    await context.bot.send_message(chat_id=update.effective_chat.id, text="这是您的主题文件，亲～")

        # await update.message.reply_text(f'Command arguments: {args}')
    else:
        # 优化说明显示
        await context.bot.send_message(chat_id=update.effective_chat.id, text=str_info)
        logger.info("可能为私聊 {}".format(str(update)))


if __name__ == "__main__":
    logger.info("运行本项目必须开启ThemeFactory")
    tracemalloc.start()
    # 同步 桌面主题
    sync_dp()
    sunc_ap()
    application = ApplicationBuilder().token(myapi).post_init(d_command).proxy(proxy_url).build()

    # 同步 安卓主题
    # application.add_handler(MessageHandler(filters.ALL, filter_user), group=-1)
    application.add_handler(MessageHandler(filters.Document.IMAGE, parse_document))
    application.add_handler(MessageHandler(filters.PHOTO, base_photo))
    # 基于图片创建 attheme主题
    application.add_handler(CommandHandler('create_attheme_base_pic', create_attheme))

    application.add_handler(CallbackQueryHandler(button_update))
    # 基于图片创建 tdesktop主题
    application.add_handler(CommandHandler('create_tdesktop_base_pic', create_tdesktop))

    # 随机获取主题
    application.add_handler(CommandHandler('getandroidtheme', get_android_theme))
    application.add_handler(CommandHandler('getiostheme', get_ios_theme))
    application.add_handler(CommandHandler('getdesktoptheme', get_desktop_theme))
    application.add_handler(CommandHandler('getrandomtheme', get_ran_theme))

    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('report', write_ban_word))

    application.add_handler(CommandHandler('combinthemeandphoto', combin_theme))
    application.add_handler(CommandHandler('getbackground', combin_theme))

    # application.add_handler(MessageHandler(filters.TEXT, admin_handle))
    application.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, on_join))

    application.add_error_handler(error_handler)

    # 开启辅助线程
    server = Thread(target=run)
    # run_on(port_number) #Run in main thread
    # server.daemon = True # Do not make us wait for you to exit
    server.start()
    application.run_polling()
