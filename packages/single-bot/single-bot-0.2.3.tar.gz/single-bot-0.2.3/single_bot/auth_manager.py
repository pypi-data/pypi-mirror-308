# allow or disallow access
# default. banned. admin
from typing import Literal
from sqlitedict import SqliteDict

access_levels = Literal["allowed", "denied", "banned", "admin"]


class AuthManager:
    def __init__(
        self,
        default: access_levels = "allowed",
        messengers_default: dict = {},
        messengers: dict = {},
    ):
        self.messengers = messengers
        self.default = default
        self.messengers_default = messengers_default

    def check_user(self, messenger: str, messenger_user_id: str) -> access_levels:
        if messenger in self.messengers:
            if messenger_user_id in self.messengers[messenger]:
                return self.messengers[messenger][messenger_user_id]
        if messenger in self.messengers_default:
            return self.messengers_default[messenger]
        return self.default

    def set_user(
        self,
        messenger: str,
        messenger_user_id: str,
        access_level: access_levels,
    ):
        if messenger not in self.messengers:
            self.messengers[messenger] = {}

        self.messengers[messenger][messenger_user_id] = access_level
