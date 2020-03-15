import asyncio
import json
import logging

import tornado.web
import tornado.ioloop

from message import TelegramMessage


class MessageHandler(tornado.web.RequestHandler):
    def initialize(self, to_telegram_queue: asyncio.Queue):
        self._to_telegram_queue = to_telegram_queue

    async def post(self):
        self.set_header("Content-Type", "application/json")
        msg = json.loads(self.request.body)

        try:
            telegram_message = TelegramMessage(msg)
            print(str(telegram_message))
        except KeyError as e:
            logging.exception(f"the key {e} field not exist in message")
            self.set_status(400)
            self.write(json.dumps(
                {'error_code': 10, 'error_message': f"{e} field not exist in message", 'result': None}))
            return
        except Exception as e:
            logging.exception(f"message parse error {e}")
            self.set_status(400)
            self.write(json.dumps(
                {'error_code': 10, 'error_message': 'invalid message format', 'result': None}))
            return

        self._to_telegram_queue.put_nowait(telegram_message)

        self.write(json.dumps({'error_code': 0, 'error_message': None, 'result': {}}))


class TestHandler(tornado.web.RequestHandler):
    async def post(self):
        print(self.request.full_url())
        print('chat_id :', self.request.query_arguments)

    async def get(self):
        print(self.request.full_url())
        print('chat_id :', self.request.query_arguments)


def create_web_server(to_telegram_queue: asyncio.Queue):
    return tornado.web.Application([
        (r"/messages", MessageHandler, {'to_telegram_queue': to_telegram_queue}),
        (r"/test", TestHandler),
    ])
