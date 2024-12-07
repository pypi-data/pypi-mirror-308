from single_bot.messengers import TelegramBot, CmdBot
from single_bot.database import UserIdStorage, UserStateStorage, HistoryStorage
from single_bot.bot import Bot
from typing import Literal
import shutil
import os
from single_bot.config import SINGLE_BOT_DATABASE_PATH


class BotFactory:
    # Responsible for creating and starting messengers
    def __init__(
        self, first_node, auth_manager, data_path: str = "data/", name: str = "bot"
    ):
        self.data_path = data_path
        self.first_node = first_node
        self.name = name
        self.auth_manager = auth_manager

    async def start(
        self, platform: Literal["telegram", "cmd"], token: str | None = None
    ):
        self.bot = Bot(
            UserIdStorage(database_url=f"{self.data_path}single_bot_{self.name}.db"),
            UserStateStorage(database_url=f"{self.data_path}single_bot_{self.name}.db"),
            HistoryStorage(f"sqlite:///{self.data_path}single_bot_{self.name}.db"),
            first_node=self.first_node,
        )
        if platform == "telegram":
            if token is None:
                messenger = TelegramBot(self.bot)
            else:
                messenger = TelegramBot(self.bot, token, auth_manager=self.auth_manager)
            await messenger.run()
        if platform == "cmd":
            messenger = CmdBot(self.bot)
            await messenger.run()

    def remove_data(self):
        if os.path.exists(self.data_path[:-1]):
            shutil.rmtree(self.data_path[:-1])
