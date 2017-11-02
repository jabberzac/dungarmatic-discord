from lib import Plugin
import markovify, feedparser, random
from datetime import datetime, timedelta
from bson import Code
import asyncio
from tornado import gen
import re, html


class StatsPlugin(Plugin):
    announced = False

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

            yield from self.client.send_message(channel, "I am coming online, plugins loaded: "+plugins)