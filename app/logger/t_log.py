import logging
import os
from logging.handlers import TimedRotatingFileHandler

from deprecated import deprecated
log_p=['info','warn','error']

# 创建日志目录
log_directory = "log"
for x in log_p:
    o_p = os.path.join(log_directory,x)
    if not os.path.exists(o_p):
        os.makedirs(o_p)

# 创建日志处理器
handlers = []

# 控制台处理器
sh = logging.StreamHandler()
if os.environ.get('ENV') == 'dev':
    handlers.append(sh)

# 定时轮换文件处理器
info_handler = TimedRotatingFileHandler(os.path.join(log_directory,'info', 'info.log'), when='midnight', interval=1, backupCount=7)
info_handler.setLevel(logging.INFO)

warn_handler = TimedRotatingFileHandler(os.path.join(log_directory,'warn', 'warn.log'), when='midnight', interval=1, backupCount=7)
warn_handler.setLevel(logging.WARNING)

error_handler = TimedRotatingFileHandler(os.path.join(log_directory,'error', 'error.log'), when='midnight', interval=1, backupCount=7)
error_handler.setLevel(logging.ERROR)

handlers.extend([info_handler, warn_handler, error_handler])

# 创建格式器
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# 将格式器添加到处理器
for handler in handlers:
    handler.setFormatter(formatter)

# 配置基本的日志记录系统
logging.basicConfig(level=logging.DEBUG, handlers=handlers)
logger = logging.getLogger(__name__)

@deprecated
def get_logger():
    return logger

def get_logging():
    return logging

