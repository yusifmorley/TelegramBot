from sqlalchemy.orm import Session
from telegram import Update, InlineKeyboardMarkup
from telegram.ext import CallbackContext

from app.model.models import CreateThemeLogo, init_session
from app.util.create_atheme import get_attheme, get_transparent_ky
import app.util.file_name_gen as f_n
import app.util.get_time as g_t
session:Session=init_session()
def callback_android_handle(update: Update, context: CallbackContext):
    data = None
    query = update.callback_query
    user_id = update.effective_user.id
    original_reply_markup = query.message.reply_markup
    same_primary_key = user_id
    existing_user:CreateThemeLogo|None = session.get(CreateThemeLogo,same_primary_key)

    if not existing_user or  query.message.message_id != existing_user.callback_id:
        query.answer("此键盘不属于你，点击无效呢！")
        return

    if existing_user.color_3:
        # 1 删除call back
        query.message.delete()
        # 2 创建 主题 发送主题
        picp = "src/Photo/" + str(user_id) + ".png"
        fp = open(picp, "rb")
        by = fp.read()
        fp.close()
        lis = [existing_user.color_1, existing_user.color_2, existing_user.color_3]

        if query.data == "off":
            data = get_attheme(by, lis)
        elif query.data == "tran":
            data = get_attheme(by, lis, True)

        usr_file =f_n.gen_name(g_t.get_now()) + ".attheme"

        context.bot.send_document(chat_id=update.effective_chat.id, document=data, filename=usr_file)
        context.bot.send_message(chat_id=update.effective_chat.id, text="这是您的主题文件，亲～")
        existing_user.flag = 0  # 置0
        session.commit()
        return
    #如果是全部随机
    if len(query.data)>15:
       color_arr= query.data.split(",")
       existing_user.color_1=color_arr[0]
       existing_user.color_2=color_arr[1]
       existing_user.color_3=color_arr[2]
       reply_markup = get_transparent_ky()
       query.edit_message_caption(caption="嗯嗯！您可以继续选择", reply_markup=reply_markup)
       session.commit()
       return

    if existing_user.color_1:
        if existing_user.color_2:
            if not existing_user.color_3:
                existing_user.color_3 = query.data
                reply_markup = get_transparent_ky()
                query.edit_message_caption(caption="嗯嗯！您可以继续选择", reply_markup=reply_markup)
        else:
            existing_user.color_2=query.data
            query.edit_message_caption(caption="好的！请设置 次要 字体颜色",reply_markup=original_reply_markup)

    else:
        existing_user.color_1=query.data
        query.edit_message_caption(caption="嗯！请设置主要字体颜色",reply_markup=original_reply_markup)

    session.commit()