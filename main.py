import asyncio
import logging
import os

import logger
from exception import EmptyTokenError
from telegram import TelegramBot
from web_server import create_web_server

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

        logging.info(f"TOKEN : {TELEGRAM_TOKEN}")
        logging.info(f"WEB_PORT : {WEB_PORT}")
        logging.info(f"LOG_LEVEL : {LOG_LEVEL}")

        web_server_to_telegram_queue = asyncio.Queue()
        create_web_server(web_server_to_telegram_queue).listen(WEB_PORT)

        logging.info(f"Web server started on {WEB_PORT}")

        TelegramBot(TELEGRAM_TOKEN, web_server_to_telegram_queue).run()

        asyncio.get_event_loop().run_forever()
