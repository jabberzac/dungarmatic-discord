from lib import PersistentPlugin
import asyncio, os, re
from steam import WebAPI

STEAM_TOKEN = os.environ.get('STEAM_TOKEN','')

#notifies #armazac channel of various overthrow stuff
class OverthrowPlugin(PersistentPlugin):
    persist = ["latest_item"]
    tick = 0
    last_check = 0
    latest_item = ''

    @asyncio.coroutine
    def on_ready(self):
        pass

    @asyncio.coroutine
    def on_tick(self):
        self.tick += 1
        if self.last_check == 0 or self.tick - self.last_check >= 40: #20 mins
            self.last_check = self.tick
            api = WebAPI(key=STEAM_TOKEN)
            channel = yield from self.get_channel("armazac")

            #Check for a new Arma 3 SITREP
            news = api.ISteamNews.GetNewsForApp_v1(appid=107410,count=1)
            latest = news['appnews']['newsitems']['newsitem'][0]

            if self.latest_item == '' or self.latest_item != latest['gid']:
                self.latest_item = latest['gid']
                yield from self.save()

                txt = "__**" + latest['title'] + "**__\n\n"
                contents = latest['contents']
                contents = re.sub(r"\[b\](.+?)\[\/b\]", r"**\1**", contents, flags=re.IGNORECASE)
                contents = re.sub(r"\[url=(.+?)\](.+?)\[\/url\]", r"\2 (\1)", contents, flags=re.IGNORECASE)

                txt += contents
                yield from self.client.send_message(channel, txt)