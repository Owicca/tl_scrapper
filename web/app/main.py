#!/usr/bin/env python

import sys, json, os, time
from typing import List

from fastapi import FastAPI, BackgroundTasks, Response, status
from sqlalchemy.sql import text

from models.config import read_config
from models.database import get_connection
from models.files import File, download_files_from_messages
from models.chats import Chat, ChatActions, ChatActionsRequest
from models.messages import Message
from models.telegram import startup_telegram_session, shutdown_telegram_session, run_cmd


app = FastAPI()
tg = None
config = read_config("./../config.json")
conn = get_connection(config)


def handle_message(update):
    message = update["message"]

    text = "NoCaption"
    if message["content"].get("caption") is not None:
        text = message["content"]["caption"]["text"]

    Message(uid=message["id"], chat_uid=message["chat_id"], type=message["content"]["@type"], text=message["content"]["caption"]["text"], data=message).create(conn)

def handle_file_update(update):
    file = update["file"]
    data = {
        "completed": file["local"]["is_downloading_completed"],
        "active": file["local"]["is_downloading_active"],
        "path": file["local"]["path"],
    }
    if data["completed"]:
        File(uid=file["id"], path=data["path"], data=file).create(conn)
#Chat(uid=chat["id"], name=chat["title"], data=chat).create(conn)
@app.on_event("startup")
async def startup():
    global tg

    tg = startup_telegram_session(config)
    tg.add_message_handler(handle_message)
    tg.add_update_handler("updateFile", handle_file_update)

@app.on_event("shutdown")
async def shutdown():
    global tg

    shutdown_telegram_session(tg)

    print("finished cleanup")


#@app.get("/")
#async def index():
#    global tg
#
#    data = []
#
#    data = download_files_from_messages(messages)
#
#    data = messages = Message().refresh_message_list(tg, conn, chat["id"], receive_limit=10)
#
#    return data

@app.get("/chats/")
async def chat_list(limit: int = 10):
    data = Chat().get_chat_list(tg, conn, limit)

    return data

@app.post("/chats/")
async def chat_action(response: Response, data: ChatActionsRequest):
    results = []

    if data.action == ChatActions.REFRESH:
        results =  Chat().refresh_chat_list(tg, conn)
    else:
        response.status_code = status.HTTP_400_BAD_REQUEST

    return results


@app.get("/chats/{chat_id}/messages/")
async def chat_message_list(chat_uid: int, limit: int = 10):
    return Message().get_chat_message_list(tg, conn, chat_uid, limit)

@app.get("/messages/")
async def message_list(limit: int = 10):
    return Message().get_message_list(tg, conn, limit=limit)

@app.get("/messages/{uid}")
async def message_list(response: Response, uid: int):
    message = Message().get_message(tg, conn, uid)

    if message is None:
        response.status_code = status.HTTP_404_NOT_FOUND

    return message

@app.get("/files/")
async def file_list(limit: int = 10):
    return File().get_file_list(tg, conn, limit=limit)

@app.post("/files/")
async def file_list(uid: int):
    res = File().download_file(tg, conn, uid=uid)

    return res
