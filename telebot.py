import time

from .http_req_object import Response, http_request
from .models import BotUpdates, BotMessage
from .custom_ex import WrongBotApiToken
from .settings import config


class Bot:
    def __init__(self, bot_token: str) -> None:
        self.bot_url = f"https://api.telegram.org/bot{bot_token}/"
        self.requests = http_request
        self.last_update_id = None
        self.token_checked = None
        self.event_loop = []

    def _check_tocken(self) -> int:
        url = self.bot_url + "getMe"
        response = self.requests(method='get', url=url).json()
        self.token_checked = response['ok']
        if not self.token_checked:
            print('******Unvalid bot token!******')
            raise WrongBotApiToken
        return 200

    def get_last_update(self) -> BotUpdates | None:
        if not self.token_checked:
            self._check_tocken()

        if self.last_update_id:
            response = self._get_updates(offset=self.last_update_id)
            if response:
                self.last_update_id += 1
            return response
        response = self._get_updates()
        if response:
            self.last_update_id = response.update_id
        return response

    def _get_updates(self, offset: int | None = None) -> BotUpdates | None:
        url = self.bot_url + "getUpdates"
        if offset:
            url += f"?offset={offset}"
        response = self.requests(method='get', url=url)
        data = response.json()
        if data["result"]:
            result = BotUpdates(**data["result"][0])
            return result
        return None

    def message_handler(self):
        def wrapper(func):
            self.event_loop.append(func)
        return wrapper

    def send_message(self, text: str, chat_id: int) -> Response:
        url = self.bot_url + "sendMessage"
        message = BotMessage(chat_id=chat_id, text=text).dict()

        response = self.requests(method='post',
                                 url=url, json=message,
                                 headers=config.headers)
        return response

    def run(self) -> None:
        while True:
            if message := self.get_last_update():
                for f in self.event_loop:
                    f(message.message)
            time.sleep(0.1)
