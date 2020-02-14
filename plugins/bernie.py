from lib import Plugin
from random import random
import asyncio, math

class BerniePlugin(Plugin):
    @asyncio.coroutine
    def on_ready(self):
        pass

    @asyncio.coroutine
    def on_message(self, message, history):
        m = message.content

        if message.author == self.client.user:
            return

        #bernie chain
        rnd = random()
        if m == "b" and random() > 0.2:
            yield from message.channel.send("e")

        if m == "e" and history[1] == "b":
            yield from message.channel.send("r")

        if m == "r" and history[1] == "e" and history[2] == "b" and rnd > 0.2:
            yield from message.channel.send("n")

        if m == "n" and history[1] == "r" and history[2] == "e" and history[3] == "b" and rnd > 0.3:
            yield from message.channel.send("i")

        if m == "i" and history[1] == "n" and history[2] == "r" and history[3] == "e" and history[4] == "b" and rnd > 0.4:
            yield from message.channel.send("e")

        #B E R N I E
        if m == "b e r n i e" or m == "B E R N I E" or m == "bernie" or m == "BERNIE":
            if rnd > 0.9:
                #get a random tweet
                tweets = yield from self.get_tweets("BernieSanders")
                num = math.floor((len(tweets)-1) * random())
                tweet = tweets[num]

                yield from message.channel.send(tweet.entities["urls"][0]["expanded_url"])
                return

            if rnd > 0.7:
                #respond in kind
                yield from message.channel.send(self.chance({"b e r n i e":0.25,"B E R N I E":0.25,"bernie":0.25,"BERNIE":0.25}))
                return

            if rnd > 0.5:
                #:allears:
                yield from message.add_reaction("allears:302026949331779587")
                return
