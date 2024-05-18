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
        logger.info(f"{update}")
        await fun(update, context)

    return add_check
