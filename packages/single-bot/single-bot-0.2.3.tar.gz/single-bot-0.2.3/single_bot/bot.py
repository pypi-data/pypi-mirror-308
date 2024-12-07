from single_bot.logger import logger
from single_bot.database import UserIdStorage, UserStateStorage, HistoryStorage
from single_bot.user_state import UserState
from single_bot.data_types import MessengerRequest, Answer
from typing import AsyncIterator
import asyncio


class Bot:
    # Responsible for managing users from messengers, running and saving their states.
    def __init__(
        self,
        user_id_storage: UserIdStorage,
        user_state_storage: UserStateStorage,
        history_storage: HistoryStorage,
        first_node: callable,
    ):
        self.history_storage = history_storage
        self.user_id_storage = user_id_storage
        self.first_node = first_node
        self.running = {}
        self.user_state_storage = user_state_storage

    async def get_answer(
        self, messenger_request: MessengerRequest
    ) -> AsyncIterator[Answer]:
        messenger_id = messenger_request["metadata"]["messenger_id"]
        messenger_user_id = messenger_request["metadata"]["messenger_user_id"]
        user_id = self.user_id_storage.get_user_id(
            messenger_id,
            messenger_user_id,
        )

        user_state_dict = self.user_state_storage.get_user_state(user_id)
        username = messenger_request["metadata"]["username"]
        if not user_state_dict:
            user_state = UserState(self.first_node, user_id=user_id)
        else:
            user_state = UserState(
                self.first_node,
                user_id=user_id,
                user_state_dict=user_state_dict,
            )
        message = messenger_request["message"]
        if user_id not in self.running:
            self.running[user_id] = user_state
            user_state.cancellation_event.clear()
        else:
            if message["text"] == "Остановить":
                self.running[user_id].cancellation_event.set()

            return

        update = {
            "messenger_id": messenger_id,
            "messenger_user_id": messenger_user_id,
            "user_id": user_id,
            "input": message,
            "output": [],
        }

        message.update({"metadata": messenger_request["metadata"]})

        async for response in user_state._invoke(message):
            text = ""
            logger.debug(f"Bot recieved: {response}")
            await asyncio.sleep(0)
            try:

                async for token in response["message"]["text"]:
                    logger.debug(f"Token: {token}")
                    text += token

                buttons = response["message"]["buttons"]
                answer = {"text": text, "buttons": buttons}
                response["message"].update(answer)
                update["output"].append(response)
            except Exception as e:
                logger.debug(f"Bot error: {e}", exc_info=e)

            # Way to proceed system requests... Not Implemented
            # if response.__class__.__name__ == "str":
            #     match response:
            #         case "auth":
            #             user_state._update({"auth_check": True})
            logger.debug(f"SingleBot answered: {answer}")
            yield answer
        logger.debug(f"Bot start updating databases")
        self.history_storage.save_message(update)  # TODO: ПОМЕНЯТЬ ИМЕНА

        self.user_state_storage.save_user_state(
            user_id, user_state._get_user_state_dict()
        )
        self.running.pop(user_id)
        logger.debug(f"Bot finished updating databases")
        return
