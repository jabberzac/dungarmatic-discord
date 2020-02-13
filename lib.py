import asyncio,json,os,re,random
from datetime import datetime, timedelta
import motor.motor_asyncio
from simplekv.fs import FilesystemStore
from tornado import gen

MONGODB_URI = os.environ.get('MONGODB_URI','mongodb://localhost')

store = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URI)['dungarmatic']
tornado_store = motor.motor_tornado.MotorClient(MONGODB_URI)['dungarmatic']

class Plugin:
    disabled = False
    help = "Whoever wrote this plugin needs to write a damn help text ffs"
    cmd = None
    client = None
    channel = None

    def from_admin(self, message):
        for role in message.author.roles:
            if role.name == "admin":
                return True

        return False

    @asyncio.coroutine
    def on_ready(self):
        pass

    @asyncio.coroutine
    def on_command(self, message):
        pass

    @asyncio.coroutine
    def on_message(self, message, history):
        reply = None
        for handler in self.handlers.keys():
            match = handler.search(message.content)
            if match:
                reply = yield from self.handlers[handler](message, match)
                if reply:
                    break

        if reply is None:
            for proc in self.processors:
                reply = yield from proc(message)
                if reply:
                    break

        if reply:
            yield from message.channel.send(reply)

    @asyncio.coroutine
    def on_tick(self):
        pass

    @asyncio.coroutine
    def on_member_update(self, old, member):
        pass

    @asyncio.coroutine
    def get_jabberzac_name(self, member):
        pass

    @asyncio.coroutine
    def get_channel(self, name, server_name=""):
        for server in self.client.guilds:
            if server_name != "" and server.name != server_name:
                continue
            for channel in server.channels:
                if channel.name == name:
                    return channel

    def get_member(self,name):
        for server in self.client.guilds:
            for member in server.members:
                if member.name == name or member.nick == name:
                    return member

    @asyncio.coroutine
    def get_plugin(self, name):
        for plugin in self.plugins:
            if plugin.name == name:
                return plugin

    def chance(self, chance):
        """chance should be a dictionary with the keys being a number like 0.25
            and the value a string to return, the keys should sum to a maximum
            of <= 1.0"""
        random.seed()
        rnd = random.random()
        t = 0
        for message in chance.keys():
            c = chance[message];
            m = t
            t = t + c
            if rnd < t and rnd >= m:
                return message
        return None

    def find_paragraph(self, node):
        if (node.localName == 'p'):
            return node
        if (node.localName == 'table'):
            return None
        for child in node.childNodes:
            paragraph = self.findParagraph(child)
            if paragraph:
                return paragraph

    def add_handler(self, phrases, callback):
        for phrase in phrases:
            self.handlers[re.compile(phrase, re.IGNORECASE)] = callback

    def add_processor(self, callback):
        self.processors.append(callback)

class PersistentPlugin(Plugin):
    persist = []

    @asyncio.coroutine
    def save(self):
        coll = store['plugins']
        data = yield from coll.find_one({'plugin': self.__class__.__name__})
        if not data:
            data = {'plugin':self.__class__.__name__}
        for name in self.persist:
            val = getattr(self,name)
            data[name] = val
        yield from coll.update_one({'plugin': self.__class__.__name__},{'$set': data})

    @asyncio.coroutine
    def load(self):
        coll = store['plugins']
        data = yield from coll.find_one({'plugin': self.__class__.__name__})
        if data:
            for name in self.persist:
                try:
                    val = data[name]
                except:
                    continue
                setattr(self, name, val)

class TimedPersistentPlugin(Plugin):
    persist = []
    dateformat = "%Y%m%d%H" #Default: aggregate data hourly
    current = ""

    @asyncio.coroutine
    def save(self):
        coll = store[self.__class__.__name__]
        data = yield from coll.find_one({'date': datetime.now().strftime(self.dateformat)})
        if not data:
            data = {'date': datetime.now().strftime(self.dateformat)}
        for name in self.persist:
            val = getattr(self, name)
            data[name] = val
        yield from coll.update_one({'date': datetime.now().strftime(self.dateformat)},{"$set":data})

    @asyncio.coroutine
    def load(self):
        coll = store[self.__class__.__name__]
        data = yield from coll.find_one({'date': datetime.now().strftime(self.dateformat)})
        if data:
            for name in self.persist:
                try:
                    val = data[name]
                except:
                    continue
                setattr(self, name, val)

    @asyncio.coroutine
    def get_data_for(self, attr, d):
        coll = store[self.__class__.__name__]
        data = yield from coll.find_one({'date': d.strftime(self.dateformat)})
        if data:
            return data[attr]
        return None

    @gen.coroutine
    def get_data_for_gen(self, attr, d):
        coll = tornado_store[self.__class__.__name__]
        data = yield coll.find_one({'date': d.strftime(self.dateformat)})
        if data:
            return data[attr]
        return None

    @asyncio.coroutine
    def map_reduce(self, map, reduce, partdate=None):
        coll = store[self.__class__.__name__]
        if partdate:
            data = yield from coll.inline_map_reduce(map, reduce, query={'date': {'$regex': '^' + partdate}})
        else:
            data = yield from coll.inline_map_reduce(map, reduce)
        return data

    @gen.coroutine
    def map_reduce_gen(self, map, reduce, partdate=None):
        coll = tornado_store[self.__class__.__name__]
        if partdate:
            data = yield coll.inline_map_reduce(map, reduce, query={'date': {'$regex': '^' + partdate}})
        else:
            data = yield coll.inline_map_reduce(map, reduce)
        return data

    @asyncio.coroutine
    def on_system_tick(self):
        d = datetime.now().strftime(self.dateformat)
        if self.current != d:
            self.current = d
            for name in self.persist:
                val = getattr(self, name)
                if isinstance(val,dict):
                    setattr(self, name, {})
                if isinstance(val,list):
                    setattr(self, name, [])
                if isinstance(val,int):
                    setattr(self, name, 0)
                if isinstance(val,str):
                    setattr(self, name, "")
