from lib import TimedPersistentPlugin
import asyncio



class MostPlayedPlugin(TimedPersistentPlugin):
    cmd = "mostplayed"
    help = "Tells you what games have been played the most in the past 7 days"
    persist = ['played']

    played = {}

    @asyncio.coroutine
    def on_tick(self):
        for member in self.client.get_all_members():
            if member.game != None:
                if member.game.name not in self.played:
                    self.played[member.game.name] = 1
                else:
                    self.played[member.game.name] += 1

    @asyncio.coroutine
    def on_command(self, message):
        pass