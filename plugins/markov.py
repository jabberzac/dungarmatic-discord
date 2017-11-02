from lib import Plugin
import markovify, feedparser, random
from datetime import datetime, timedelta
from bson import Code
import asyncio
from tornado import gen
import re, html


class MarkovPlugin(Plugin):
    cmd = "markov"
    help = "Graces you with a pearl of wisdom generated from comments in /r/the_donald"

    chain = {}
    comments = ""
    counter = 0

    @asyncio.coroutine
    def on_tick(self):
        self.counter += 1
        if self.counter > 10 or not 'chain' in self.chain: #every 5 mins
            self.counter = 0

            tag_re = re.compile(r'(<!--.*?-->|<[^>]*>)')
            #get all comments from the_dotard
            d = feedparser.parse('http://www.reddit.com/r/the_donald/comments.rss?limit=100')

            num_comments = 100

            for i in range(num_comments):
                #unescape html and remove tags
                text = html.unescape(tag_re.sub('', str(d.entries[i]['content'][0]['value']))).strip(" ").strip("\n")
                #strip urls (links to breitbart)
                text = re.sub(r'\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*', '', text)
                self.comments += text + "\n"

            model = markovify.NewlineText(self.comments)
            self.chain = model.to_dict()

        rnd = random.random()

        if rnd > 0.99 and 'chain' in self.chain:
            model = markovify.Text.from_dict(self.chain)
            txt = model.make_sentence(test_output=False)
            if txt != None:
                channel = yield from self.get_channel("discordzac")
                yield from self.client.send_message(channel,txt)

    @asyncio.coroutine
    def on_command(self, message):
        if 'chain' not in self.chain:
            yield from self.client.send_message(message.channel, "Still collecting data from /r/the_donald")
            return
        model = markovify.Text.from_dict(self.chain)
        txt = None

        if len(message.content) > 8:
            word = message.content[8:]
            words = [key for key in model.chain.model.keys() if "___BEGIN__" in key]

            for key,val in words:
                if val == word:
                    txt = model.make_sentence(init_state=(key,val), test_output=False)

            if txt == None:
                txt = "I dunno anything about " + word

        else:
            txt = model.make_sentence(test_output=False)
        if txt != None:
            yield from self.client.send_message(message.channel, txt)


