import asyncio

from single_bot.data_types import Message, UserStateAnswer
import inspect
from typing import Any, AsyncIterator
from single_bot.data_types import TelegramReplyButtons
from single_bot.logger import logger


class InputTemplate:
    def __init__(self, input_field, buttons):
        self.input_field = input_field
        self.buttons = buttons


class UserInfo:
    def __init__(
        self, authorized_status: str, user_id: int, user_name: str, history: str = None
    ):
        self.authorized_status = authorized_status
        self.user_id: int = user_id
        self.user_name: str = user_name
        self.history = history


class FromNodes:
    responses = []
    buttons = {}


class Executor:  # TODO
    ...


class UserState:
    def __init__(self, first_node: callable, user_id, user_state_dict: dict = None):
        self.first_node = first_node
        if user_state_dict:
            self.__input_template = user_state_dict["input_template"]
            self.__values = user_state_dict["values"]
            self.data = user_state_dict["data"]
            self.temp = user_state_dict["temp"]
        else:
            self.__input_template = InputTemplate({"node": first_node}, {})
            self.__values = {}
            self.data = {}
            self.temp = {}
        self.user_id = user_id
        self.cancellation_event = asyncio.Event()
        self.last_message = None
        self.__answers = []
        self.__answer_pointer = 0
        self.__answer_counter = 0
        self.__next_node = None
        self.__requested_values = {}
        self.__finish = False
        self.__node_counter = 0
        self.__current_node = None
        self.__used_buttons = []
        # "__actions" - the way to send system messeges to the bot
        # "__updates" - the way to send answers to UserState
        self.__actions = []
        self.__updates = {}
        self.run_ids = []

    def _get_user_state_dict(self):
        return {
            "input_template": self.__input_template,
            "values": self.__values,
            "data": self.data,
            "temp": self.temp,
        }

    async def _invoke(self, request: Message) -> AsyncIterator[UserStateAnswer]:
        self.__user_request = request
        self.last_message = request
        logger.debug(f"Request: {request}")
        self.__node_counter = 0
        logger.debug("STARTED")
        task = asyncio.create_task(self.__execute_nodes())
        logger.debug("INVOKE")
        async for response in self.__listen_updates():  # НЕ ЗАКАНЧИВАЕТ РАБОТУ
            logger.debug("LISTENING")
            yield response
        logger.debug("END LISTENING")
        self.__answers = []
        self.__answer_pointer = 0
        self.__next_node = None
        return

    async def _update(self, values: dict):
        self.__updates.update(values)

    async def __execute_nodes(self):
        logger.debug(f"executing nodes started")
        while True:

            await asyncio.sleep(0)

            if self.__answer_counter < len(self.__answers):
                await asyncio.sleep(0)
                continue
            node = self.__get_next_node()
            if not node:
                self.__finish = True
                logger.debug("END EXECUTION")
                break
            self.__current_node = node.__name__
            logger.debug(f"current node: {node.__name__}")
            self.__node_counter += 1
            try:
                if inspect.iscoroutinefunction(node):
                    await node(self)
                else:
                    node(self)
            except Exception as e:
                raise logger.error(f"Error executing node: {str(e)}", exc_info=True)

    def __get_next_node(self) -> callable:
        # Returns node for executing.
        user_text = self.__user_request["text"]
        if self.__node_counter == 0:
            if user_text in self.__input_template.buttons.keys():
                node = self.__input_template.buttons[user_text]
                self.__buttons = {}
                self.__input_template.buttons = {}
                self.__used_buttons.append(
                    {"button_text": user_text, "node_name": node.__name__}
                )
                return node

            self.__buttons = {}
            self.__input_template.buttons = {}
            if "node" in self.__input_template.input_field.keys():
                node = self.__input_template.input_field["node"]
                self.__input_template.input_field = {"node": self.first_node}
                return node

        else:
            if self.__next_node:
                node = self.__next_node
                self.__next_node = None
                return node

        return False

    async def __listen_updates(self) -> AsyncIterator[UserStateAnswer]:

        last_loop = False
        while True:
            await asyncio.sleep(0)
            # "__actions" - the way to send system messeges to the
            # if len(self.__actions) != 0:
            #     yield self.__actions.pop(0)
            # logger.debug(
            #     f"Listening updates. Counter:{self.__answer_counter} Len answers: {len(self.__answers)}"
            # )
            if self.__answer_counter < len(self.__answers):
                self.__answer_counter += 1
                logger.debug(f"Yielding message to SingleBot: {self.__answer_counter}")
                yield {
                    "message": {
                        "text": self.__listen_streaming(self.__answer_counter - 1),
                        "content": self.__answers[self.__answer_counter - 1]["content"],
                        "buttons": self.__buttons,
                    },
                    "used_buttons": self.__used_buttons,
                    "node": self.__current_node,
                    "requested_values": self.__requested_values,
                    "run_ids": self.run_ids,
                }

                self.__requested_values = {}
                self.run_ids = []
                self.__used_buttons = []
            elif self.__finish:
                if last_loop:
                    logger.debug("listen_updates FINISHED")
                    break
                last_loop = True

    async def __listen_streaming(self, answer_id):
        chunk_counter = 0
        last_loop = False
        while answer_id == self.__answer_pointer or chunk_counter < len(
            self.__answers[answer_id]["text"]
        ):

            await asyncio.sleep(0)
            if not self.__answers[answer_id]["text"]:
                yield ""
                return
            try:

                chunk = self.__answers[answer_id]["text"][chunk_counter]
                chunk_counter += 1
                yield chunk
            except:
                pass

            if self.__finish:
                if last_loop:
                    break
                last_loop = True

    ### Methods for using in nodes
    def get_request(self) -> Message:
        return self.__user_request

    def send_message(
        self,
        text: str = "",
        buttons: Any = {},
        content: list[dict] = [],
        stream: bool = False,
    ):
        logger.debug(f"send_message {self.__answer_pointer+1} called with text: {text}")
        logger.debug(f"and buttons: {buttons}")
        if buttons.__class__ == TelegramReplyButtons:
            self.__input_template.buttons = buttons.get_dict()
            self.__buttons = buttons.get_buttons()
        else:
            self.__input_template.buttons = buttons
        if len(self.__answers) < self.__answer_pointer + 1:
            self.__answers.append({"text": [], "content": []})
        if text:
            self.__answers[self.__answer_pointer]["text"].append(text)

        if content:
            self.__answers[self.__answer_pointer]["content"].append(content)
        if not stream:
            self.__answer_pointer += 1
        elif not text:
            self.__answer_pointer += 1

    def add_button(self, name: str, node: callable):
        logger.debug(f"Add button: {name} - {node.__name__}")
        self.__input_template.buttons[name] = node

        if self.__buttons == {}:
            self.__buttons = {"type": "base", "content": {name: node}}
            return
        if self.__buttons["type"] == "base":
            self.__buttons["content"].update({name: node})

    def add_buttons(self, buttons: dict):
        logger.debug(f"Add buttons: {buttons}")
        if self.__buttons == {}:
            self.__buttons = {"type": "base", "content": buttons}
            return
        if self.__buttons["type"] == "base":
            self.__buttons["content"].update(buttons)
        else:
            print("Ошибка при добавлении различных типов кнопок")

    def set_input_field(self, node):
        self.__input_template.input_field = {"node": node}

    def set_next_node(self, node):
        self.__next_node = node

    def set_value(self, name, value):
        self.__values[name] = value

    def get_value(self, name):
        try:
            value = self.__values[name]
        except:
            value = None
        # For creating history of values
        self.__requested_values[name] = value
        return value

    async def auth_check(self) -> bool:
        self.__actions.append("auth_check")
        while True:
            await asyncio.sleep(0)
            if "auth_check" in self.__updates.keys():
                return self.__updates.pop("auth_check")

    def save_run_id(self, run_id):
        self.run_ids.append(run_id)
