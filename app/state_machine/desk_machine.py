from io import BytesIO

from sqlalchemy.orm import Session
from telegram import Update, Chat, Message
from telegram.ext import ContextTypes
from transitions import Machine, State
import app.util.file_name_gen as f_n
import app.util.get_time as g_t
from app.model.models import CreateThemeLogo
from app.util.create_atheme import get_attheme_color_pic, get_kyb, get_transparent_ky, get_attheme
from app.util.create_desktop import get_desktop_kyb
from app.util.db_op import clear


class Desk_Machine(Machine):
    def __init__(self, update: Update,
                 context: ContextTypes.DEFAULT_TYPE,
                 session: Session,
                 flag
                 ):
        # TODO 通过数据库查询直接赋值状态 可以直接复用同一个类

        self.update = update
        self.context = context
        self.session = session
        self.same_primary_key = self.update.effective_user.id
        self.existing_user: CreateThemeLogo | None = (self.session.get(CreateThemeLogo, self.same_primary_key))

        self.query = update.callback_query
        self.user_id = update.effective_user.id
        self.original_reply_markup = self.query.message.reply_markup

        states = [State("可创建状态", on_enter="can_run"),
                  State("拥有图片", on_enter="handle_photo"),
                  State('拥有主背景颜色', on_enter="set_bg"),
                  State('拥有主字体颜色', on_enter="set_mian_c"),
                  State('拥有次要颜色', on_enter="set_s_c"),
                  State("已经选择是否透明", on_enter="set_can_opc"),
                  State("未创建状态", on_enter="set_clear")
                  ]  # 状态
        transitions = [  # 状态映射 （重要）
            {'trigger': 'recive_command', 'source': "未创建状态", 'dest': "可创建状态"},
            {'trigger': 'recive_photo', 'source': "可创建状态", 'dest': "拥有图片"},
            {'trigger': 'recive_bgcolor', 'source': "拥有图片", 'dest': '拥有主背景颜色'},
            {'trigger': 'recive_miancolor', 'source': '拥有主背景颜色', 'dest': '拥有主字体颜色'},
            {'trigger': 'recive_secondcolor', 'source': '拥有主背景颜色', 'dest': '拥有次要颜色'},
            {'trigger': 'recive_secondcolor', 'source': '拥有次要颜色', 'dest': '已经选择是否透明'},
            {'trigger': 'recive_secondcolor', 'source': '已经选择是否透明', 'dest': '未创建状态'}
        ]
        Machine.__init__(self,
                         states=states,
                         transitions=transitions,
                         initial='未创建状态',
                         ordered_transitions=True,
                         # before_state_change='on_exit',
                         # after_state_change='on_enter'
                         )

    def can_run(self):  # 日志
        existing_user: CreateThemeLogo | None = self.session.get(CreateThemeLogo, self.same_primary_key)
        if existing_user:
            clear(existing_user)
            existing_user.flag = 100
        else:
            new_user = CreateThemeLogo(uid=self.same_primary_key, flag=100)
            self.session.add(new_user)

        self.session.commit()



    async def set_bg(self):
        self.existing_user.color_1 = self.query.data
        await self.query.edit_message_caption(caption="嗯！请设置主要字体颜色", reply_markup=self.original_reply_markup)

    async def set_mian_c(self):
        self.existing_user.color_2 = self.query.data
        await self.query.edit_message_caption(caption="好的！请设置 次要 字体颜色", reply_markup=self.original_reply_markup)

    async def set_s_c(self):
        self.existing_user.color_3 = self.query.data
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

        await self.context.bot.send_document(chat_id=self.update.effective_chat.id, document=data, filename=usr_file)
        await self.context.bot.send_message(chat_id=self.update.effective_chat.id, text="这是您的主题文件，亲～")

    def set_clear(self):
        self.existing_user.flag = 0  # 置0
        clear(self.existing_user)

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
        if hasattr(self.update.message, "caption"):
            text = self.update.message.caption
            # if text:
            #     user = self.update.effective_user
            #     boo = mon_per.run(user.id, user.first_name + " " + user.first_name, text, update, context, ban_words,
            #                       logger)
            #     if boo:
            #         return

        existing_user: CreateThemeLogo | None = self.session.get(CreateThemeLogo, same_primary_key)
        if not existing_user:
            return

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

        if existing_user.flag != 4:

            reply_markup = get_kyb(content[0])
            call_message: Message = await self.update.message.reply_photo(content[1],
                                                                          caption="首先，请选择主题的背景颜色",
                                                                          reply_markup=reply_markup)
        else:
            reply_markup = get_desktop_kyb(content[0])
            call_message: Message = await self.update.message.reply_photo(content[1],
                                                                          caption="首先，请选择主题的背景颜色",
                                                                          reply_markup=reply_markup)

        # 如果记录已存在，执行 变更 picpath

        existing_user.callback_id = call_message.message_id
        self.session.commit()

        # pic_file.download("src/Photo/"+file_id+".jpg")


# setup model and state machine

