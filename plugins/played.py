from lib import PersistentPlugin
import asyncio



class PlayedPlugin(PersistentPlugin):
    cmd = "played"
    help = "Displays what games I have seen people playing"
    persist = ['played']

    played = {}

    @asyncio.coroutine
    def on_ready(self):
        for member in self.client.get_all_members():
            if member.game != None:
                if member.game.name not in self.played:
                    self.played[member.game.name] = []
                if (member.nick or member.name) not in self.played[member.game.name]:
                    self.played[member.game.name].append(member.nick or member.name)

    @asyncio.coroutine
    def on_member_update(self, old, member):
        if member.game != None and member.game != old.game:
            if member.game.name not in self.played:
                self.played[member.game.name] = []
            if (member.nick or member.name) not in self.played[member.game.__str__()]:
                self.played[member.game.name].append(member.nick or member.name)

    @asyncio.coroutine
    def on_command(self, message):
        m = "Games jabberzac is playing:\n\n"
        for game in self.played.keys():
            m += "**" + game + "**\n" + ', '.join(self.played[game]) + "\n\n"

        yield from self.client.send_message(message.channel, m)