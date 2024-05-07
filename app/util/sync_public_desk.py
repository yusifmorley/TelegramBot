import os
import shutil

from sqlalchemy.orm import Session

from app.logger.t_log import get_logging
from app.model.models import init_session, ThemeUploadRecord
from app.util.get_preview import get_from

from sqlalchemy import Enum

log = get_logging().getLogger(__name__)
# 主题所在文件夹
orgin_dir = "src/Theme/desktop-theme"
# 公共目录
desk_dir_root = 'src/myserver_bot_public/desk'

session: Session = init_session()

lis = os.listdir(desk_dir_root)
# 数据库信息
desk_ls = session.query(ThemeUploadRecord).filter(ThemeUploadRecord.type == 'tdesktop' and ThemeUploadRecord.strc == 0
                                                  ).all()
# 必要，保存session数据
# 展示的主题列表
desk_list = []
for x in desk_ls:
    desk_list.append(x.t_preview_name)


def flush_dic():
    global lis
    lis = os.listdir(desk_dir_root)


def get_desk_list():
    flush_dic()
    di = dict()
    for x in lis:
        di.update({x: "tdesktop-theme"})
    return di


def sync_dp(directory_path=desk_dir_root):
    global lis
    lis = os.listdir(directory_path)
    for x in desk_list:
        filename = x
        x = x.replace(".tdesktop-theme", "")
        if x in lis:
            log.info("公共目录 %s已经存在", filename)
            pass
        else:
            log.info("公共目录 %s不存在 正在生成", filename)
            target_dir = os.path.join(desk_dir_root, x)  # 当前目录
            os.makedirs(target_dir)
            # 复制文件
            orgin_file = os.path.join(orgin_dir, filename)
            target_file = os.path.join(desk_dir_root, x, filename)
            target_preview_jpg = os.path.join(desk_dir_root, x, x + ".jpg")
            # 生成预览
            with open(orgin_file, "rb") as fd:
                preview_bytes = get_from("desk", filename, fd.read())
                if preview_bytes:
                    shutil.copyfile(orgin_file, target_file)
                    with open(target_preview_jpg, "wb") as pf:
                        pf.write(preview_bytes)
                        log.info("公共目录 %s 生成成功", filename)
                else:
                    log.warn("!!!!!!公共目录 %s 生成失败!!!!", filename)

            lis = os.listdir(desk_dir_root)
    log.info("---公共目录完整---")


def desk_add_by_name(tdesk_name):
    global lis
    x = tdesk_name
    filename = x
    x = x.replace(".tdesktop-theme", "")
    if x in lis:
        log.info("公共目录 %s已经存在", filename)
        pass
    else:
        log.info("公共目录 %s不存在 正在生成", filename)
        target_dir = os.path.join(desk_dir_root, x)  # 当前目录
        os.makedirs(target_dir)
        # 复制文件
        orgin_file = os.path.join(orgin_dir, filename)
        target_file = os.path.join(desk_dir_root, x, filename)
        target_preview_jpg = os.path.join(desk_dir_root, x, x + ".jpg")
        # 生成预览
        with open(orgin_file, "rb") as fd:
            preview_bytes = get_from("desk", filename, fd.read())
            if preview_bytes:
                shutil.copyfile(orgin_file, target_file)
                with open(target_preview_jpg, "wb") as pf:
                    pf.write(preview_bytes)
                    log.info("公共目录 %s 生成成功", filename)
            else:
                log.warn("!!!!!!公共目录 %s 生成失败!!!!", filename)

        lis = os.listdir(desk_dir_root)


def delete(str):
    shutil.rmtree(os.path.join(desk_dir_root, str))
