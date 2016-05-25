import asyncio

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
    def on_message(self, message):
        pass

    @asyncio.coroutine
    def on_member_update(self, old, member):
        pass