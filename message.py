class TelegramButton:
    def __init__(self, text, callback_url, callback_http_method='GET', is_horizontal=False):
        self._text = text
        self._callback_url = callback_url
        self._callback_http_method = callback_http_method
        self._is_horizontal = is_horizontal

    @property
    def text(self):
        return self._text

    @property
    def callback_url(self):
        return self._callback_url

    @property
    def callback_http_method(self):
        return self._callback_http_method

    @property
    def is_horizontal(self):
        return self._is_horizontal


class TelegramMessage:
    def __init__(self, msg: dict):
        self._chat_id = msg['chat_id']
        self._text = msg['text']
        self._parse_mode = msg['parse_mode'] if 'parse_mode' in msg else None
        self._buttons = []

        if 'buttons' in msg:
            for btn in msg['buttons']:
                self._buttons.append(
                    TelegramButton(btn['text'],
                                   btn['callback_url'],
                                   callback_http_method=btn['callback_http_method']
                                   if 'callback_http_method' in btn else 'GET',
                                   is_horizontal=btn['is_horizontal'] if 'is_horizontal' in btn else False))

    @property
    def chat_id(self):
        return self._chat_id

    @property
    def text(self):
        return self._text

    @property
    def parse_mode(self):
        return self._parse_mode

    @property
    def buttons(self):
        return self._buttons
