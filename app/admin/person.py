import functools

from app.admin import admin_function


class Person:  # 每个人10句话
    def __init__(self, userid, username, talk_num):
        self.userid = userid
        self.username = username
        self.talk_num = talk_num
        self.talkrecord = []  # 记录用户发言

    def add_contain(self, text):
        flag = self.__addAndCheck__(text)
        self.__contain_size__()
        return flag

    def __eq__(self, other):
        if self.userid == other.userid:
            return True
        else:
            return False

    def __addAndCheck__(self, text):
        if text in self.talkrecord:
            return True
        else:
            self.talkrecord.append(text)
        return False

    def __contain_size__(self):
        if len(self.talkrecord) > self.talk_num:
            del self.talkrecord[0]


def _comp_(x, y):
    return len(x.talkrecord) - len(y.talkrecord)


class MonitorPerson:  # 检测5个人
    def __init__(self, monitor_person_num):  # monitor_person为监听人个数
        self.monitor_person = monitor_person_num
        self.monit_list = []  # 我们依据每个人的 talkrecord个数排序

    def __contain_size__(self): #维持监控队列大小
        if len(self.monit_list) > self.monitor_person:
            self.monit_list.sort(key=functools.cmp_to_key(_comp_))  # 排序
            del self.monit_list[0]  # 删除talk最少的

    def __add_person__(self, person):
        self.monit_list.append(person)
        self.__contain_size__()

    def run(self, usr_id, user_name, text, update, context,banword,logger):

    #判断是否触违禁词
        os = admin_function.deletetxt(banword, text)
        if os:  # 若存在违禁词
            admin_function.blockperson(update, context)
            logger.info(os)  # 记录
            return

        current_person = None
        person = Person(usr_id, user_name, 5)  #
        # if person not in self.monit_list:
        #     self.__add_person__(person)
        for x in self.monit_list:
            if x == person:
                current_person = x
                break
        if current_person is None:
            self.__add_person__(person)
            current_person = person

        if current_person.add_contain(text):  # True则有重复 封禁
            admin_function.blockperson(update, context)  # 封禁
            self.monit_list.remove(current_person)  # 去除封禁person
