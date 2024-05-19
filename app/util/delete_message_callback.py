from telegram import Message
from telegram.ext import ContextTypes

async def callback_plan(context: ContextTypes.DEFAULT_TYPE):
    # Beep the person who called this alarm:
    message:Message=context.job.data
    await message.delete()
