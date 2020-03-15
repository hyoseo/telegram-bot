import asyncio
import json
import tornado.web
import tornado.ioloop


class MessageHandler(tornado.web.RequestHandler):
    def initialize(self, to_telegram_queue: asyncio.Queue):
        self._to_telegram_queue = to_telegram_queue

    async def post(self):
        self.set_header("Content-Type", "application/json")
        msg = json.loads(self.request.body)

        if 'chat_id' not in msg:
            self.set_status(400)
            self.write(json.dumps(
                {'error_code': 10, 'error_message': 'chat_id field dose not exist in request body', 'result': None}))
            return

        if 'text' not in msg:
            self.set_status(400)
            self.write(json.dumps(
                {'error_code': 10, 'error_message': 'text field dose not exist in request body', 'result': None}))
            return

        self._to_telegram_queue.put_nowait(msg)

        self.write(json.dumps({'error_code': 0, 'error_message': None, 'result': {}}))


def create_web_server(to_telegram_queue: asyncio.Queue):
    return tornado.web.Application([
        (r"/messages", MessageHandler, {'to_telegram_queue': to_telegram_queue}),
    ])
