from typing import (
    Any,
    Callable,
    List,
    TypedDict,
    Optional,
    Iterator,
    AsyncIterator,
    Union,
)
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


class Answer(TypedDict):
    text: str
    buttons: dict


class MessengerButtons(TypedDict):
    type: str
    content: Any


class Buttons:
    def __init__(self, content): ...

    def check_input(self, text): ...

    def get_dict(self) -> dict[str, callable]: ...

    def get_buttons(self) -> MessengerButtons: ...


class TelegramReplyButtons(Buttons):
    def __init__(self, content: List[dict[str, Callable]]):
        self.content = content

    def get_buttons(self) -> MessengerButtons:
        matrix = []
        for buttons in self.content:
            matrix.append([])
            for button in buttons:
                matrix[-1].append(KeyboardButton(text=button))

        return {
            "type": "telegram_reply",
            "content": ReplyKeyboardMarkup(keyboard=matrix, resize_keyboard=True),
        }

    def get_dict(self) -> dict[str, callable]:
        buttons_dict = {}
        for buttons in self.content:
            buttons_dict.update(buttons)
        return buttons_dict


class UserStateMessage(TypedDict):
    text: str
    buttons: dict
    content: list[dict]


class UserStateAnswer(TypedDict):
    message: UserStateMessage
    node: str
    requested_values: dict
    run_ids: list[str]
    used_buttons: list[dict]


class Metadata(TypedDict):
    message_id: Optional[str]
    messenger_name: str
    messenger_user_id: str
    username: Optional[str]
    full_name: Optional[str]
    messenger_chat_id: Optional[str]
    reply_to_message_id: Optional[str]
    authorized: Optional[bool]


class Message(TypedDict):
    metadata: Metadata
    text: str
    content: Optional[list]


class UserAuth(TypedDict):
    messenger_id: str
    messenger_user_id: str
    authorized: bool
    blocked: bool


class MessengerRequest(TypedDict):
    metadata: Metadata
    message: Message


class InputField(TypedDict):
    node: callable
    validator: Optional[callable]
    description: Optional[str]


class InputTemplate(TypedDict):
    input_field: Optional[InputField]
    buttons: dict


class UserStateDict(TypedDict):
    input_template: InputTemplate
    values: Optional[dict]


class RequestedData(TypedDict): ...


class History(TypedDict):
    node: str
    position_in_node: int
    requested_values: dict
    question: str
    answer: str
