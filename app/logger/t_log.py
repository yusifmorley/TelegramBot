import logging
from logging.handlers import TimedRotatingFileHandler

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)  # »’÷æ
logger = logging.getLogger("__mian__")
handler = TimedRotatingFileHandler('log/my_log.log', when='midnight', interval=1, backupCount=7)
logger.addHandler(handler)


def get_logger():
    return logger
