import time
from typing import List

from .telegram import run_cmd

from telegram.client import Telegram


def download_files_from_messages(messages: List[dict]) -> List[dict]:
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
            data.append(download_file(tg, id))
            time.sleep(1)

    return data


def download_file(tg: Telegram, id: int) -> List[dict]:
    data = {}

    f = run_cmd(tg, "downloadFile", {
        "file_id": id,
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
