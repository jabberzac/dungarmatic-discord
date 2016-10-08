import asyncio,json,os
from datetime import datetime, timedelta
import motor.motor_asyncio
from simplekv.fs import FilesystemStore

MONGODB_URI = os.environ.get('MONGODB_URI','')

store = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URI)['dungarmatic']

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
        yield from coll.save(data)

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

    @asyncio.coroutine
    def map_reduce(self, map, reduce, partdate):
        coll = store[self.__class__.__name__]
        data = yield from coll.inline_map_reduce(map,reduce,query={'date':{'$regex':'^'+partdate}})
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