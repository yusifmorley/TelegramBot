import base64
# with open("PICTURE.jpg","rb") as fio:
#      a=fio.read()
#      print(a)
#
# # with open("PICTURE.jpg","rb")as fi:
#      a=fi.read()
#      print(a)
# with open("HI.attheme-editor","rb")as fil:
#      a=base64.b64encode(fil.read())
#      print(a)

#b'\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x00\x00\x01\x00\x01\x00\x00\xff\xe2\x02(ICC_PROFILE\x00\x01\x01\x00\x00\x02\x18\x00\x00\x00\x00\x02\x10\x00\x00mntrRGB XYZ
# with open("HI.attheme-editor","rb")as go:
#      print(base64.b64decode(go.read()))
# with open("temptheme/Flower.attheme", "rb")as jp:
#     a=jp.readlines()
#     for x in a:
#         if x==b'WPS\n':
#             a=jp.tell()
#
#     fil=jp.read()
#     jp.seek(a,0)
#     print(fil)

a={'chat': {'first_name': 'morley', 'id': 507467074, 'type': 'private', 'last_name': 'dimu', 'username': 'morleydim'}, 'new_chat_members': [], 'group_chat_created': False, 'channel_chat_created': False, 'forward_from': {'id': 1816402746, 'last_name': '🈶招fb发帖员🈶40种技术🈶tlg主题🈶tng二维码美化', 'first_name': '蓝冰霓', 'is_bot': False, 'username': 'lanbingni'}, 'supergroup_chat_created': False, 'forward_date': 1641810136, 'delete_chat_photo': False, 'caption_entities': [], 'entities': [], 'date': 1641811682, 'message_id': 907, 'new_chat_photo': [], 'photo': [{'file_size': 1516, 'width': 60, 'file_unique_id': 'AQAD7q0xGztR4VZ4', 'height': 90, 'file_id': 'AgACAgUAAxkBAAIDi2HcDuJI-xze45Ipx9IiyAABjRj9fwAC7q0xGztR4VZgpEgUzIwg7AEAAwIAA3MAAyME'}, {'file_size': 19947, 'width': 213, 'file_unique_id': 'AQAD7q0xGztR4VZy', 'height': 320, 'file_id': 'AgACAgUAAxkBAAIDi2HcDuJI-xze45Ipx9IiyAABjRj9fwAC7q0xGztR4VZgpEgUzIwg7AEAAwIAA20AAyME'}, {'file_size': 57589, 'width': 500, 'file_unique_id': 'AQAD7q0xGztR4VZ9', 'height': 750, 'file_id': 'AgACAgUAAxkBAAIDi2HcDuJI-xze45Ipx9IiyAABjRj9fwAC7q0xGztR4VZgpEgUzIwg7AEAAwIAA3gAAyME'}], 'from': {'id': 507467074, 'last_name': 'dimu', 'first_name': 'morley', 'is_bot': False, 'username': 'morleydim', 'language_code': 'zh-hans'}}
#
# for x,y in a.items():
#     print(x)
#     print(y)
#     print("\n")

print(a["photo"][2])
