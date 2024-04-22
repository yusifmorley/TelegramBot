from transitions import Machine, State


class My_Machine(Machine):
    def __init__(self):
        states = [State("可创建状态", on_enter="send_message"),
                  State("拥有图片"),
                  State('拥有主背景颜色'),
                  State('拥有主字体颜色'),
                  State('拥有次要颜色'),
                  State("已经选择是否透明"),
                  State("未创建状态")
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

    # def on_enter(self):  # 日志
    #     print('entered state %s' % self.state)
    #
    # def on_exit(self):  # 日志
    #     print('exited state %s' % self.state)

    def send_message(self):
        print("发送消息")


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