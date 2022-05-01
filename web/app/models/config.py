import json
from uuid import uuid4


def read_config(path: str):
    f = open(path, "r")
    config = json.load(f)
    config["http"]["instance"] = config["http"].get("instance", uuid4())

    f.close()

    return config
