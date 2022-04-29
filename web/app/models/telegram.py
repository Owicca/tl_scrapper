import time
from random import uniform

from telegram.client import Telegram, AuthorizationState


def startup_telegram_session(config: dict) -> Telegram:
    tg = Telegram(
        api_id=config["telegram"]["api_id"],
        api_hash=config["telegram"]["api_hash"],
        phone=config["telegram"]["phone"],  # you can pass 'bot_token' instead
        database_encryption_key=config["telegram"]["database_encryption_key"],
        files_directory=config["telegram"]["files_directory"],
        use_message_database=config["telegram"]["use_message_database"],
        use_secret_chats=config["telegram"]["use_secret_chats"],
        tdlib_verbosity=config["telegram"]["tdlib_verbosity"]
    )
    state = tg.login(blocking=False)

    if state == AuthorizationState.WAIT_CODE:
        print("Need code")
        pin = input("Enter code: ")
        tg.send_code(pin)
        status = tg.login(blocking=False)
    if state == AuthorizationState.WAIT_PASSWORD:
        print("Need password")
        password = input("Enter password: ")
        tg.send_password(password)
        status = tg.login(blocking=False)

    return tg


def shutdown_telegram_session(tg: Telegram):
    tg.stop()  # you must call `stop` at the end of the script


def run_cmd(tg: Telegram, cmd: str, params: dict = {}) -> dict:
    res = tg.call_method(cmd, params)
    res.wait()

    time.sleep(uniform(0.5, 2.0)) #throttle requests

    return res.update
