# import telegram
# from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, ChatPermissions
# from adminfunction import *
# from telegram.ext import Updater, CallbackContext, CallbackQueryHandler
# import logging
# from getbackground import getbackground
# from mysqlop import createMysql
# from telegram.ext import MessageHandler, Filters
# from telegram.ext import CommandHandler
# from combinate import combinate
# import time
# import ast
#
# myapi = "5738858657:AAFJmjtD5VVi3ed0n9n_5t44chXHVrZLHcM"  # 机器人api
# updater = Updater(token=myapi, use_context=True)
# dispatcher = updater.dispatcher
#
# logging.basicConfig(filename="Log/mylog", format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#                     level=logging.INFO)  # 日志
#
# myarr = {}
# themeFileDowmloaded = False
# themePhontoDownloaded = False
# spuperflag = False  # 为True 时就要 为只接受主题
# Securitydoor = False  # 判断是选择了服务 没有选择就提示发送start 选择服务
# Accpepflag = False  # 一旦开启
# banword = getbanword()
#
# def ceshi(update, context):
#     context.bot.send_message(chat_id=update.effective_chat.id, text="l am alive!")
#
#
# def start(update, context):
#     context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")
#     keyboard = [
#         [
#             InlineKeyboardButton("合并主题和图片", callback_data='1'),
#             InlineKeyboardButton("提取主题背景", callback_data='2'),
#         ],
#
#     ]
#     reply_markup = InlineKeyboardMarkup(keyboard)  # 2
#     global Accpepflag
#     Accpepflag = False
#     update.message.reply_text("请选择服务", reply_markup=reply_markup)
#
#
# def keyboard_callback(update, contetx):
#     query = update.callback_query
#     query.answer()
#     # query.edit_message_text(text=f"Selected option: {query.data} ")
#     global spuperflag
#     global Securitydoor
#     Securitydoor = True  # 安全们开启
#     if query.data == '1':
#         query.edit_message_text(text="请发送您的主题和图片")
#     else:
#         query.edit_message_text(text="请发送您的主题")
#         spuperflag = True
#
#
#
#
# def downloadtheme(update, context):
#     global themeFileDowmloaded
#     global themePhontoDownloaded
#     global spuperflag
#     global Securitydoor
#     if Accpepflag:
#         return
#     if not Securitydoor:  # 安全门判断
#         context.bot.send_message(chat_id=update.effective_chat.id, text="请输入 /start 命令")
#         return
#     file = context.bot.getFile(update.message.document.file_id)
#     file.download("temptheme/" + update.message.document.file_name)
#     context.bot.send_message(chat_id=update.effective_chat.id, text="我已收到主题文件")
#     themeFileDowmloaded = "temptheme/" + update.message.document.file_name
#     if spuperflag:
#         picpath = getbackground(themeFileDowmloaded)
#         context.bot.send_document(chat_id=update.effective_chat.id, document=open(picpath, "rb"))
#         spuperflag = False  # 重置
#         Securitydoor = False  # 重置 服务结束
#         return
#
#     if themeFileDowmloaded and themePhontoDownloaded:
#         newthemepath = combinate(themeFileDowmloaded, themePhontoDownloaded)
#         context.bot.send_document(chat_id=update.effective_chat.id, document=open(newthemepath, "rb"))
#         context.bot.send_message(chat_id=update.effective_chat.id, text="成功！，这是合成的新主题")
#         themeFileDowmloaded = False
#         themePhontoDownloaded = False
#         spuperflag = False  # 重置
#         Securitydoor = False  # 重置 服务结束
#         logging.info("完成合并 来自用户 id " + str(update.effective_user.id) + "用户名：" + update.effective_user.full_name)
#     else:
#         context.bot.send_message(chat_id=update.effective_chat.id, text="我需要一张背景图片")
#
#
# def handlePhoto(update: Update, context: CallbackContext):
#     global themeFileDowmloaded
#     global themePhontoDownloaded
#     global spuperflag
#     global Securitydoor
#     if Accpepflag:
#         print(update)
#         if update.effective_user.id != 507467074:
#             context.bot.send_message(chat_id=update.effective_chat.id, text="您非私人用户")
#             context.bot.send_message(chat_id=update.effective_chat.id, text=str(update.effective_user.id))
#             logging.warning("非法的使用 用户id为 " + str(update.effective_user.id))
#             return
#         tim = time.localtime()
#         timstr = time.strftime("%Y-%m-%d-%H-%M-%S", tim)
#         file = context.bot.getFile(update.message.photo[2]['file_id'])
#         photoPath = "Photo/" + timstr + ".jpg"
#         file.download(photoPath)
#         context.bot.send_message(chat_id=update.effective_chat.id, text="图片已下载")
#         logging.info("下载完成！ 图片文件 id ：" + str(file))
#         return
#
#     if not Securitydoor:
#         # context.bot.send_message(chat_id=update.effective_chat.id, text="请输入 /start 命令")
#         return
#     if spuperflag:
#         context.bot.send_message(chat_id=update.effective_chat.id, text="不需要图片 ")
#         return
#     tim = time.localtime()
#     timstr = time.strftime("%Y-%m-%d-%H-%M-%S", tim)
#     context.bot.send_message(chat_id=update.effective_chat.id, text="这确实是一张图片！")
#     file = context.bot.getFile(update.message.photo[2]['file_id'])
#     photoPath = "tempthemephoto/" + timstr + ".jpg"
#     file.download(photoPath)
#     context.bot.send_message(chat_id=update.effective_chat.id, text="图片已下载")  # 下载图片
#     themePhontoDownloaded = "tempthemephoto/" + timstr + ".jpg"
#     if themeFileDowmloaded and themePhontoDownloaded:
#         newthemepath = combinate(themeFileDowmloaded, themePhontoDownloaded)
#         context.bot.send_document(chat_id=update.effective_chat.id, document=open(newthemepath, "rb"))
#         context.bot.send_message(chat_id=update.effective_chat.id, text="成功！，这是合成的新主题")
#         # alls = getPreview(newthemepath)  # 2p
#         # channelandthemepara = {"themeName": newthemepath[newthemepath.find("/"):],
#         #                        "file": newthemepath}
#         # alls = dict(alls, **channelandthemepara)
#         # createMysql(alls)
#         # print('success!')
#
#         themeFileDowmloaded = False
#         themePhontoDownloaded = False
#         spuperflag = False  # 重置
#         Securitydoor = False  # 重置 服务结束
#         logging.info("完成合并 来自用户 id " + str(update.effective_user.id) + "用户名：" + update.effective_user.full_name)
#     else:
#         context.bot.send_message(chat_id=update.effective_chat.id, text="我需要一个主题文件")
#
#
# def adminhanderex(update, context):  # 管理员
#     if Accpepflag:
#         if update.effective_user.id != 507467074:
#             context.bot.send_message(chat_id=update.effective_chat.id, text="您非私人用户")
#             context.bot.send_message(chat_id=update.effective_chat.id, text=str(update.effective_user.id))
#             return
#         with open("Text/text","a") as tx:
#             tx.write(update.effective_message.text+"\n")
#             context.bot.send_message(chat_id=update.effective_chat.id, text="文本写入完成")
#
#     text = update.effective_message.text
#     os = deletetxt(text, banword)
#     if os:
#         context.bot.delete_message(chat_id=update.effective_chat.id, message_id=update.effective_message.message_id)
#         context.bot.restrict_chat_member(chat_id=update.effective_chat.id,
#                                          user_id=update.effective_user.id,
#                                          until_date=259200,
#                                          permissions=ChatPermissions(can_send_messages=False,
#                                                                      can_send_media_messages=False))
#         textlog = "用户id :" + str(
#             update.effective_user.id) + " 用户名 :" + update.effective_user.full_name + "已被封禁3天，由于触发 关键词 " + os
#         context.bot.send_message(chat_id=update.effective_chat.id, text=textlog)
#         logging.info(textlog)
#     else:
#         pass
#
#
# def welcome(update, context):
#     context.bot.delete_message(chat_id=update.effective_chat.id, message_id=update.effective_message.message_id)
#
#
# def accept(update, context):
#     global Accpepflag
#     Accpepflag = True
#     context.bot.send_message(chat_id=update.effective_chat.id, text="开启接收模式！")
#
#
# def videohandle(update, context):
#     print(update)
#     if Accpepflag:
#         if update.effective_user.id != 507467074:
#             context.bot.send_message(chat_id=update.effective_chat.id, text="您非私人用户")
#             context.bot.send_message(chat_id=update.effective_chat.id, text=str(update.effective_user.id))
#             return
#         filename = ""
#         # if update.message.video.file_name:
#         #     filename = update.message.video.file_name
#         # elif update.message.caption:
#         #     filename = update.message.caption
#         # else:
#         #     tim = time.localtime()
#         #     timstr = time.strftime("%Y-%m-%d-%H-%M-%S", tim)
#         #     filename = timstr
#         # if len(filename) > 15:
#         #     filename = filename[:15]
#         # if update.message.video.file_size > 20000000:
#         with open("Videoid/videoid", "a") as ws:
#             ws.write(
#                 update.message.video.to_json() + "\n")
#             context.bot.send_message(chat_id=update.effective_chat.id, text="文件已经下载")
#             logging.info("写入完成！ 视频文件 id ：" + str(update.message.video))
#         # else:
#         #     with open("Videoid/videoid", "a") as ws:
#         #         ws.write(
#         #             update.message.video.to_json() + "\n")
#         #     logging.info("写入完成！ 视频文件 id ：" + str(update.message.video))
#         #     file = context.bot.getFile(update.message.video.file_id)
#         #     file.download("MyFile/Video/" + filename)
#         #     context.bot.send_message(chat_id=update.effective_chat.id, text="文件已经下载")
#         #     logging.info("下载完成！ 视频文件 id ：" + str(file))
#
#
# def getvideo(update, context):
#     if Accpepflag:
#         if update.effective_user.id != 507467074:
#             context.bot.send_message(chat_id=update.effective_chat.id, text="您非私人用户")
#             context.bot.send_message(chat_id=update.effective_chat.id, text=str(update.effective_user.id))
#             return
#         with open("Videoid/videoid", "r") as dep:
#             ob = dep.readline()
#             context.bot.send_video(chat_id=update.effective_chat.id,
#                                    video=telegram.Video.de_json(data=ast.literal_eval(ob), bot=context.bot))
#
#
# def animationhander(update, context):
#     if Accpepflag:
#         if update.effective_user.id != 507467074:
#             context.bot.send_message(chat_id=update.effective_chat.id, text="您非私人用户")
#             context.bot.send_message(chat_id=update.effective_chat.id, text=str(update.effective_user.id))
#             return
#         tim = time.localtime()
#         timstr = time.strftime("%Y-%m-%d-%H-%M-%S", tim)
#         file = context.bot.getFile(update.message.animation.file_id)
#         animationPath = "Photo/" + timstr + ".gif"
#         file.download(animationPath)
#         context.bot.send_message(chat_id=update.effective_chat.id, text="文件已下载")
#
#
# def reset(update, context):
#     global themeFileDowmloaded
#     global themePhontoDownloaded
#     global spuperflag
#     global Securitydoor
#     global Accpepflag
#     themeFileDowmloaded = False
#     themePhontoDownloaded = False
#     spuperflag = False  # 为True 时就要 为只接受主题
#     Securitydoor = False  # 判断是选择了服务 没有选择就提示发送start 选择服务
#     Accpepflag = False  # 一旦开启
#     context.bot.send_message(chat_id=update.effective_chat.id, text="重置完成")
#
#
# combins = CommandHandler('start', start)
# dispatcher.add_handler(combins)
#
# combinss = CommandHandler('ceshi', ceshi)
# dispatcher.add_handler(combinss)
#
# combinsss = CommandHandler('accept', accept)
# dispatcher.add_handler(combinsss)
#
# combinssss = CommandHandler('get', getvideo)
# dispatcher.add_handler(combinssss)
#
# combinsssss = CommandHandler('reset', reset)
# dispatcher.add_handler(combinsssss)
#
#
#
# accpet_handler = MessageHandler(Filters.video, videohandle)
# dispatcher.add_handler(accpet_handler)
#
# unknown_handler = MessageHandler(Filters.photo, handlePhoto)
# dispatcher.add_handler(unknown_handler)
#
# animation = MessageHandler(Filters.animation, animationhander)
# dispatcher.add_handler(animation)
#
# checkatthem = MessageHandler(Filters.document.file_extension("attheme"), downloadtheme)
# dispatcher.add_handler(checkatthem)
#
# adminhander = MessageHandler(Filters.text, adminhanderex)
# dispatcher.add_handler(adminhander)
#
# memberwelcom = MessageHandler(Filters.status_update.new_chat_members, welcome)
# dispatcher.add_handler(memberwelcom)
#
# updater.dispatcher.add_handler(CallbackQueryHandler(keyboard_callback))
# updater.start_polling()
