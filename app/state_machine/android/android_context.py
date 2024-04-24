from io import BytesIO
from sqlalchemy.orm import Session
from telegram import Update, Chat, Message
from telegram.ext import ContextTypes
import app.util.file_name_gen as f_n
import app.util.get_time as g_t
from app.logger import t_log
from app.model.models import CreateThemeLogo
from app.util.create_atheme import get_attheme_color_pic, get_kyb, get_transparent_ky, get_attheme
from app.util.create_desktop import get_desktop_kyb
from app.util.db_op import clear
logger = t_log.get_logging().getLogger(__name__)
class AndroidContext:
        def __init__(self, update: Update,
                     context: ContextTypes.DEFAULT_TYPE,
                     session: Session, flag: int = 0
                     ):
            # TODO 通过数据库查询直接赋值状态 可以直接复用同一个类
            # 1<=flag<100
            # 0是未创建状态
            # 依次类推

            self.update = update
            self.context = context
            self.session = session
            self.flag = flag
            self.same_primary_key = self.update.effective_user.id
            self.existing_user: CreateThemeLogo | None = self.session.get(CreateThemeLogo, self.same_primary_key)
            if hasattr(update, "callback_query"):
                self.query = update.callback_query
            self.user_id = update.effective_user.id
            if hasattr(update, "query"):
                self.original_reply_markup = self.query.message.reply_markup
            logger.info("当前状态为{}".format(self.flag))

        async def can_run(self):  # 日志
            logger.info("运行了")
            existing_user: CreateThemeLogo | None = self.session.get(CreateThemeLogo, self.same_primary_key)
            if existing_user:
                clear(existing_user)
                existing_user.flag = 1
            else:
                new_user = CreateThemeLogo(uid=self.same_primary_key, flag=1)
                self.session.add(new_user)

            self.session.commit()
            await self.context.bot.send_message(chat_id=self.update.effective_chat.id, text="请发送您的图片.")

        async def on_exit(self):  # 日志
            self.session.commit()

        async def set_bg(self):
            self.existing_user.color_1 = self.query.data
            self.existing_user.flag = self.existing_user.flag + 1
            self.session.commit()

            await self.query.edit_message_caption(caption="嗯！请设置主要字体颜色",
                                                  reply_markup=self.original_reply_markup)

        async def set_mian_c(self):
            self.existing_user.color_2 = self.query.data
            self.existing_user.flag = self.existing_user.flag + 1
            await self.query.edit_message_caption(caption="好的！请设置 次要 字体颜色",
                                                  reply_markup=self.original_reply_markup)

        async def set_s_c(self):
            self.existing_user.color_3 = self.query.data
            self.existing_user.flag = self.existing_user.flag + 1
            reply_markup = get_transparent_ky()
            await  self.query.edit_message_caption(caption="嗯嗯！您可以继续选择", reply_markup=reply_markup)

        async def set_can_opc(self):
            await self.query.message.delete()
            # 2 创建 主题 发送主题
            picp = "src/Photo/" + str(self.user_id) + ".png"
            fp = open(picp, "rb")
            by = fp.read()
            fp.close()
            lis = [self.existing_user.color_1, self.existing_user.color_2, self.existing_user.color_3]

            if self.query.data == "off":
                data = get_attheme(by, lis)
            elif self.query.data == "tran":
                data = get_attheme(by, lis, True)

            usr_file = f_n.gen_name(g_t.get_now()) + ".attheme"

            await self.context.bot.send_document(chat_id=self.update.effective_chat.id, document=data,
                                                 filename=usr_file)
            await self.context.bot.send_message(chat_id=self.update.effective_chat.id, text="这是您的主题文件，亲～")
            self.existing_user.flag = self.existing_user.flag + 1
            self.session.commit()

        async def set_clear(self):
            clear(self.existing_user)  # 清除置空
            self.session.commit()

        async def send_message(self):
            same_primary_key = self.update.effective_user.id
            existing_user: CreateThemeLogo | None = self.session.get(CreateThemeLogo, same_primary_key)
            if existing_user:
                clear(existing_user)
                existing_user.flag = 1
            else:
                new_user = CreateThemeLogo(uid=same_primary_key, flag=1)
                self.session.add(new_user)
            self.session.commit()
            await self.context.bot.send_message(chat_id=self.update.effective_chat.id, text="请发送您的图片")

        async def handle_photo(self):
            if self.update.effective_message.chat.type == Chat.CHANNEL:
                return
            pic_bytes = None
            same_primary_key = self.update.effective_user.id
            existing_user: CreateThemeLogo | None = self.session.get(CreateThemeLogo, same_primary_key)
            if not existing_user:
                return
            # 未创建则发送图图片
            if existing_user and existing_user.flag == 0:
                return

            # if self.update.message.document:
            #     if doucment_pt:
            #         fd = open(doucment_pt, 'rb')
            #         pic_bytes = fd.read()
            #         fd.close()
            #         existing_user.pic_path = doucment_pt
            # else:

            pid = self.update.effective_message.photo[-1].file_id  # 最后一个是完整图片
            pic_file = await self.context.bot.get_file(pid)
            user_id = self.update.effective_user.id
            # io重用
            bio = BytesIO()
            # 写入图片
            pic_p = "src/Photo/" + str(user_id) + ".png"
            fp = open(pic_p, "wb")
            await pic_file.download_to_memory(bio)
            fp.write(bio.getvalue())
            fp.close()
            # 更新数据库
            pic_bytes = bio.getvalue()
            bio.close()
            existing_user.pic_path = pic_p
            content: list = get_attheme_color_pic(pic_bytes)
            # 生成键盘
            reply_markup = get_kyb(content[0])
            call_message: Message = await self.update.message.reply_photo(content[1],
                                                                          caption="首先，请选择主题的背景颜色",
                                                                          reply_markup=reply_markup)
            # 转变状态
            existing_user.flag = existing_user.flag + 1
            # 如果记录已存在，执行 变更 picpath
            existing_user.callback_id = call_message.message_id
            self.session.commit()