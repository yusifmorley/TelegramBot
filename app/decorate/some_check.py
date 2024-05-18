import telegram
from telegram import Update, Chat, User
from telegram.error import TelegramError
from telegram.ext import ContextTypes, CallbackContext
from sqlalchemy.orm.session import Session
import app
from app.admin.admin_function import bot_delete_permission, bot_restrict_permission
from app.logger.t_log import get_logging
from app.model.models import init_session, CreateThemeLogo, UserUseRecord, BanUserLogo, GroupInfo
from datetime import date

logger = get_logging().getLogger(__name__)


# 用户使用监听
# 如果被封禁了就不可使用机器人
def some_check(fun):
    async def add_check(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.effective_chat.id == -1001313322278:
            await context.bot.send_message(chat_id=update.effective_chat.id,
                                           text="此命令已经在本群组中禁用。如若使用请私聊我~")
            return
        await fun(update, context)

    return add_check
