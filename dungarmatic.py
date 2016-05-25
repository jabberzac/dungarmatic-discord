import discord, inspect, sys
import asyncio
from plugins import *
from lib import Plugin

try:
    import settings
except:
    print('No settings.py found. try: cp example_settings.py settings.py')
    exit()


client = discord.Client()

channel = None

loaded_plugins = []

for name, obj in inspect.getmembers(sys.modules[__name__]):
    for n, o in inspect.getmembers(obj):
        if inspect.isclass(o) and issubclass(o,Plugin) and o != Plugin:
            print('Loading Plugin: ' + o.__name__)
            plug = o()
            plug.client = client
            loaded_plugins.append(plug)

@client.event
@asyncio.coroutine
def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

    for c in client.get_all_channels():
        channel = c

    for plugin in loaded_plugins:
        plugin.channel = c
        yield from plugin.on_ready()



@client.event
@asyncio.coroutine
def on_member_update(old,member):
    for plugin in loaded_plugins:
        yield from plugin.on_member_update(old,member)

@client.event
@asyncio.coroutine
def on_message(message):
    for plugin in loaded_plugins:
        yield from plugin.on_message(message)

    if message.content.startswith('!help'):
        m = "Available commands: \n\n"
        for plugin in loaded_plugins:
            if plugin.cmd:
                m += "!" + plugin.cmd + ": " + plugin.help + "\n"
        yield from client.send_message(message.channel, m)

    elif message.content.startswith('!'):
        cmd = message.content[1:]
        for plugin in loaded_plugins:
            if plugin.cmd and plugin.cmd == cmd:
                yield from plugin.on_command(message)

client.run(settings.token)
