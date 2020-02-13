from lib import Plugin
import markovify, feedparser, random
from datetime import datetime, timedelta
from bson import Code
import asyncio
from tornado import gen
import re, html


class StatsPlugin(Plugin):
    cmd = "stats"
    help = "Shows bot stats (admin only)"
    announced = False

    @asyncio.coroutine
    def on_command(self, message):
        plugins = ""
        for plugin in self.loaded_plugins:
            if plugin != "TimedPersistentPlugin":
                plugins += plugin[0:-6] + ", "
        plugins = plugins[0:-2]

        yield from message.channel.send("Loaded plugins: " + plugins)

        games = ""
        played = yield from self.get_plugin("PlayedPlugin")
        for game in played.played:
            games += game + ", "
        games = games[0:-2]

        yield from message.channel.send("All known games: " + games)

    @asyncio.coroutine
    def on_tick(self):
        if not self.announced:
            self.announced = True
            channel = yield from self.get_channel("dungarmatic-test")

            plugins = ""
            for plugin in self.loaded_plugins:
                if plugin != "TimedPersistentPlugin":
                    plugins += plugin[0:-6] + ", "
            plugins = plugins[0:-2]

            yield from channel.send("I am coming online, plugins loaded: "+plugins)
