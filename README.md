# telegram-bot
This help to make telegram-bot.

## Installation
1. Install python version 3.8 (This was only tested in python version 3.8)

    On Mac:
    ```bash
    brew install python@3.8
    ```
2. Clone the repository
    ```bash
    git clone https://github.com/hyoseo/telegram-bot.git
    ```
3. Create virtual environments in the cloned folder
    ```bash
    /usr/local/Cellar/python@3.8/3.8.1/bin/python3.8 -m venv /Users/hyoseo/IdeaProjects/telegram-bot/venv
    ```
4. Install dependencies from `requirements.txt`
    ```bash
    ./venv/bin/pip3 install -r requirements.txt
    ```
## Running
Run `telegram-bot`:
```bash
./sh_scripts/start.sh <TOKEN> <WEB_PORT> <LOG_LEVEL>
```
... where:
- `<TOKEN>` is the telegram token. You must pass it for first parameter.
- If you don't know what is telegram token or how to get it, The [BotFather](https://telegram.me/BotFather) will give you guide.
- `<WEB_PORT>` is the port, used for you can order to telegram-bot send message.
- If you don't pass `<WEB_PORT>`, default is `8080`.
- `<LOG_LEVEL>` is the log level which this program use. default is `INFO`
 
After run this, type `cat logs/telegram-bot.log` 
You can see the log liks:
```bash
2020-03-16 16:47:38.969      INFO [MainThread] main.py:24 - <module> : application pid : 50938
2020-03-16 16:47:38.969      INFO [MainThread] main.py:26 - <module> : TOKEN : <YOUR TELEGRAM TOKEN>
2020-03-16 16:47:38.969      INFO [MainThread] main.py:27 - <module> : WEB_PORT : 8080
2020-03-16 16:47:38.970      INFO [MainThread] main.py:28 - <module> : LOG_LEVEL : INFO
2020-03-16 16:47:38.974      INFO [MainThread] main.py:33 - <module> : Web server started on 8080
2020-03-16 16:47:38.974      INFO [MainThread] telegram.py:100 - process_web_server_queue : process_web_server_queue started.
```

## Usage
Send Message:
```bash
curl -v -X POST http://localhost:<WEB_PORT>/messages --data '{"chat_id":<chat_id>,"text":"hello world!"}'
```
Message Format:
```yaml
{
  "chat_id": <chat_id>,
  "text": "hello world!",
  "buttons": [
    {
      "text": ":o:Yes",
      "callback_url": "http://localhost:19800/test?i=30",
      "callback_http_method": "POST",
      "is_horizontal": true
    },
    {
      "text": "No",
      "callback_url": "https://www.google.co.kr/"
    }
  ]
}
```
... where:
- `<chat_id>` is the chat_id which you want to send to.
If you don't know how get chat_id, start your telegram bot and type /getchatid. Bot will show you your chat_id.
- `buttons` field is optional. If you use that and add button, you must include `text` and `callback_url` field.
- If you click the button you made in telegram, the `callback_url` you registered is called.

## Docker image
You can use this more easily by [telegram-bot Docker image](https://hub.docker.com/r/hyoseo/telegram-bot).

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)