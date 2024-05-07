import os
import shutil

from sqlalchemy.orm import Session

from app.logger.t_log import get_logging
from app.model.models import init_session, ThemeUploadRecord
from app.util.get_preview import get_from

# 主题所在文件夹
orgin_dir = "src/Theme/android-theme"
# 公共目录
desk_dir_root = 'src/myserver_bot_public/attheme'
log = get_logging().getLogger(__name__)

session: Session = init_session()

attheme_ls = session.query(ThemeUploadRecord).filter(
    ThemeUploadRecord.type == 'android' and ThemeUploadRecord.strc == 0).all()
# 展示的主题列表
attheme_list = []
for x in attheme_ls:
    attheme_list.append(x.t_preview_name)

lis = os.listdir(desk_dir_root)


# 展示的主题列表
# 注意 文件名里最好没有空格
def flush_dic():
    global lis
    lis = os.listdir(desk_dir_root)


def get_attheme_list():
    flush_dic()
    di = dict()
    for x in lis:
        di.update({x: "attheme"})
    return di


def sunc_ap(directory_path=desk_dir_root):
    global lis
    for x in attheme_list:
        filename = x
        x = x.replace(".attheme", "")
        if x in lis:
            log.info("公共目录 %s已经存在", filename)
            pass
        else:
            log.info("公共目录 %s不存在 正在生成", filename)
            target_dir = os.path.join(desk_dir_root, x)  # 当前目录

            # 复制文件
            orgin_file = os.path.join(orgin_dir, filename)
            target_file = os.path.join(desk_dir_root, x, filename)
            target_preview_jpg = os.path.join(desk_dir_root, x, x + ".jpg")

            # 生成预览
            with open(orgin_file, "rb") as fd:
                preview_bytes = get_from("android", filename, fd.read())
                if preview_bytes:
                    os.makedirs(target_dir)
                    shutil.copyfile(orgin_file, target_file)
                    with open(target_preview_jpg, "wb") as pf:
                        pf.write(preview_bytes)
                        log.info("公共目录 %s 生成成功", filename)
                else:
                    log.warn("!!!!!!公共目录 %s 生成失败!!!!", filename)

                lis = os.listdir(desk_dir_root)
    log.info("---公共目录完整---")


def android_add_by_name(aname):
    # aname 是 xxx.attheme
    global lis
    x = aname
    filename = x
    x = x.replace(".attheme", "")
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
            preview_bytes = get_from("android", filename, fd.read())
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
