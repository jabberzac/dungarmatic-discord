import asyncio,json,os
from datetime import date, timedelta
import motor.motor_asyncio
from simplekv.fs import FilesystemStore

MONGODB_URI = os.environ.get('MONGODB_URI','')

store = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URI)['heroku_bj2w4pbb']

class Plugin:
    help = "Whoever wrote this plugin needs to write a damn help text ffs"
    cmd = None
    client = None
    channel = None

    @asyncio.coroutine
    def on_ready(self):
        pass

    @asyncio.coroutine
    def on_command(self, message):
        pass

    @asyncio.coroutine
    def on_message(self, message, history):
        pass

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
    def get_channel(self, name):
        for server in self.client.servers:
            for channel in server.channels:
                if channel.name == name:
                    return channel

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
        yield from coll.save(data)

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

    @asyncio.coroutine
    def save(self):
        coll = store[self.__class__.__name__]
        data = yield from coll.find_one({'date': date.today().isoformat()})
        if not data:
            data = {'plugin': self.__class__.__name__}
        for name in self.persist:
            val = getattr(self, name)
            data[name] = val
        yield from coll.save(data)

    @asyncio.coroutine
    def load(self):
        coll = store[self.__class__.__name__]
        data = yield from coll.find_one({'date': date.today().isoformat()})
        if data:
            for name in self.persist:
                try:
                    val = data[name]
                except:
                    continue
                setattr(self, name, val)

    def sum_week(self, attr):
        coll = store[self.__class__.__name__]
        ret = {}
        d = date.today() - timedelta(days=7)
        for x in range(1,7):
            data = yield from coll.find_one({'date': date.today().isoformat()})
            for k,v in data[attr].items():
                if isinstance(v,int):
                    if k not in ret:
                        ret[k] = v
                    else:
                        ret[k] += v

