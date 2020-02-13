from lib import PersistentPlugin
import markovify, feedparser, random
from datetime import datetime, timedelta
from bson import Code
import asyncio
from tornado import gen
import re, html


class GameChannelPlugin(PersistentPlugin):
    disabled=True
    cmd = "gamechannel"
    help = "Sets up this channel as a game channel (admin only)"
    persist = ["games"]

    games = {}

    @asyncio.coroutine
    def on_command(self, message):
        if self.from_admin(message):
            game = message.content[13:]
            self.games[message.channel.name] = game

    def on_message(self, message, history):
        if message.content == "!letsplay" and message.channel.name in self.games:
            game = self.games[message.channel.name]
            if game:
                played = yield from self.get_plugin("PlayedPlugin")

                txt = ""
                for name in played.played[game]:
                    member = self.get_member(name)
                    txt += "<@" + member.id + "> "

                if txt != "":
                    yield from self.client.send_message(message.channel, txt)
