import logging

from emoji import emojize
from telepot import exception
from telepot.namedtuple import InlineKeyboardMarkup


class BotHelper:
    def __init__(self, bot):
        self.bot = bot

    async def send(self, chat_id, text, keyboard_buttons=None, parse_mode='Markdown'):
        try:
            if keyboard_buttons:
                result = await self.bot.sendMessage(chat_id=chat_id, text=emojize(text, use_aliases=True),
                                                    parse_mode=parse_mode,
                                                    reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard_buttons))
            else:
                result = await self.bot.sendMessage(chat_id=chat_id, text=emojize(text, use_aliases=True),
                                                    parse_mode=parse_mode)
            return result['message_id']
        except exception.TelegramError as ex:
            logging.exception(ex)

        return None

    async def edit(self, chat_id, msg_id, text, keyboard_buttons=None):
        try:
            if keyboard_buttons:
                await self.bot.editMessageText((chat_id, msg_id), text=emojize(text, use_aliases=True),
                                               parse_mode='Markdown',
                                               reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard_buttons))
            else:
                await self.bot.editMessageText((chat_id, msg_id), text=emojize(text, use_aliases=True),
                                               parse_mode='Markdown')
        except exception.TelegramError as ex:
            logging.exception(f"{msg_id} {ex}")

    async def delete(self, chat_id, msg_id):
        try:
            await self.bot.deleteMessage((chat_id, msg_id))
        except exception.TelegramError as ex:
            logging.exception(f"{msg_id} {ex}")
