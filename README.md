# dungarmatic-discord

## How to dev
1. Install Mongo DB Community edition https://docs.mongodb.com/manual/tutorial/install-mongodb-on-ubuntu/
1. Clone this repo somewhere
1. cd to the folder
1. `python3 -m pip install -r requirements.txt`
1. Set environment variable with a Discord bot token, it is pinned in the `dunagrmatic-test` channel, ask astat for access to this channel if you are not admin
1. `python3 dungarmatic.py`
1. Please keep all your testing to the 'dungarmatic-test' channel so as not to spam everyone
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
      yield from message.channel.send("you triggered my command!") #send a reply to the originating channel
      yield from message.author.send("hello fren")                 #send a dm to the author      
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
      yield from message.channel.send("you said a thing!")         #send a reply to the originating channel
      yield from message.author.send("hello fren")                 #send a dm to the author
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

## Events
Override these methods in your plugin to respond to events. You must decorate these with `@asyncio.coroutine` because dungar is asynchronous.

### on_ready
Is called when your plugin is first loaded, after persistent data is loaded, in case you need to set anything up or cache stuff
```python
    @asyncio.coroutine
    def on_ready(self):
        #do stuff here
```

### on_command
Is called when someone says your command (set by `command = "blah"` in your plugin)
```python
    @asyncio.coroutine
    def on_command(self, message):
        print message.content
```

### on_message
Is called when anyone says anything, including dungar himself
```python
    @asyncio.coroutine
    def on_message(self, message, history):
        if message.author == self.client.user:
            print "this message was sent by dungar himself"
        print message.content       #the message text
        print message.author.name   #Who posted it
        print history               #A list of the last 30 messages in that channel
```

### on_tick
Is called every 30 seconds (a 'tick')
```python
    @asyncio.coroutine
    def on_tick(self):
        #do stuff
```

### on_member_update
Is called every time a member changes (ie what they are playing, or joining a channel, etc)
```python
    @asyncio.coroutine
    def on_member_update(self, old, member):
        #old = the member before they updated
        #member = the member after they updated
```

## Helper functions
The following can all be accessed within a plugin using self.<method> to automate some useful tasks

### `is_admin = self.from_admin(message)`
Returns true if the provided message came from someone with admin permissions

### `channel = self.get_channel(name)`
Returns a particular channel by name (you can then call `channel.send` to send to that specific channel)

### `member = self.get_member(name)`
Returns a particular user by name (you can then call `member.send` to send to that specific person)

### `plugin = self.get_plugin(name)`
Returns loaded reference to another plugin, in case you need your plugins to talk to each other

### `tweets = yield from self.get_tweets(screen_name)`
Returns the most recent 20 tweets posted by anyone on twitter. You must yield this so it doesnt block while contacting twitter.

More coming soon...

