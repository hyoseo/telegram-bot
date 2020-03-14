import logging
import os
from logging.handlers import TimedRotatingFileHandler

import coloredlogs


def init(base_name, dir_name='', log_level='INFO'):
    logger = logging.getLogger()
    logger.setLevel(logging.getLevelName(log_level))

    if dir_name:
        os.makedirs(dir_name, exist_ok=True)

    base_file_name = base_name if not dir_name else dir_name + '/' + base_name

    log_fmt = '%(asctime)s.%(msecs)03d %(levelname)9s [%(threadName)s] ' \
              '%(filename)s:%(lineno)s - %(funcName)s : %(message)s'
    log_date_fmt = '%Y-%m-%d %H:%M:%S'

    formatter = logging.Formatter(fmt=log_fmt, datefmt=log_date_fmt)

    file_handler = TimedRotatingFileHandler(base_file_name, when='D', interval=1, backupCount=10)
    file_handler.setFormatter(formatter)

    def namer(default_name):
        default_name += ".log"
        return default_name

    file_handler.namer = namer

    logger.addHandler(file_handler)

    coloredlogs.install(level=logging.getLevelName(log_level), fmt=log_fmt, datefmt=log_date_fmt)
