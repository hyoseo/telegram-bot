import asyncio
import logging

import telepot.aio
import telepot.aio.helper
# from telegram.btn_handler import btn_pressed_handlers
# from telegram.chat_helper import ChatHelper
from telepot.aio.delegate import include_callback_query_chat_id, pave_event_space, per_chat_id, create_open
from telepot.aio.loop import MessageLoop

from bot_helper import BotHelper


class TelegramHandler:
    def __init__(self):
        self._bot_helper: BotHelper = None

    def set_bot(self, bot):
        self._bot_helper = BotHelper(bot)

    async def on_chat_message(self, msg):
        content_type, chat_type, chat_id = telepot.glance(msg)
        text = msg['text']

        if text == '/getchatid':
            await self._bot_helper.send(chat_id, f"your chat id is '{chat_id}'")
        else:
            await self._bot_helper.send(chat_id,
                                        "You can control me by sending these commands:\n\n"
                                        "/getchatid - get my chat id")

    async def on_callback_query(self, msg):
        query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')

        btn_class_name = query_data
        btn_extra_name = None
        btn_extra_name_start_pos = query_data.rfind('?')

        if btn_extra_name_start_pos != -1:
            btn_class_name = query_data[:btn_extra_name_start_pos]
            btn_extra_name = query_data[btn_extra_name_start_pos + 1:]

        # if btn_class_name in btn_pressed_handlers:
        #     try:
        #         pass
        #         await btn_pressed_handlers[btn_class_name].on_pressed(
        #             self._bot_helper,
        #             self._chat_helper,
        #             btn_extra_name,
        #             self._broker_msg_processor,
        #             self._order_id_to_msg_id,
        #             telepot.origin_identifier(msg)[1]
        #         )
        #     except Exception as e:
        #         await self._bot_helper.send(f":heavy_exclamation_mark:{btn_class_name} on_pressed Exception : {str(e)}",
        #                                     parse_mode=None)
        #         logging.exception(btn_class_name)
        # else:
        #     await self._bot_helper.send("해당 버튼에 대한 처리가 존재하지 않습니다.")

    async def on_web_server_message(self, msg):
        await self._bot_helper.send(msg['chat_id'], msg['text'], parse_mode=None)


class MyChatHandler(telepot.aio.helper.ChatHandler):
    def __init__(self, seed_tuple, telegram_handler, **kwargs):
        super(MyChatHandler, self).__init__(seed_tuple, **kwargs)
        self._telegram_handler = telegram_handler

    async def on_chat_message(self, msg):
        await self._telegram_handler.on_chat_message(msg)

    async def on_callback_query(self, msg):
        await self._telegram_handler.on_callback_query(msg)

    def on_close(self, ex):
        pass


class TelegramBot:
    def __init__(self, token, from_web_server_queue):
        super().__init__()

        self._from_web_server_queue = from_web_server_queue

        self._telegram_handler = TelegramHandler()

        self.bot = telepot.aio.DelegatorBot(token, [
            include_callback_query_chat_id(pave_event_space())(
                per_chat_id(), create_open, MyChatHandler, self._telegram_handler, timeout=10)
        ])

        self._telegram_handler.set_bot(self.bot)

    async def process_web_server_queue(self):
        logging.info(f"process_web_server_queue started.")

        while True:
            msg = await self._from_web_server_queue.get()
            await self._telegram_handler.on_web_server_message(msg)

    def run(self):
        loop = asyncio.get_event_loop()
        loop.create_task(MessageLoop(self.bot).run_forever())
        loop.create_task(self.process_web_server_queue())
