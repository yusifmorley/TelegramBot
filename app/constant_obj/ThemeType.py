from app.util.sync_public_attheme import get_attheme_list
from app.util.sync_public_desk import get_desk_list


class ThemeType(object):
    def __init__(self):
        self.lic = None
        self.flushdict()

    def flushdict(self):
        self.lic = dict(get_desk_list(), **get_attheme_list())

    def get_ty_list(self):
        return self.lic


t_y = ThemeType()

def get_theme_list():
    return t_y
