import json


def read_config(path: str):
    f = open(path, "r")
    config = json.load(f)

    f.close()

    return config
