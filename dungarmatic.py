import discord, inspect, sys, os
import asyncio
from plugins import *
from lib import Plugin,PersistentPlugin


client = discord.Client()

channel = None

loaded_plugins = []

for name, obj in inspect.getmembers(sys.modules[__name__]):
    for n, o in inspect.getmembers(obj):
        if inspect.isclass(o) and issubclass(o,Plugin) and o != Plugin and o != PersistentPlugin:
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
        break

    for plugin in loaded_plugins:
        plugin.channel = channel
        if issubclass(type(plugin),PersistentPlugin):
            yield from plugin.load()
        yield from plugin.on_ready()

    while True:
        yield from asyncio.sleep(30)
        for plugin in loaded_plugins:
            if issubclass(type(plugin), PersistentPlugin):
                yield from plugin.save()
            yield from plugin.on_tick()


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
        yield from client.send_message(message.channel, m)

    elif message.content.startswith('!'):
        cmd = message.content[1:]
        for plugin in loaded_plugins:
            if plugin.cmd and plugin.cmd == cmd:
                yield from plugin.on_command(message)

print("Connecting to server")
client.run(os.environ.get('DISCORD_TOKEN',''))
