import asyncio,json,os
from simplekv.fs import FilesystemStore

try:
    os.mkdir('./dungarmatic.data')
except:
    pass
store = store = FilesystemStore('./dungarmatic.data')

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

class PersistentPlugin(Plugin):
    persist = []

    @asyncio.coroutine
    def save(self):
        for name in self.persist:
            val = json.dumps(getattr(self,name))
            store.put(self.__class__.__name__+'_'+name,val.encode())

    @asyncio.coroutine
    def load(self):
        for name in self.persist:
            try:
                val = store.get(self.__class__.__name__ + '_' + name)
            except:
                continue
            setattr(self, name, json.loads(val.decode()))
