from lib import Plugin
from random import random
import asyncio

#notifies #armazac channel of various overthrow stuff
class OverthrowPlugin(Plugin):
    @asyncio.coroutine
    def on_ready(self):
        pass

    @asyncio.coroutine
    def on_message(self, message, history):
        m = message.content
        if m == "z" and random() > 0.2:
            yield from self.client.send_message(message.channel, "0")
        if m == "0" and history[1] == "z":
            if random() > 0.95:
                yield from self.client.send_message(message.channel, "g")
            else:
                yield from self.client.send_message(message.channel, "r")
        if m == "r" and history[1] == "0" and history[2] == "z" and random() > 0.8:
            yield from self.client.send_message(message.channel, "0")
        if m == "0" and history[1] == "r" and history[2] == "0" and history[2] == "z" and random() > 0.5:
            if random() > 0.95:
                yield from self.client.send_message(message.channel, "C-C-C-Combo breaker")
            else:
                yield from self.client.send_message(message.channel, "z")