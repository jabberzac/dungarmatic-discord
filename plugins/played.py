from lib import Plugin
import asyncio

played = {}

class PlayedPlugin(Plugin):
    cmd = "played"
    help = "Displays what games I have seen people playing"

    @asyncio.coroutine
    def on_ready(self):
        for member in self.client.get_all_members():
            if member.game != None:
                if member.game.name not in played:
                    played[member.game.name] = []
                if member.name not in played[member.game.name]:
                    played[member.game.name].append(member.name)

    @asyncio.coroutine
    def on_member_update(self, old, member):
        if member.game != None and member.game != old.game:
            if member.game.name not in played:
                played[member.game.name] = []
            if member.name not in played[member.game.__str__()]:
                played[member.game.name].append(member.name)

    @asyncio.coroutine
    def on_command(self, message):
        m = "Games jabberzac is playing:\n\n"
        for game in played.keys():
            m += game + ": " + ', '.join(played[game]) + "\n"

        yield from self.client.send_message(message.channel, m)