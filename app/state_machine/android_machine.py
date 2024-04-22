from io import BytesIO

from sqlalchemy.orm import Session
from telegram import Update, Chat, Message
from telegram.ext import ContextTypes
from transitions import Machine, State

from app.model.models import CreateThemeLogo
from app.util.create_atheme import get_attheme_color_pic, get_kyb
from app.util.create_desktop import get_desktop_kyb
from app.util.db_op import clear


class My_Machine(Machine):
    def __init__(self, update: Update, context: ContextTypes.DEFAULT_TYPE, session: Session):
        self.update = update
        self.context = context
        self.session = session
        states = [State("可创建状态", on_enter="send_message"),
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

    def on_enter(self):  # 日志
        self.same_primary_key = self.update.effective_user.id
        existing_user: CreateThemeLogo | None =self.session.get(CreateThemeLogo, self.same_primary_key)
        if existing_user:
            clear(existing_user)
            existing_user.flag = 1
        else:
            new_user = CreateThemeLogo(uid=self.same_primary_key, flag=1)
            self.session.add(new_user)

        self.session.commit()

    def on_exit(self):  # 日志
        print('exited state %s' % self.state)

    def set_bg(self):
        pass

    def set_mian_c(self):
        pass

    def set_s_c(self):
        pass

    def set_can_opc(self):
        pass

    def set_clear(self):
        pass

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
model = My_Machine()

print(model.state)
model.next_state()
print(model.state)
model.next_state()
print(model.state)
model.next_state()
print(model.state)
model.next_state()
print(model.state)
model.next_state()
print(model.state)
model.next_state()
print(model.state)
model.next_state()
