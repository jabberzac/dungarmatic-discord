from lib import PersistentPlugin
from datetime import datetime, timedelta
from bson import Code
import asyncio
from tornado import gen


class IgnorePlugin(PersistentPlugin):
    cmd = "ignore"
    help = "Ignores a game in all stats (admin only)"
    persist = ['ignores']

    ignores = []

    @asyncio.coroutine
    def on_command(self, message):
        if not self.from_admin(message):
            yield from self.client.send_message(message.channel, "You must be an admin to add ignores")
            return

        played = yield from self.get_plugin("PlayedPlugin")

        content = message.content[8:]

        txt = ""

        if content in played.played:
            if content not in self.ignores:
                self.ignores.append(content)
                txt = "Will ignore " + content + " from now on"
            else:
                txt = "I am already ignoring " + content
        else:
            txt = "I have never heard of the game " + content

        yield from self.client.send_message(message.channel, txt)

