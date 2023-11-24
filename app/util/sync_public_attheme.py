import os
import shutil

from get_preview import get_from

# 主题所在文件夹
orgin_dir = "src/Theme/android-theme"
# 公共目录
desk_dir_root = 'src/myserver_bot_public/attheme'

# 展示的主题列表
attheme_list = [
             ]


def print_subdirectories(directory_path=desk_dir_root):
    lis = os.listdir(directory_path)
    for x in attheme_list:
        x = x.replace(".attheme", "")
        if x in lis:
            pass
        else:
            filename = x
            x = x.replace(".attheme", "")
            target_dir = os.path.join(desk_dir_root, x)  # 当前目录
            os.makedirs(target_dir)
            # 复制文件
            orgin_file = os.path.join(orgin_dir, filename)
            target_file = os.path.join(desk_dir_root, x, filename)
            target_preview_jpg = os.path.join(desk_dir_root, x, filename + ".jpg")
            shutil.copyfile(orgin_file, target_file)
            # 生成预览
            with open(orgin_file, "rb") as fd:
                preview_bytes = get_from("attheme", filename, fd.read())
                with open(target_preview_jpg, "wb") as pf:
                    pf.write(preview_bytes)


