# dungarmatic-discord

## How to dev
1. Install Mongo DB Community edition https://docs.mongodb.com/manual/tutorial/install-mongodb-on-ubuntu/
1. Clone this repo somewhere
1. cd to the folder
1. `python3 -m pip install -r requirements.txt`
1. Set environment variable with a Discord bot key (ask astat for it): `export DISCORD_KEY=blah`
1. `python3 dungarmatic.py`
1. Please keep all your testing to the 'dungarmatic-test' channel so as not to spam everyone, if you need access to it ask astat
1. You can have multiple Dungarmatics on the server (ie the main one and your dev one), just note that the normal Dungar might also respond to your commands

## How to make a basic non-persistent plugin
Here's how to create the most basic type of plugin that does not need to persist anything to the db and responds to !command

Create a .py file in `plugins` and they will automatically be loaded on startup
```python
from lib import Plugin
import asyncio

class MyPlugin(Plugin):
    cmd = "command"       #the command to respond to
    help = "Does a thing" #help text when people say !help

    @asyncio.coroutine
    def on_command(self, message):
      print message.content                             #print the whole message, split on space or whatever to get params
      print message.author.name                         #print the author's name
      message.channel.send("you triggered my command!") #send a reply to the originating channel
      message.author.send("hello fren")                 #send a dm to the author      
```

## How to make a plugin that runs on every message
Here's how to create one that doesnt respond to !commands but instead can run on every single message thats sent (in any channel, for example z0r chains)

```python
from lib import Plugin
import asyncio

class MyPlugin(Plugin):
    
    @asyncio.coroutine
    def on_message(self, message, history):
      print history[1]                                  #print the message that came before this one (up to 30 messages)
      print message.content                             #print the whole message, split on space or whatever to get params
      print message.author.name                         #print the author's name
      message.channel.send("you said a thing!")         #send a reply to the originating channel
      message.author.send("hello fren")                 #send a dm to the author
```

## Persistent plugins
There are two types of persistent plugins; normal and timed. 

### Normal
```python
from lib import PersistentPlugin
import asyncio

class MyPlugin(PersistentPlugin):
    persist = ['data']  #A list of class param names to persist
    data = {}           #your data

    @asyncio.coroutine
    def on_ready(self):
        print self.data             #print the stored data
        self.data = {"blah":"hi"}   #set the data
```

This plugin will then automatically persist `self.data` to mongo and re-populate it from the db on startup

### Timed (Advanced)
```python
from lib import TimedPersistentPlugin
import asyncio

class MyPlugin(TimedPersistentPlugin):
    persist = ['data']  #A list of class param names to persist
    data = {}           #your data

    @asyncio.coroutine
    def on_tick(self):
        #this method will be called every 30 seconds (considered a "tick")
        print self.data             #print the stored data
        self.data = {"blah":"hi"}   #set the data
```

This plugin will then automatically persist `self.data` but with a timestamp attached. You can then use map/reduce to generate sums, graphs or whatever. See the MostPlayedPlugin for an example.
