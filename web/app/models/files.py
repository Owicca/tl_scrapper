import time
from typing import List

from sqlalchemy import Column, String, JSON, Integer, select
from sqlalchemy.sql import text
from sqlalchemy.orm import Session
from telegram.client import Telegram

from .database import Base
from .telegram import run_cmd


class File(Base):
    __tablename__ = "files"

    uid = Column(Integer, primary_key=True, index=True)
    path = Column(String)
    data = Column(JSON)

    def create(self, conn: Session):
        conn.add(self)
        conn.commit()

        return None

    def get_file_list(self, conn: Session, limit: int = 10):
        return conn.query(File).limit(limit).all()

    def download_file(self, tg: Telegram, conn: Session, uid: int) -> dict:
        data = {}

        f = run_cmd(tg, "downloadFile", {
            "file_id": uid,
            "priority": 1,
            "offset": 0,
            "limit": 0,
            "synchronous": False
        })
        if f is not None:
            data = {
                "completed": f["local"]["is_downloading_completed"],
                "active": f["local"]["is_downloading_active"],
                "path": f["local"]["path"],
            }
        else:
            data = {
                "is_none": "is_none"
            }

        return data


def download_files_from_messages(conn: Session, messages: List[dict]) -> List[dict]:
    data = []

    for msg_id in messages:
        content = messages[msg_id]["content"]
        id = None

        #data.append(messages[msg_id])
        if content["@type"] == "messagePhoto":
            photo = content["photo"]["sizes"][1]
            id = photo["photo"]["id"]
        elif content["@type"] == "messageVideo":
            vid = content["video"]["video"]
            id = vid["id"]

        if id is not None:
            data.append(download_file(tg, conn, id))
            time.sleep(1)

    return data
