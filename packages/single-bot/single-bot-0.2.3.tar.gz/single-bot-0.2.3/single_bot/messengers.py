from aiogram import types, Bot, Dispatcher, F
from aiogram.types import Message
from single_bot.bot import Bot as ChatBot
import os
from single_bot.data_types import MessengerRequest, Metadata
from single_bot.auth_manager import AuthManager
from single_bot.logger import logger

# from auth_manager import AuthManager


# class BaseMessenger:
#     def __init__(self, single_bot):
#         self.single_bot = single_bot

#     def run(self):


# Принятие контакта пользователя
# class TelegramAuthManager:
#     def __init__(self, auth_manager: AuthManager):
#         self.


class TelegramBot:
    messenger_id = "telegram"

    def __init__(
        self,
        bot: ChatBot,
        TELEGRAM_TOKEN: str,
        auth_manager: AuthManager,
        require_auth: bool = False,
        # auth_message: str = "Для использования бота необходимо отправить свой контакт.",
        # auth_button_message: str = "Отправить контакт",
        restricted_access: bool = False,
    ):

        self.telegram_bot = Bot(TELEGRAM_TOKEN)
        self.chat_bot = bot
        self.auth_manager = auth_manager
        self.require_auth = require_auth
        self.restricted_access = restricted_access
        # self.auth_button_message = auth_button_message
        # self.auth_message = auth_message
        # self.auth_manager = auth_manager
        self._create_dispatcher()

    async def run(self):

        import logging
        import sys

        logging.basicConfig(level=logging.INFO, stream=sys.stdout)
        await self.dp.start_polling(self.telegram_bot)

    def _create_buttons(self, buttons=None):
        kb = [[]]
        for button in buttons:
            kb[0].append(types.KeyboardButton(text=button))
        return kb

    def _create_dispatcher(self):

        self.dp = Dispatcher()

        # @self.dp.message(F.contact)
        # async def contact_handler(message: Message):
        #     self.auth_manager.add_user(message.from_user.id)

        @self.dp.message()
        async def message_handler(message: Message):
            access = self.auth_manager.check_user(
                self.messenger_id, str(message.from_user.id)
            )
            if access not in ["admin", "allowed"]:
                return
            # if self.restricted_access:
            #     if not self.auth_manager.check_user(message.from_user.id):
            #         return

            async def send_message(text, reply_markup=types.ReplyKeyboardRemove()):
                if len(text) > 4095:
                    for x in range(0, len(text), 4095):
                        await message.answer(
                            text[x : x + 4095], reply_markup=reply_markup
                        )
                else:
                    await message.answer(text, reply_markup=reply_markup)

            # if self.require_auth:
            #     if not self.auth_manager.is_user_authorized(message.from_user.id):
            #         kb = [
            #             [
            #                 types.KeyboardButton(
            #                     text=self.auth_button_message, request_contact=True
            #                 )
            #             ]
            #         ]
            # await send_message(
            #     self.auth_message,
            #     reply_markup=types.ReplyKeyboardMarkup(
            #         keyboard=kb, resize_keyboard=True
            #     ),
            # )
            # return

            async def get_message_content():
                content = []
                if message.photo:
                    for photo in message.photo:
                        content.append({"type": "photo", "content": photo.model_dump()})

                if message.voice:
                    content.append(
                        {"type": "voice", "content": message.voice.model_dump()}
                    )
                if message.video:
                    content.append(
                        {"type": "video", "content": message.video.model_dump()}
                    )
                if message.document:
                    file_id = message.document.file_id
                    # Download using bot instance
                    file = await self.telegram_bot.get_file(file_id)
                    bytes = await self.telegram_bot.download_file(file.file_path)
                    content.append(
                        {
                            "type": "document",
                            "content": message.document.model_dump(),
                            "bytes": bytes,
                        }
                    )
                if message.audio:
                    content.append(
                        {"type": "audio", "content": message.audio.model_dump()}
                    )
                if message.caption:
                    content.append({"type": "caption", "content": message.caption})
                return content

            request = {
                "metadata": {
                    "message_id": str(message.message_id),
                    "messenger_id": self.messenger_id,
                    "full_name": str(message.from_user.full_name),
                    "username": str(message.from_user.username),
                    "messenger_user_id": str(message.from_user.id),
                    "messenger_chat_id": str(message.chat.id),
                    "authorized": True,
                    "reply_to_message_id": (
                        str(message.reply_to_message.message_id)
                        if message.reply_to_message
                        else None
                    ),
                },
                "message": {
                    "text": message.text,
                    "content": await get_message_content(),
                },
            }

            # ## EXAMPLE
            # async for answer in self.bot.get_answer(request):
            #     print(answer["text"])
            #     self.message_counter += 1
            #     buttons = answer["buttons"]
            # for button in buttons:
            #     print(f" - {button}")
            async for answer in self.chat_bot.get_answer(request):
                kb = [[]]
                text = answer["text"]
                logger.debug(f"Answer from telegram bot to user: {answer}")
                if text in ["", None]:
                    continue
                if "buttons" in answer:
                    if len(answer["buttons"]):
                        if answer["buttons"]["type"] == "telegram_reply":
                            keyboard = answer["buttons"]["content"]
                        else:
                            kb = self._create_buttons(answer["buttons"]["content"])
                            keyboard = types.ReplyKeyboardMarkup(
                                keyboard=kb, resize_keyboard=True
                            )
                        logger.debug(
                            f"Sending telegram message with buttons: {keyboard}"
                        )
                        await send_message(text, keyboard)
                        continue

                await send_message(text)

    # async def _process_streaming(self, stream):
    #     answer = ""
    #     async for token in stream:
    #         answer += token
    #     return answer

    # @dp.message(F.contact)
    # async def contacts(message: Message):
    #     save_user_phone(message.from_user.id, message.contact.phone_number)
    #     await message.answer("Спасибо!")
    #     await message.answer(
    #         text="Добро пожаловать!\n\nТеперь бот в твоём распоряжении.\nЗадавай вопрос, связанный с ТК РФ:",
    #         reply_markup=types.ReplyKeyboardRemove(),
    #     )


# class VoiceBot:
#     # Tasks:
#     def __init__(self, bot: ChatBot):
#         self.bot = bot

#     async def invoke(self):
#         tools = {
#             "send message",
#             #  "get_graph",
#         }


class CmdBot:
    def __init__(self, bot: ChatBot):
        self.bot = bot
        self.message_counter = 0

    async def run(self):

        while True:

            user_input = input("> ")
            request = {
                "metadata": {
                    "messenger_id": "cmd",
                    "messenger_user_id": os.getlogin(),
                    "messenger_chat_id": "0",
                    "authorized": True,
                    "username": os.getlogin(),
                    "reply_to_message_id": None,
                },
                "message": {"text": user_input, "content": []},
            }
            self.message_counter += 1

            async for message in self.bot.get_answer(request):
                print(message["text"])
                self.message_counter += 1
                buttons = message["buttons"]
            for button in buttons:
                print(f" - {button}")


# class VkBot:
#     def __init__(self, bot: ChatBot):
#         self.bot = bot

#     async def run(self):
