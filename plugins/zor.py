from lib import Plugin
from random import random
import asyncio

class ZorPlugin(Plugin):
    @asyncio.coroutine
    def on_ready(self):
        pass

    @asyncio.coroutine
    def on_message(self, message, history):
        m = message.content
        if m == "z" and random() > 0.2:
            yield from message.channel.send("0")
        if m == "0" and history[1] == "z":
            if random() > 0.95:
                yield from message.channel.send("g")
            else:
                yield from message.channel.send("r")
        if m == "r" and history[1] == "0" and history[2] == "z" and random() > 0.8:
            yield from message.channel.send("0")
        if m == "0" and history[1] == "r" and history[2] == "0" and history[2] == "z" and random() > 0.5:
            if random() > 0.95:
                yield from message.channel.send("C-C-C-Combo breaker")
            else:
                yield from message.channel.send("z")
