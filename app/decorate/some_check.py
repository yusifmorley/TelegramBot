from telegram import Update
from telegram.ext import ContextTypes
from app.logger.t_log import get_logging
from app.util.delete_message_callback import callback_plan
logger = get_logging().getLogger(__name__)

# 用户使用监听
# 如果被封禁了就不可使用机器人
def some_check(fun):
    async def add_check(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.effective_chat.id == -1001313322278:
            message = await context.bot.send_message(chat_id=update.effective_chat.id,
                                                     text="此命令已经在本群组中禁用。如若使用请私聊我~")
            context.job_queue.run_once(callback_plan, 60, data=message)
            return
        await fun(update, context)

    return add_check
