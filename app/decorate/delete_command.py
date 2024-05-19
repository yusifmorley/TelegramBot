from telegram import Update
from telegram.ext import ContextTypes


def delete_command(fun):
    async def add_delete_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.effective_chat.id == -1001313322278:
            await context.bot.delete_message(chat_id=update.effective_chat.id, message_id=update.message.message_id)
        await fun(update, context)

    return add_delete_command
