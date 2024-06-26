import asyncio
from io import BytesIO

from PIL import Image
from sqlalchemy.orm import Session
from telegram import Update, Chat, Message, File
from telegram.ext import ContextTypes
from transitions.extensions import AsyncMachine
import app.util.file_name_gen as f_n
import app.util.get_time as g_t
from app.logger import t_log
from app.model.models import CreateThemeLogo
from app.util.create_atheme import get_attheme_color_pic, get_kyb, get_transparent_ky, get_attheme
from app.util.create_desktop import get_desktop_kyb
from app.util.db_op import clear

logger = t_log.get_logging().getLogger(__name__)


class AsyncModel:

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
        self.user_id = update.effective_chat.id
        if hasattr(update, "query"):
            self.original_reply_markup = self.query.message.reply_markup
        logger.warning(f"当前 flag为 {flag}")
        logger.info("当前状态为{}".format(sta[self.flag]))

    async def random_theme(self, query, existing_user):
        color_arr = query.data.split(",")
        existing_user.color_1 = color_arr[0]
        existing_user.color_2 = color_arr[1]
        existing_user.color_3 = color_arr[2]
        reply_markup = get_transparent_ky()
        await query.edit_message_caption(caption="嗯嗯！您可以继续选择", reply_markup=reply_markup)
        existing_user.flag = 5
        self.session.commit()
        return

    async def can_run(self):  # 日志
        # logger.info("运行了")
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
                                              reply_markup=self.query.message.reply_markup)

    async def set_mian_c(self):
        self.existing_user.color_2 = self.query.data
        self.existing_user.flag = self.existing_user.flag + 1
        await self.query.edit_message_caption(caption="好的！请设置 次要 字体颜色",
                                              reply_markup=self.query.message.reply_markup)

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

        if self.query.data == "tran":
            data = get_attheme(by, lis,True)
        # elif self.query.data == "tran":
        else:
            data = get_attheme(by, lis, )

        usr_file = f_n.gen_name(g_t.get_now()) + ".attheme"

        await self.context.bot.send_document(chat_id=self.update.effective_chat.id, document=data, filename=usr_file)
        await self.context.bot.send_message(chat_id=self.update.effective_chat.id, text="这是您的主题文件，亲～。更多安卓主题请关注我们的频道 https://t.me/moleydimu")
        self.existing_user.flag = self.existing_user.flag + 1
        self.session.commit()

    async def set_clear(self):
        clear(self.existing_user)  # 清除置空
        self.session.commit()


    async def handle_document(self, doucment_pt):
        logger.debug("进入 handle_document")
        existing_user: CreateThemeLogo | None = self.session.get(CreateThemeLogo, self.same_primary_key)
        logger.debug(f"得到变量 {doucment_pt}")
        fd = open(doucment_pt, 'rb')
        pic_bytes = fd.read()
        fd.close()
        existing_user.pic_path = doucment_pt
        logger.info("正在读取 document 大小为{}比特".format(len(pic_bytes)))
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
        # logger.warning(f"call message id 为 {call_message.id}")
        self.session.commit()

    async def handle_photo(self):
        # 键名 是chat id
        existing_user: CreateThemeLogo | None = self.session.get(CreateThemeLogo, self.same_primary_key)

        pid = self.update.effective_message.photo[-1].file_id  # 最后一个是完整图片
        pic_file = await self.context.bot.get_file(pid)
        user_id = self.update.effective_chat.id
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


transition = [dict(trigger='recive_command', source="未创建状态", dest="可创建状态", before="can_run"),
              dict(trigger='recive_photo', source="可创建状态", dest="拥有图片", before="handle_photo"),
              dict(trigger='recive_document', source="可创建状态", dest="拥有图片", before="handle_document"),

              dict(trigger='recive_random_color', source="*", dest="拥有次要颜色", before="random_theme"),

              dict(trigger='recive_color', source="拥有图片", dest="拥有主背景颜色", before="set_bg"),
              dict(trigger='recive_color', source='拥有主背景颜色', dest="拥有主字体颜色", before="set_mian_c"),
              dict(trigger='recive_color', source='拥有主字体颜色', dest="拥有次要颜色", before="set_s_c"),
              dict(trigger='recive_color', source='拥有次要颜色', dest="已经选择是否透明", before="set_can_opc",
                   after="set_clear"  # 清空

                   )
              ]
sta = [
    "未创建状态",
    "可创建状态",
    "拥有图片",
    '拥有主背景颜色',
    '拥有主字体颜色',
    '拥有次要颜色',
    "已经选择是否透明"
]


def get_modle(update, context, session, flag):
    model = AsyncModel(update, context, session, flag)
    machine = AsyncMachine(model, states=sta,
                           transitions=transition,
                           initial=sta[flag])

    return model
