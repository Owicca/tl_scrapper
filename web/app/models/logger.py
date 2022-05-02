import time, json
from enum import IntEnum


class LoggerLevel(IntEnum):
    ERROR = 1
    WARN = 2
    INFO = 3
    DEBUG = 4

    @classmethod
    def map_level(self, level: str):
        results = self.ERROR

        if level == "warn":
            results = self.WARN
        elif level == "info":
            results = self.INFO
        elif level == "debug":
            results = self.DEBUG

        return results

def lg(config: dict, message: dict = {}, log_level: LoggerLevel = LoggerLevel.DEBUG):
    if log_level.value > LoggerLevel.map_level(config["logger"]["level"]):
        return

    msg = {
        "time": time.time_ns(),
        "msg": message,
        "level": log_level.name,
        "domain": config["http"]["domain"],
        "instance": str(config["http"]["instance"])
    }

    print(json.dumps(msg))
