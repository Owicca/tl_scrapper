import time, json
from typing import List
from enum import Enum

from sqlalchemy import Column, String, JSON, Integer, select
from sqlalchemy.sql import text
from sqlalchemy.orm import Session
from telegram.client import Telegram

from .database import Base
from .telegram import run_cmd


class MessageTypes(Enum):
    searchMessagesFilterAnimation = -155713339
    searchMessagesFilterAudio = 867505275
    searchMessagesFilterChatPhoto = -1247751329
    searchMessagesFilterDocument = 1526331215
    searchMessagesFilterFailedToSend = -596322564
    searchMessagesFilterMention = 2001258652
    searchMessagesFilterPhoto = 925932293
    searchMessagesFilterPhotoAndVideo = 1352130963
    searchMessagesFilterPinned = 371805512
    searchMessagesFilterUnreadMention = -95769149
    searchMessagesFilterUrl = -1828724341
    searchMessagesFilterVideo = 115538222
    searchMessagesFilterVideoNote = 564323321
    searchMessagesFilterVoiceAndVideoNote = 664174819
    searchMessagesFilterVoiceNote = 1841439357
    #searchMessagesFilterEmpty = -869395657


class Message(Base):
    __tablename__ = "messages"

    uid = Column(Integer, primary_key=True, index=True)
    chat_uid = Column(Integer)
    type = Column(String)
    text = Column(String)
    data = Column(JSON)


    def refresh_message_list(self, tg: Telegram, conn: Session, chat_uid: int, from_id: int = 0, receive_limit: int = 10):
        results = {}
        stmt = """REPLACE INTO messages VALUES(:uid, :chat_uid, :type, :text, :data)"""
        receive = True
        from_message_id = from_id

        while receive:
            res = run_cmd(tg, "getChatHistory", {
                "chat_id": chat_uid,
                "from_message_id": from_message_id,
                "offset": 0,
                "limit": receive_limit,
                "only_local": False
            })
            if res is None:
                receive = False
                break

            received_count = res["total_count"]
            message_list = res["messages"]

            for message in message_list:
                results[message['id']] = message

                text = "NoCaption"
                if message['content']['@type'] == 'messageText':
                    text = message['content']['text']['text']
                elif message["content"].get("caption") is not None:
                    text = message["content"]["caption"]["text"]
                #msg = Message(uid=message["id"], chat_uid=message["chat_id"], type=message["content"]["@type"], text=text, data=message)
                msg = {
                    "uid": message["id"],
                    "chat_uid": message["chat_id"],
                    "type": message["content"]["@type"],
                    "text": text,
                    "data": json.dumps(message)
                }
                conn.execute(stmt, msg)
                from_message_id = message['id']

            total_messages = len(results)
            if total_messages > receive_limit or not received_count or not received_count < receive_limit:
                receive = False
            if received_count < receive_limit:
                receive_limit -= received_count

        conn.commit()

        return {
            "results": results,
            "last_id": from_message_id
        }

    def get_message(self, tg: Telegram, conn: Session, limit: int):
        return conn.query(Message).where(Message.uid == uid).one_or_none()

    def get_message_list(self, tg: Telegram, conn: Session, limit: int):
        return conn.query(Message).limit(limit).all()

    def get_chat_message_list(self, tg: Telegram, conn: Session, chat_uid: int, limit: int = 10):
        return conn.query(Message).where(Message.chat_uid == chat_uid).limit(limit).all()

    def get_chat_message_count(self, tg: Telegram, chat_uid: int):
        results = []

        for tp in MessageTypes:
            res = run_cmd(tg, "getChatMessageCount", {
                "chat_id": chat_uid,
                "filter": tp.name,
                "return_local": False
            })

            results.append(res)

        return results

    def create(self, conn: Session):
        conn.add(self)
        conn.commit()

        return None
