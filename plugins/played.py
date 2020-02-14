from lib import PersistentPlugin
import asyncio
from discord import ActivityType


class PlayedPlugin(PersistentPlugin):
    cmd = "whoplays"
    help = "Tells you who plays the provided game"
    persist = ['played']

    played = {}

    @asyncio.coroutine
    def on_ready(self):
        self.ignore = self.get_plugin("IgnorePlugin")
        for member in self.client.get_all_members():
            if len(member.activities) > 0 and member.activities[0].type == ActivityType.playing:
                if member.activities[0].name not in self.ignore.ignores:
                    if member.activities[0].name not in self.played:
                        self.played[member.activities[0].name] = []
                    if (member.nick or member.name) not in self.played[member.activities[0].name]:
                        self.played[member.activities[0].name].append(member.nick or member.name)

    @asyncio.coroutine
    def on_member_update(self, old, member):
        if len(member.activities) > 0 and len(old.activities) == 0 and member.activities[0].type == ActivityType.playing:
            if member.activities[0].name not in self.ignore.ignores:
                if member.activities[0].name not in self.played:
                    self.played[member.activities[0].name] = []
                if (member.nick or member.name) not in self.played[member.activities[0].name]:
                    self.played[member.activities[0].name].append(member.nick or member.name)

    @asyncio.coroutine
    def on_command(self, message):
        game = message.content[10:].lower()

        aliases = self.get_plugin("AliasPlugin")
        if game in aliases.reverse:
            game = aliases.reverse[game]

        theset = {}
        for k,v in self.played.items():
            theset[k.lower()] = {'v':v,'k':k}

        if game.lower() in theset:
            i = theset[game.lower()]
            w = " plays "
            if len(i['v']) > 1:
                w = " play "
            yield from message.channel.send(', '.join(i['v']) + w + i['k'])
        else:
            yield from message.channel.send("No one plays " + game + ". It's probably a shit game anyway.")
