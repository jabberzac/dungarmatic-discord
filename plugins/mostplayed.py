from lib import TimedPersistentPlugin
from datetime import datetime, timedelta
from bson import Code
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
        d = datetime.now() - timedelta(days=7)
        agg = {}
        for x in range(0,8):
            r = yield from self.map_reduce(Code('function map(){for(var k in this.played){emit(k,this.played[k])}}'),
                                           Code('function reduce(names,totals){return Array.sum(totals);}'),d.strftime("%Y%m%d"))

            d += timedelta(days=1)

            for result in r:
                if result['_id'] not in agg:
                    agg[result['_id']] = result['value']
                else:
                    agg[result['_id']] += result['value']


        ordered = []
        for k, v in agg.items():
            ordered.append({'g':k,'v':v})
        ordered = list(reversed(sorted(ordered, key=lambda k: k['v'])))

        txt = "**Most played games in the last 7 days**\n\n"
        num = 5
        if len(ordered) < num:
            num = len(ordered)
        for x in range(0,num):
            row = ordered[x]
            hrs = round(row['v'] / 120)
            txt += "" + str(x+1) + ". " + row['g'] + " (" + str(hrs) + " hrs)\n"

        yield from self.client.send_message(message.channel, txt)