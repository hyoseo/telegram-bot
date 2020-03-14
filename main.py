import logging
import os

import logger
from exception import EmptyTokenError

if __name__ == "__main__":
    pid = str(os.getpid())
    with open('application.pid', 'w') as f:
        f.write(pid)

    TELEGRAM_TOKEN = os.environ.get('TOKEN')
    WEB_PORT = os.environ.get('WEB_PORT', 8080)
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')

    if not TELEGRAM_TOKEN:
        raise EmptyTokenError()
    else:
        logger.init("telegram-bot.log", dir_name="logs", log_level=LOG_LEVEL)

        logging.info(f"application pid : {pid}")

        logging.warning("token is " + TELEGRAM_TOKEN)
        logging.debug("web_port is " + WEB_PORT)
        logging.info("this log level is " + LOG_LEVEL)



