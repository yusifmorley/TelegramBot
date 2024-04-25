import logging
import os
from logging.handlers import TimedRotatingFileHandler

hs = []
sh = logging.StreamHandler()
if os.environ.get('ENV') == 'dev':
    hs.append(sh)
handler = TimedRotatingFileHandler('log/my_log.log', when='midnight', interval=1, backupCount=7)
hs.append(handler)
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO, handlers=hs)
logger = logging.getLogger("__mian__")


def get_logger():
    return logger


def get_logging():
    return logging
