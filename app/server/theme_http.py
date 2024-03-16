import os
import shutil
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import base64
from sqlalchemy.orm import Session
from app.model.models import init_session, ThemeUploadRecord
from app.logger.t_log import get_logger
from app.util.get_preview import get_from
from app.util.sync_public_attheme import android_add_by_name
from app.util.sync_public_desk import desk_add_by_name

session: Session = init_session()
log = get_logger()


class MyRequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):

        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)

        try:
            # 解析 JSON 数据
            json_data = json.loads(post_data.decode('utf-8'))
            if json_data['path'] == "theme":  # 确定路径
                date = json_data['date']
                if date['hasFile'] == "true":  # 注意 传输的是二进制文件
                    res = None
                    if date['kind'] == '0':  # attheme
                        # 预览图在函数内生成
                        sync(date['name'], 0, 0, base64.b64decode(date['fileBase64']))
                    else:  # tdesktop-theme
                        sync(date['name'], 1, 0, base64.b64decode(date['fileBase64']))

                else:  # 如果是主题名
                    if date['kind'] == '0':  # attheme
                        tup = ThemeUploadRecord(None, date['name'], 'android', 0)
                        session.add(tup)
                        sync(date['name'], 0, 1)
                    else:
                        tup = ThemeUploadRecord(None, date['name'], 'tdesktop', 0)
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
        except json.JSONDecodeError as e:
            # JSON 解析失败的处理
            self.send_response(400)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            error_response = {'status': 'error', 'message': 'Invalid JSON data'}
            self.wfile.write(
                json.dumps(error_response)
                .encode('utf-8'))


def run():
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
        x = x.replace(".attheme", "")
        orgin_dir = "src/Theme/android-theme"
        # 公共目录
        desk_dir_root = 'src/myserver_bot_public/attheme'

        # 创建目标目录
        target_dir = os.path.join(desk_dir_root, x)
        os.makedirs(target_dir)
        # 创建目标目录 创建目标
        target_file = os.path.join(desk_dir_root, x, filename)
        target_preview_jpg = os.path.join(desk_dir_root, x, filename + ".jpg")

        if flag == 0:  # 文件
            preview_bytes = get_from("android", filename, bytes)

            with open(target_file, 'w') as fp:
                fp.write(bytes)  # 写入二进制文件
            with open(target_preview_jpg, 'w') as fj:
                fj.write(preview_bytes)

        else:  # 处理 文件名
            android_add_by_name(filename)

    else:  # tdesktop
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
        target_preview_jpg = os.path.join(desk_dir_root, x, filename + ".jpg")

        if flag == 0:  # 文件
            preview_bytes = get_from("desk", filename, bytes)
            with open(target_file, 'w') as fp:
                fp.write(bytes)  # 写入二进制文件
            with open(target_preview_jpg, 'w') as fj:
                fj.write(preview_bytes)
        else:  # 处理 文件名
            desk_add_by_name(filename)

    target_dir = os.path.join(desk_dir_root, x)  # 当前目录
    os.makedirs(target_dir)
    # 复制文件
    orgin_file = os.path.join(orgin_dir, filename)
    target_file = os.path.join(desk_dir_root, x, filename)
    target_preview_jpg = os.path.join(desk_dir_root, x, filename + ".jpg")

    # 生成预览
    with open(orgin_file, "rb") as fd:
        preview_bytes = get_from("android", filename, fd.read())
        if preview_bytes:
            shutil.copyfile(orgin_file, target_file)
            with open(target_preview_jpg, "wb") as pf:
                pf.write(preview_bytes)
                log.info("公共目录 %s 生成成功", filename)
        else:
            log.warn("!!!!!!公共目录 %s 生成失败!!!!", filename)
