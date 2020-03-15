import asyncio
import logging

import telepot.aio
import telepot.aio.helper
from aiohttp import ClientSession
from emoji import emojize
from telepot.aio.delegate import include_callback_query_chat_id, pave_event_space, per_chat_id, create_open
from telepot.aio.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardButton

from bot_helper import BotHelper
from message import TelegramMessage


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

        try:
            async with ClientSession() as session:
                # http method 선택할 수 있게 처리하자.
                async with session.request('GET', query_data, params={'chat_id': from_id}) as response:
                    if response.status != 200:
                        await self._bot_helper.send(from_id,
                                                    f":heavy_exclamation_mark:run callback_url failed {response.reason}")
        except Exception as e:
            logging.exception(e)

    async def on_web_server_message(self, msg: TelegramMessage):
        keyboard_buttons = []
        line_button = []
        for button in msg.buttons:
            line_button.append(InlineKeyboardButton(text=emojize(button.text, use_aliases=True),
                                                    callback_data=button.callback_url))

            if len(line_button) == 2 or not button.is_horizontal:
                keyboard_buttons.append(line_button)
                line_button = []

        if line_button:
            keyboard_buttons.append(line_button)

        await self._bot_helper.send(msg.chat_id, msg.text, keyboard_buttons=keyboard_buttons, parse_mode=msg.parse_mode)


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
