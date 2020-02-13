from lib import Plugin
import markovify, feedparser, random
from datetime import datetime, timedelta
from bson import Code
import asyncio
from tornado import gen
import re, html


class ThinkingEmojiPlugin(Plugin):

    @asyncio.coroutine
    def on_message(self, message, history):
        if message.content.find("🤔") > -1:
            yield from message.add_reaction('🤔')
        if message.content.find("<:thinkingbig:326671061225832448>") > -1:
            yield from message.add_reaction("thinkingbig:326671061225832448")
