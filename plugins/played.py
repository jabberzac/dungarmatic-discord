from lib import PersistentPlugin
import asyncio



class PlayedPlugin(PersistentPlugin):
    cmd = "whoplays"
    help = "Tells you who plays the provided game"
    persist = ['played']

    played = {}

    @asyncio.coroutine
    def on_ready(self):
        self.ignore = yield from self.get_plugin("IgnorePlugin")
        for member in self.client.get_all_members():
            if member.game != None:
                if member.game.name not in self.ignore.ignores:
                    if member.game.name not in self.played:
                        self.played[member.game.name] = []
                    if (member.nick or member.name) not in self.played[member.game.name]:
                        self.played[member.game.name].append(member.nick or member.name)

    @asyncio.coroutine
    def on_member_update(self, old, member):
        if member.game != None and member.game != old.game:
            if member.game.name not in self.ignore.ignores:
                if member.game.name not in self.played:
                    self.played[member.game.name] = []
                if (member.nick or member.name) not in self.played[member.game.__str__()]:
                    self.played[member.game.name].append(member.nick or member.name)

    @asyncio.coroutine
    def on_command(self, message):
        game = message.content[10:].lower()

        aliases = yield from self.get_plugin("AliasPlugin")
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
            yield from self.client.send_message(message.channel, ', '.join(i['v']) + w + i['k'])
        else:
            yield from self.client.send_message(message.channel, "No one plays " + game + ". It's probably a shit game anyway.")