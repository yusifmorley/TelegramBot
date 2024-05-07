import os
import shutil
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import base64
from sqlalchemy.orm import Session

from app.constant_obj.ThemeType import get_theme_list
from app.model.models import init_session, ThemeUploadRecord
from app.logger.t_log import get_logging
from app.util.get_preview import get_from
from app.util.sync_public_attheme import android_add_by_name, delete
from app.util.sync_public_desk import desk_add_by_name, delete as d_delete

session: Session = init_session()
log = get_logging().getLogger(__name__)
ty_lis = get_theme_list()


class MyRequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):

        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)

        try:
            # 解析 JSON 数据
            json_data = json.loads(post_data.decode('utf-8'))
            if json_data['path'] == "delete":  # 确定路径
                date = json.loads(json_data['date'])
                name: str = date['name']
                le = name.split("/")
                if date['kind'] == '0':  # attheme
                    session.query(ThemeUploadRecord).filter(ThemeUploadRecord.t_preview_name == le[1]).delete()
                    delete(le[0])
                else:
                    session.query(ThemeUploadRecord).filter(ThemeUploadRecord.t_preview_name == le[1]).delete()
                    d_delete(le[0])
                session.commit()
            if json_data['path'] == "theme":  # 确定路径
                date = json.loads(json_data['date'])
                if date['hasFile']:  # 注意 传输的是二进制文件
                    res = None
                    if date['kind'] == '0':  # attheme
                        tup = ThemeUploadRecord(id=None, t_preview_name=date['name'], type='android', strc=1)
                        session.add(tup)
                        # 预览图在函数内生成
                        sync(date['name'], 0, 0, base64.b64decode(date['fileBase64']))
                    else:  # tdesktop-theme
                        tup = ThemeUploadRecord(id=None, t_preview_name=date['name'], type='tdesktop', strc=1)
                        session.add(tup)
                        sync(date['name'], 1, 0, base64.b64decode(date['fileBase64']))
                    session.commit()
                else:  # 如果是主题名
                    #  删除

                    if date['kind'] == '0':  # attheme
                        tup = ThemeUploadRecord(id=None, t_preview_name=date['name'], type='android', strc=0)
                        session.add(tup)
                        sync(date['name'], 0, 1)
                    else:
                        tup = ThemeUploadRecord(id=None, t_preview_name=date['name'], type='tdesktop', strc=0)
                        session.add(tup)
                        sync(date['name'], 1, 1)
                    session.commit()
            # 处理 JSON 数据
            # 这里可以根据需要执行你的逻辑
            # 返回响应
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {'status': 'success', 'message': 'JSON data received successfully'}
            self.wfile.write(json.dumps(response)
                             .encode('utf-8'))

            # 刷新 type字典
            ty_lis.flushdict()
        except json.JSONDecodeError as e:
            log.error("json 解析错误 : %s".format(e))
            # JSON 解析失败的处理
            self.send_response(400)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            error_response = {'status': 'error', 'message': 'Invalid JSON data'}
            self.wfile.write(
                json.dumps(error_response)
                .encode('utf-8'))


def run():
    log.info("Starting server...")
    server_address = ('127.0.0.1', 7950)
    httpd = HTTPServer(server_address, MyRequestHandler)
    # log.info('Starting server on port 7950...')
    httpd.serve_forever()


def sync(filename, type, flag, bytes=None):  # 生成合适 的mybackstage目录
    # name 文件名
    # type 文件种类 安卓还是桌面
    # flag 标记是处理 二进制文件 还是 文件名
    # filename 是 xxx.ss
    # x 是 xxx
    # bytes 文件的二进制
    x = filename
    if type == 0:  # attheme
        if flag == 0:  # 文件
            x = x.replace(".attheme", "")
            orgin_dir = "src/Theme/android-theme"
            # 公共目录
            desk_dir_root = 'src/myserver_bot_public/attheme'

            # 创建目标目录
            target_dir = os.path.join(desk_dir_root, x)
            os.makedirs(target_dir)
            # 创建目标目录 创建目标
            target_file = os.path.join(desk_dir_root, x, filename)
            target_preview_jpg = os.path.join(desk_dir_root, x, x + ".jpg")

            preview_bytes = get_from("android", filename, bytes)
            if preview_bytes is None:
                log.error("生成预览失败")
            with open(target_file, 'wb') as fp:
                fp.write(bytes)  # 写入二进制文件

            with open(target_preview_jpg, 'wb') as fj:
                fj.write(preview_bytes)


        else:  # 处理 文件名
            android_add_by_name(filename)

    else:  # tdesktop

        if flag == 0:  # 文件
            x = x.replace(".tdesktop-theme", "")
            # 主题所在文件夹
            orgin_dir = "src/Theme/desktop-theme"
            # 公共目录
            desk_dir_root = 'src/myserver_bot_public/desk'
            # 创建目标目录
            target_dir = os.path.join(desk_dir_root, x)
            os.makedirs(target_dir)
            # 创建目标目录 创建目标
            target_file = os.path.join(desk_dir_root, x, filename)
            target_preview_jpg = os.path.join(desk_dir_root, x, x + ".jpg")
            preview_bytes = get_from("desk", filename, bytes)
            if preview_bytes is None:
                log.error("生成预览失败")
            with open(target_file, 'wb') as fp:
                fp.write(bytes)  # 写入二进制文件

            with open(target_preview_jpg, 'wb') as fj:
                fj.write(preview_bytes)

        else:  # 处理 文件名
            desk_add_by_name(filename)
