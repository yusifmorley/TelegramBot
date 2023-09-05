import functools

from app.admin import admin_function

class MonitorPerson:
    def __init__(self, monitor_person_num):  # monitor_person为监听人个数
        self.monitor_person = monitor_person_num
        self.text_list = []

    def __contain_list__(self,text):
        if len(self.text_list)>self.monitor_person:
            del  self.text_list[0]  #删除首个元素
        self.text_list.append(text)

    def run(self, usr_id, user_name, text, update, context,banword,logger):
        #对@进行特殊处理
        if '@' in text and "/" not in text:
            admin_function.blockperson(update, context,"@")
        #防止误删来自频道的消息
        if  "addtheme" in text:
            return

    #判断是否触违禁词
        os = admin_function.deletetxt(banword, text)
        if os:  # 若存在违禁词
            admin_function.blockperson(update, context,os)
            logger.info(os)  # 记录

            return
    #判断text 是否有重复
        if text in self.text_list:
            admin_function.blockperson(update,context,"重复")
        else:
            self.__contain_list__(text)

