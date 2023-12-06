from sqlalchemy.orm import Session
from telegram import Update, InlineKeyboardMarkup
from telegram.ext import CallbackContext

from app.model.models import CreateThemeLogo, init_session
from app.util.create_atheme import get_attheme, get_transparent_ky
from app.util.create_desktop import get_tdektop
import app.util.file_name_gen as f_n
import app.util.get_time as g_t

session: Session = init_session()


def callback_desktop_handle(update: Update, context: CallbackContext):
    data = None
    query = update.callback_query
    user_id = update.effective_user.id
    original_reply_markup = query.message.reply_markup
    same_primary_key = user_id
    existing_user: CreateThemeLogo | None = session.get(CreateThemeLogo, same_primary_key)

    # 全部随机
    if len(query.data) > 8:
        color_arr = query.data.split(",")
        query.message.delete()
        # 2 创建 主题 发送主题
        picp = "src/Photo/" + str(user_id) + ".png"
        fp = open(picp, "rb")
        by = fp.read()
        fp.close()
        data = get_tdektop(by, color_arr)
        usr_file = f_n.gen_name(g_t.get_now()) + ".tdesktop-theme"
        context.bot.send_document(chat_id=update.effective_chat.id, document=data, filename=usr_file)
        context.bot.send_message(chat_id=update.effective_chat.id, text="这是您的主题文件，亲～")
        existing_user.flag = 0  # 置0
        session.commit()
        return

    # 表明 这是第二次
    if existing_user.color_1:
        # 1 删除call back
        query.message.delete()
        # 2 创建 主题 发送主题
        picp = "src/Photo/" + str(user_id) + ".png"
        fp = open(picp, "rb")
        by = fp.read()
        fp.close()
        lis = [existing_user.color_1, query.data]

        data = get_tdektop(by, lis)

        usr_file = f_n.gen_name(g_t.get_now()) + ".tdesktop-theme"

        context.bot.send_document(chat_id=update.effective_chat.id, document=data, filename=usr_file)

        context.bot.send_message(chat_id=update.effective_chat.id, text="这是您的主题文件，亲～")

        existing_user.flag = 0  # 置0

        session.commit()
        return

    # 如果是全部随机
    existing_user.color_1 = query.data
    query.edit_message_caption(caption="嗯！请设置次要颜色", reply_markup=original_reply_markup)
    session.commit()
