import discord, inspect, sys, os, json
import asyncio, threading
import gettext
from plugins import *
from lib import Plugin,PersistentPlugin,TimedPersistentPlugin

import tornado.ioloop
import tornado.web
from tornado import gen

client = discord.Client()

channel = None

loaded_plugins = []
loaded_plugin_names = []

for name, obj in inspect.getmembers(sys.modules[__name__]):
    for n, o in inspect.getmembers(obj):
        if inspect.isclass(o) and issubclass(o,Plugin) and o != Plugin and o != PersistentPlugin and o != TimedPersistentPlugin:
            print('Loading Plugin: ' + o.__name__)
            plug = o()
            if not plug.disabled:
                plug.client = client
                plug.plugins = loaded_plugins
                plug.name = o.__name__
                plug.loaded_plugins = loaded_plugin_names
                loaded_plugins.append(plug)
                loaded_plugin_names.append(o.__name__)

@client.event
@asyncio.coroutine
def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

    lang_en = gettext.translation('dungarmatic', '.', languages=['en'])

    for c in client.get_all_channels():
        channel = c
        break

    for plugin in loaded_plugins:
        plugin.lang = lang_en
        plugin.channel = channel
        plugin.handlers = {}
        plugin.processors = []
        if issubclass(type(plugin),PersistentPlugin):
            yield from plugin.load()
        yield from plugin.on_ready()

    while True:
        for plugin in loaded_plugins:
            if issubclass(type(plugin), PersistentPlugin):
                yield from plugin.save()
            if issubclass(type(plugin), TimedPersistentPlugin):
                yield from plugin.on_system_tick()
                yield from plugin.save()
            yield from plugin.on_tick()
        yield from asyncio.sleep(30)


@client.event
@asyncio.coroutine
def on_member_update(old,member):
    for plugin in loaded_plugins:
        yield from plugin.on_member_update(old,member)

history = {}

@client.event
@asyncio.coroutine
def on_message(message):
    if message.channel.id not in history:
        history[message.channel.id] = []

    history[message.channel.id].insert(0, message.content)
    if len(history[message.channel.id]) > 30:
        history[message.channel.id].pop()

    if message.author == client.user:
        return

    for plugin in loaded_plugins:
        yield from plugin.on_message(message,history[message.channel.id])

    if message.content.startswith('!help'):
        m = "Available commands: \n\n"
        for plugin in loaded_plugins:
            if plugin.cmd:
                m += "!" + plugin.cmd + ": " + plugin.help + "\n"
        yield from message.channel.send(m)

    elif message.content.startswith('!'):
        cmd = message.content[1:]
        for plugin in loaded_plugins:
            if plugin.cmd and cmd.startswith(plugin.cmd):
                yield from plugin.on_command(message)
                if issubclass(type(plugin), PersistentPlugin):
                    yield from plugin.save()


#Web client (Tornado)
class MainHandler(tornado.web.RequestHandler):
    def get(self):
        html = open('templates/index.html', encoding='utf-8')
        self.write(html.read())

class ApiHandler(tornado.web.RequestHandler):
    @gen.coroutine
    def get(self,path):
        for plugin in loaded_plugins:
            if(hasattr(plugin,"api_"+path)):
                method = getattr(plugin,"api_"+path)
                data = yield method()
                self.set_header('Content-Type', 'application/json')
                self.write(json.dumps(data))
                return

        raise(tornado.web.HTTPError(404))

class FileHandler(tornado.web.StaticFileHandler):
    def parse_url_path(self, url_path):
        if not url_path or url_path.endswith('/'):
            url_path = url_path + 'index.html'
        return url_path

def start_web():
    app = tornado.web.Application([
        (r"/", MainHandler),
        (r"^/api/(.*)", ApiHandler),
        (r"^/static/(.*)", FileHandler, {'path': os.getcwd()+"/static"}),
    ], debug=True)
    port = int(os.environ.get("PORT", 5000))
    print("Starting web server on port " + str(port))
    app.listen(port)
    tornado.ioloop.IOLoop.current().start()

if __name__ == "__main__":

    #t = threading.Thread(target=start_web)
    #t.daemon = True
    #t.start()

    print("Connecting to Discord")
    client.run(os.environ.get('DISCORD_TOKEN',''))
