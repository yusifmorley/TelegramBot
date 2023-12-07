import os
import shutil

from app.logger.t_log import get_logger
from app.util.get_preview import get_from

# 主题所在文件夹
orgin_dir = "src/Theme/android-theme"
# 公共目录
desk_dir_root = 'src/myserver_bot_public/attheme'
log = get_logger()
#展示的主题列表
#注意 文件名里最好没有空格
attheme_list = ['Carbon_v1.3.attheme',
                'Bright Green by @arsLan4k1390 (2).attheme',
                'Patina on Mauve by @ThemerBot.attheme',
                'pastae purbae (1).attheme',
                'Sy5XO by @CreateAtthemeBot.attheme',
                'RootLinux-Halloween-V8.attheme',
                'Dark_Mild Blue+Fiery Red.attheme',
                'Kenyan Copper on Shark by @TempThemerBot.attheme',
                'Chelsea.attheme'
                ]


def sunc_ap(directory_path=desk_dir_root):
    lis = os.listdir(directory_path)
    for x in attheme_list:
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
    log.info("---公共目录完整---")
