import os
import shutil

from app.logger.t_log import get_logger
from app.util.get_preview import get_from

log=get_logger()
# 主题所在文件夹
orgin_dir = "src/Theme/desktop-theme"
# 公共目录
desk_dir_root = 'src/myserver_bot_public/desk'

# 展示的主题列表
desk_list = [
             'deepin.tdesktop-theme',
             'NumixDark (1).tdesktop-theme',
             'darkify.tdesktop-theme',
             'YoualiAzul.tdesktop-theme',
             'Sponge Bob.tdesktop-theme',
             'Wood.tdesktop-theme',
             'awesome (7).tdesktop-theme',
             'DarkByNull.tdesktop-theme',
             'null-core-theme-v0.1.tdesktop-theme',
             'S1.tdesktop-theme',
             'CUTIE MOLANG.tdesktop-theme',
             'Landscape Moonlight (3).tdesktop-theme',
             'Desktop Dark Legacy.tdesktop-theme',
             'Digital Night.tdesktop-theme',
             '10 Dark Breeze (v7.3).tdesktop-theme'
             ]

def sync_dp(directory_path=desk_dir_root):
    lis = os.listdir(directory_path)
    for x in desk_list:
        filename = x
        x = x.replace(".tdesktop-theme", "")
        if x in lis:
            log.info("公共目录 %s已经存在",filename)
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
    log.info("---公共目录完整---")


