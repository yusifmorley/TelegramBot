from app.logger import t_log
from app.util.sync_public_attheme import get_attheme_list
from app.util.sync_public_desk import get_desk_list

logger = t_log.get_logging().getLogger(__name__)


class ThemeType(object):
    def __init__(self):
        self.lic = None
        self.flushdict()
        logger.info("字典type字典初始化完成,大小为 {} ".format(str(len(self.lic))))

    def flushdict(self):
        self.lic = dict(get_desk_list(), **get_attheme_list())
        logger.info("刷新type字典完成")
        logger.info("大小为 %s ".format(str(len(self.lic))))

    def get_ty_list(self):
        return self.lic


t_y = ThemeType()


def get_theme_list():
    return t_y
