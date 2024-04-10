import logging
from logging.handlers import TimedRotatingFileHandler

handler = TimedRotatingFileHandler('log/my_log.log', when='midnight', interval=1, backupCount=7)
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO, handlers=[handler])  # »’÷æ
logger = logging.getLogger("__mian__")


# “≈¡Ù¥˙¬Î
def get_logger():
    return logger


def get_logging():
    return logging
