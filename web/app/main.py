#!/usr/bin/env python

import sys, json, os, time
from typing import List

from fastapi import FastAPI, BackgroundTasks, Response, status
from sqlalchemy.sql import text

from models.config import read_config
from models.database import get_connection
from models.files import File, download_files_from_messages
from models.chats import Chat, ChatActions, ChatActionsRequest
from models.messages import Message, MessageTypes
from models.telegram import startup_telegram_session, shutdown_telegram_session, run_cmd


app = FastAPI()
tg = None
config = read_config("./../config.json")
conn = get_connection(config)


def handle_message(update):
    message = update["message"]

    text = "NoText"
    if message['content']['@type'] == 'messageText':
        text = message['content']['text']['text']
    elif message["content"].get("caption") is not None:
        text = message["content"]["caption"]["text"]

    Message(uid=message["id"], chat_uid=message["chat_id"], type=message["content"]["@type"], text=text, data=message).create(conn)
    print("new message", message["id"], message["chat_id"])

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


@app.get("/chats/{chat_uid}/messages/")
async def chat_message_list(chat_uid: int, limit: int = 10):
    return Message().get_chat_message_list(tg, conn, chat_uid, limit)

@app.post("/chats/{chat_uid}/messages/{message_uid}")
async def scrape_chat(chat_uid: int, message_uid: int = 0, limit: int = 25):
    results = []
    total = 0
    run = True
    from_id = message_uid

    while run:
        res = Message().refresh_message_list(tg, conn, chat_uid, from_id=from_id, receive_limit=limit)
        from_id = res["last_id"]
        step_results = res["results"]
        cnt = len(step_results)
        results.append(cnt)
        total += cnt

        if not step_results:
            run = False
        print(cnt, total, from_id, run)

    return results


@app.get("/messages/")
async def message_list(limit: int = 10):
    return Message().get_message_list(tg, conn, limit=limit)

@app.get("/messages/{uid}")
async def get_message(response: Response, uid: int):
    message = Message().get_message(tg, conn, uid)

    if message is None:
        response.status_code = status.HTTP_404_NOT_FOUND

    return message


@app.get("/files/")
async def file_list(limit: int = 10):
    return File().get_file_list(tg, conn, limit=limit)

@app.post("/files/")
async def file_download(uid: int):
    res = File().download_file(tg, conn, uid=uid)

    return res
