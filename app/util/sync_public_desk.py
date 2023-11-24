import os
import shutil

from get_preview import get_from

# 主题所在文件夹
orgin_dir = "src/Theme/desktop-theme"
# 公共目录
desk_dir_root = 'src/myserver_bot_public/desk'

# 展示的主题列表
desk_list = ['DarkTheme@themesbyAsif.tdesktop-theme',
             'deepin.tdesktop-theme',
             'NumixDark (1).tdesktop-theme',
             'darkify.tdesktop-theme',
             'YoualiAzul.tdesktop-theme',
             'Sponge Bob.tdesktop-theme',
             ]


def print_subdirectories(directory_path=desk_dir_root):
    lis = os.listdir(directory_path)
    for x in desk_list:
        x = x.replace(".tdesktop-theme", "")
        if x in lis:
            pass
        else:
            filename = x
            x = x.replace(".tdesktop-theme", "")
            target_dir = os.path.join(desk_dir_root, x)  # 当前目录
            os.makedirs(target_dir)
            # 复制文件
            orgin_file = os.path.join(orgin_dir, filename)
            target_file = os.path.join(desk_dir_root, x, filename)
            target_preview_jpg = os.path.join(desk_dir_root, x, filename + ".jpg")
            shutil.copyfile(orgin_file, target_file)
            # 生成预览
            with open(orgin_file, "rb") as fd:
                preview_bytes = get_from("desk", filename, fd.read())
                with open(target_preview_jpg, "wb") as pf:
                    pf.write(preview_bytes)



