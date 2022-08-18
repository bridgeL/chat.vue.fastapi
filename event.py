from inspect import isclass
from typing import List
from pydantic import BaseModel
from utils import get_time_s


class Event(BaseModel):
    __event__ = ""


class RawEvent(Event):
    __event__ = "raw"
    data: dict


class UserInfo(BaseModel):
    name: str
    color: str
    uid: str


class MessageEvent(Event):
    __event__ = "message"
    user: UserInfo
    text: str
    ctime: str

    def __init__(self, **data):
        data["ctime"] = get_time_s()
        super().__init__(**data)


class HeartBeatEvent(Event):
    __event__ = "heartbeat"


class LoginEvent(Event):
    __event__ = "login"
    uid: str
    name: str
    color: str


class InitEvent(Event):
    __event__ = "init"
    uid: str
    history: List[MessageEvent]


models = locals()
models = [m for m in models.values() if isclass(m)]
models = [m for m in models if issubclass(m, Event)]
models = {m.__event__: m for m in models if m.__event__}


def json2event(data: dict):
    try:
        event_type = data["type"]
        event = models[event_type](**data)
    except:
        event = RawEvent(data=data)
    return event
