from telegram import Update
from telegram.ext import ContextTypes

from app.logger.t_log import get_logging

logger = get_logging().getLogger(__name__)
def delete_command(fun):
    async def add_delete_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.effective_chat.id == -1001313322278:
            logger.info(f"{update}")
            await context.bot.delete_message(chat_id=update.effective_chat.id, message_id=update.effective_message.id)
        await fun(update, context)

    return add_delete_command
