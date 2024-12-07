from single_bot.data_types import UserStateDict
from sqlitedict import SqliteDict
from typing import Union
import os
from sqlalchemy import create_engine, Column, Integer, String, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import dill
import sqlite3


def encode(obj):
    """Serialize an object using dill to a binary format accepted by SQLite."""
    return sqlite3.Binary(dill.dumps(obj))


def decode(obj):
    """Deserialize objects retrieved from SQLite using dill."""
    return dill.loads(bytes(obj))


class UserStateStorage:
    def __init__(self, database_url):
        self.database_url = database_url
        self.storage = SqliteDict(
            self.database_url,
            tablename="user_states",
            autocommit=True,
            encode=encode,
            decode=decode,
        )

    def get_user_state(self, user_id: int) -> Union[UserStateDict, False]:
        user_id = str(user_id)
        if user_id in self.storage:
            return self.storage[user_id]
        else:
            return False

    def save_user_state(self, user_id: int, state: UserStateDict):
        user_id_str = str(user_id)
        self.storage[user_id_str] = state

    def close(self):
        self.storage.close()


class UserIdStorage:
    def __init__(self, database_url):
        self.users_count = 0
        self.messengers_stores = {}
        self.database_url = database_url

        # Open the main database
        with SqliteDict(
            self.database_url,
            autocommit=True,
            encode=encode,
            decode=decode,
        ) as db:
            # Get the list of tables (messengers)
            tables = db.get("__tables__", [])

            # Initialize stores for each messenger
            for messenger in tables:
                self.messengers_stores[messenger] = SqliteDict(
                    self.database_url,
                    tablename=messenger,
                    autocommit=True,
                    encode=encode,
                    decode=decode,
                )
                self.users_count += len(self.messengers_stores[messenger])

    def get_user_id(self, messenger_name: str, messenger_user_id):

        messenger_user_id = str(messenger_user_id)

        if messenger_name not in self.messengers_stores:
            # Create a new table for the messenger if it doesn't exist
            self.messengers_stores[messenger_name] = SqliteDict(
                self.database_url,
                tablename=messenger_name,
                autocommit=True,
                encode=encode,
                decode=decode,
            )

            # Update the list of tables
            with SqliteDict(
                self.database_url,
                autocommit=True,
                encode=encode,
                decode=decode,
            ) as db:
                tables = db.get("__tables__", [])
                if messenger_name not in tables:
                    tables.append(messenger_name)
                    db["__tables__"] = tables

        store = self.messengers_stores[messenger_name]

        if messenger_user_id not in store:
            self.users_count += 1
            store[messenger_user_id] = self.users_count

        return store[messenger_user_id]

    def close(self):
        for store in self.messengers_stores.values():
            store.close()

    # def _create_full_user_id_database(self):
    # self.users_storage = SqliteDict("user_id_storage.db", autocommit=True)
    #     for storage_name in self.messengers_stores.keys():
    #         for user in self.messengers_stores[storage_name].keys():
    #             self.users_storage[str(self.messengers_stores[storage_name][user])] = {
    #                 "messenger_name": storage_name,
    #                 "messenger_user_id": user,
    #             }


class HistoryStorage:
    Base = declarative_base()

    class MessagesHistory(Base):
        __tablename__ = "messages_history"
        id = Column(Integer, primary_key=True, autoincrement=True)
        user_id = Column(String)
        messenger_id = Column(String)
        messenger_user_id = Column(String)
        timestamp = Column(DateTime, default=datetime.now())
        # input = Column(JSON, nullable=True)
        # output = Column(JSON, nullable=True)

        user_feedback = Column(String, default=None)

    def __init__(self, database_url):
        self.engine = create_engine(f"{database_url}")
        self.Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def save_message(self, message: dict):
        session = self.Session()
        session.add(
            self.MessagesHistory(
                messenger_id=message["messenger_id"],
                messenger_user_id=message["messenger_user_id"],
                # input=message["input"],
                # output=message["output"],
                user_id=message["user_id"],
            )
        )
        session.commit()
        session.close()
