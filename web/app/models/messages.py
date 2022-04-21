import time
from typing import List

from sqlalchemy import Column, String, JSON, Integer, select
from sqlalchemy.sql import text
from sqlalchemy.orm import Session
from telegram.client import Telegram

from .database import Base
from .telegram import run_cmd


class Message(Base):
    __tablename__ = "messages"

    uid = Column(Integer, primary_key=True, index=True)
    chat_uid = Column(Integer)
    type = Column(String)
    text = Column(String)
    data = Column(JSON)

    def refresh_message_list(self, tg: Telegram, conn: Session, chat_id: id, receive_limit: id = 1):
        receive = True
        from_message_id = 0
        db_messages = []
        stats_data = {}

        while receive:
            res = run_cmd(tg, "getChatHistory", {
                "chat_id": chat_id,
                "limit": 1,
                "from_message_id": from_message_id,
            })

            for message in res["messages"]:
                stats_data[message['id']] = message
                msg = Message(uid=message["id"], chat_uid=message["chat_id"], type=message["content"]["@type"], text=message["content"]["caption"]["text"], data=message)
                db_messages.append(msg)
                #if message['content']['@type'] == 'messageText':
                #    stats_data[message['id']] = message['content']['text']['text']
                from_message_id = message['id']

            total_messages = len(stats_data)
            if total_messages > receive_limit or not res['total_count']:
                receive = False

            print(f'[{total_messages}/{receive_limit}] received')

        conn.add_all(db_messages)
        conn.commit()

        return stats_data

    def get_message(self, tg: Telegram, conn: Session, uid: int):
        return conn.query(Message).where(Message.uid == uid).one_or_none()

    def get_chat_message_list(self, tg: Telegram, conn: Session, chat_uid: int, limit: int = 10):
        return conn.query(Message).where(Message.chat_uid == chat_uid).limit(limit).all()
