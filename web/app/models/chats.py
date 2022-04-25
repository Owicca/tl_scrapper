import time
from enum import Enum
from typing import List

from sqlalchemy import Column, String, JSON, Integer, select
from sqlalchemy.sql import text
from sqlalchemy.orm import Session
from telegram.client import Telegram
from pydantic import BaseModel

from .database import Base
from .telegram import run_cmd


class ChatActions(Enum):
    REFRESH = 1
    UPDATE = 2


class ChatActionsRequest(BaseModel):
    action: ChatActions = ChatActions.REFRESH


class Chat(Base):
    __tablename__ = "chats"

    uid = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    data = Column(JSON)

    def refresh_chat_list(self, tg: Telegram, conn: Session) -> List[dict]:
        chats = []
        db_chats = []

        res = tg.get_chats()
        res.wait()

        chat_ids = res.update["chat_ids"]
        for id in chat_ids:
            chat = run_cmd(tg, "getChat", {
                "chat_id": id
            })
            db_chats.append(Chat(uid=chat["id"], name=chat["title"], data=chat))
            chats.append(chat)
            time.sleep(0.3)

        conn.execute(text("TRUNCATE TABLE chats"))
        conn.add_all(db_chats)
        conn.commit()

        return chats

    def get_chat_list(self, tg: Telegram, conn: Session, limit: int = 10):
        return conn.query(Chat).limit(limit).all()

    def create(self, conn: Session):
        conn.add(self)
        conn.commit()

        return None
