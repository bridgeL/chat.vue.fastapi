from __future__ import annotations
from random import sample
from typing import Callable, Dict, List
from fastapi import WebSocket

from utils import log
from event import Event, LoginEvent, MessageEvent, InitEvent

uid_build_str = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"


def get_uid():
    return "".join(sample(uid_build_str, 6))


class User:
    users: List[User] = []
    history: List[MessageEvent] = []
    dealer_dict: Dict[str, List[Callable]] = {}

    @classmethod
    def add_user(self, user: User):
        self.users.append(user)

    @classmethod
    def remove_user(self, user: User):
        self.users.remove(user)

    @classmethod
    def add_msg(self, msg: MessageEvent):
        self.history.append(msg)

    @classmethod
    def dealer(self, event: Event):
        def base(func: Callable):
            key = event.__event__
            func_list = self.dealer_dict.get(key, None)
            if not func_list:
                self.dealer_dict[key] = [func]
            else:
                func_list.append(func)
        return base

    def __init__(self, ws: WebSocket) -> None:
        self.uid = ""
        self.ws = ws
        self.logined = False
        self.add_user(self)
        log.success(self.ws.client, "connect")

    def disconnect(self):
        self.remove_user(self)
        log.success(self.ws.client, "disconnect")

    async def send(self, event: Event):
        data = event.dict()
        data["type"] = event.__event__
        await self.ws.send_json(data)

        log.info("send", data)

    async def handle_event(self, event: Event):
        log.info("recv", event.__event__, event)

        func_list = self.dealer_dict.get(event.__event__, [])
        for func in func_list:
            await func(self, event)


@User.dealer(MessageEvent)
async def forward(self: User, event: MessageEvent):
    # 添加到历史记录
    self.add_msg(event)

    # 转发
    users = [u for u in self.users if u.logined and u != self]
    for u in users:
        await u.send(event)


@User.dealer(LoginEvent)
async def login(self: User, event: LoginEvent):
    # 发送初始化信息：uid、房间历史消息
    self.uid = event.uid if event.uid else get_uid()
    self.logined = True
    event = InitEvent(uid=self.uid, history=self.history)
    await self.send(event)
