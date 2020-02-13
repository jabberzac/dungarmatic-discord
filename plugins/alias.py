from lib import PersistentPlugin
from datetime import datetime, timedelta
from bson import Code
import asyncio
from tornado import gen


class AliasPlugin(PersistentPlugin):
    cmd = "alias"
    help = "Sets an alias for a game (admin only)"
    persist = ['aliases']

    aliases = {}
    reverse = {}

    @asyncio.coroutine
    def on_ready(self):
        for game in self.aliases:
            for alias in self.aliases[game]:
                self.reverse[alias] = game

    @asyncio.coroutine
    def on_command(self, message):
        if not self.from_admin(message):
            yield from message.channel.send("You must be an admin to add aliases")
            return

        played = yield from self.get_plugin("PlayedPlugin")

        content = message.content[7:]

        txt = ""

        if " as " not in content:
            yield from message.channel.send("Like this: !alias Fallout 76 as Terrible Game")
            return

        s = content.split(" as ")
        if s[0] in played.played:
            if s[0] not in self.aliases:
                self.aliases[s[0]] = []
            self.aliases[s[0]].append(s[1])
            self.reverse[s[1]] = s[0]
            txt = "Added alias for " + s[0] + " as '" + s[1] + "'"
        else:
            txt = "I have never heard of the game " + s[0]

        yield from message.channel.send(txt)
