from lib import TimedPersistentPlugin
from datetime import datetime, timedelta
from bson import Code
import asyncio,re
from tornado import gen


class LinksPlugin(TimedPersistentPlugin):
    cmd = "links"
    help = "Gives you the last 5 links posted in this channel"
    persist = ['links']

    timeline = {}
    links = {}

    @asyncio.coroutine
    def on_message(self, message, history):
        m = message.content

        regex = r"(https?:\/\/)?([\da-z\.-]+\.(?:[a-z\.]{2,6}))([\/\w\.-]+)[\/\s]?"
        matches = re.finditer(regex, m, re.MULTILINE)
        id = message.channel.id
        if id not in self.links:
            self.links[id] = []
        if id not in self.timeline:
            self.timeline[id] = []

        for matchNum, match in enumerate(matches):
            url = ''.join(map(str,match.groups()))
            if url not in self.links[id]:
                self.links[id].append(url)
            if url not in self.timeline[id]:
                self.timeline[id].append(url)
            else:
                # do nothing because img timeline is a piece of shit

    @asyncio.coroutine
    def on_command(self, message):
        if message.channel.id not in self.timeline or len(self.timeline[message.channel.id]) == 0:
            yield from self.client.send_message(message.channel, "No links have been posted in here")
            return
        r = self.timeline[message.channel.id][::-1]
        txt = "**Last 5 Links in this channel**\n\n"
        for x in range(0,5):
            if (len(r)-1) < x:
                break
            txt += str(x+1) + ". " + r[x] + "\n"

        yield from self.client.send_message(message.channel, txt)