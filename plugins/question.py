from lib import Plugin
import asyncio,urllib,traceback,re,xml
import xml.etree.ElementTree as ET
import wikipedia

#ask a stupid question, get a stupid answer
class QuestionPlugin(Plugin):
    @asyncio.coroutine
    def on_ready(self):
        self.tome = r"^<@!" + str(self.client.user.id) + ">\s*"
        self.add_handler([self.tome + r".*\?"], self.handler_question)

    @asyncio.coroutine
    def handler_question(self, mess, match):
        """Ask a stupid question, get a stupid answer"""
        text = mess.content
        tome = r""

        # What is?
        regex = self.tome + self.lang.gettext("REGEX_WHAT_IS")
        regex = re.compile(regex, re.IGNORECASE)
        m = regex.search(text)
        if m:
            phrase = m.group("phrase")
            reply = self.get_description(phrase)
            if reply:
                return reply

        #something or something else?
        regex = self.tome + self.lang.gettext("REGEX_OPTIONS")
        regex = re.compile(regex, re.IGNORECASE)
        m = regex.search(text)
        if m:
            return self.handler_options(mess, m)

        #fallback: 8 ball
        return self.chance({self.bot_8ball(mess, ""): 0.9,
                                     self.bot_goonball(mess, ""): 0.1})

    def handler_options(self, mess, match):
        """[img-timeline]"""
        options = match.group('options')
        options = re.split(self.lang.gettext("REGEX_OR"), options)
        choice = {'checkbox, voted all': 0.005,
                  "not checkbox, didn't vote": 0.005}
        for option in options:
            choice[option] = 0.99 / len(options)
        return self.chance(choice)

    def bot_8ball(self, mess, args):
        """The magic 8 ball"""
        chance = {self.lang.gettext('As I see it, yes'): 0.05,
                  self.lang.gettext('Ask again later'): 0.05,
                  self.lang.gettext('Better not tell you now'): 0.05,
                  self.lang.gettext('Cannot predict now'): 0.05,
                  self.lang.gettext('Concentrate and ask again'): 0.05,
                  self.lang.gettext('Don\'t count on it'): 0.05,
                  self.lang.gettext('It is certain'): 0.05,
                  self.lang.gettext('It is decidedly so'): 0.05,
                  self.lang.gettext('Most likely'): 0.05,
                  self.lang.gettext('My reply is no'): 0.05,
                  self.lang.gettext('My sources say no'): 0.05,
                  self.lang.gettext('Outlook good'): 0.05,
                  self.lang.gettext('Outlook not so good'): 0.05,
                  self.lang.gettext('Reply hazy, try again'): 0.05,
                  self.lang.gettext('Signs point to yes'): 0.05,
                  self.lang.gettext('Very doubtful'): 0.05,
                  self.lang.gettext('Without a doubt'): 0.05,
                  self.lang.gettext('Yes'): 0.05,
                  self.lang.gettext('Yes - definitely'): 0.05,
                  self.lang.gettext('You may rely on it'): 0.05}
        return self.chance(chance)

    def bot_goonball(self, mess, args):
        """The magic goon ball"""
        chance = {self.lang.gettext('As I see it, yes. Furthermore,'): 0.05,
                  self.lang.gettext('Ask again when your daughter is legal'): 0.05,
                  self.lang.gettext('Can\'t talk, deadtear will ban me'): 0.05,
                  self.lang.gettext('Can\'t talk, solo will ban me'): 0.05,
                  self.lang.gettext('Can\'t talk, lux will pink text me'): 0.05,
                  self.lang.gettext('Concentrate and ask again faggot'): 0.05,
                  self.lang.gettext('My sources say: "You are a faggot"'): 0.05,
                  self.lang.gettext('Do fatties like ham?'): 0.05,
                  self.lang.gettext('Do fatties like candy?'): 0.05,
                  self.lang.gettext('About a likely as the forums going down. Again.'): 0.05,
                  self.lang.gettext('My reply is rofl'): 0.05,
                  self.lang.gettext('My sources say send Urcher 1B ISK for an answer'): 0.05,
                  self.lang.gettext('Outlook better than thunderbird'): 0.05,
                  self.lang.gettext('Outlook not so good, mlyp'): 0.05,
                  self.lang.gettext('Reply hazy, kill yourself'): 0.05,
                  self.lang.gettext(
                      'Signs point to your mothers house, because that is the worlds most common destination :iceburn:'): 0.05,
                  self.lang.gettext('Only if CCP can keep the servers going for 24 *consecutive* hours'): 0.05,
                  self.lang.gettext('Only if Solo can keep the servers going for 24 *consecutive* hours'): 0.05,
                  self.lang.gettext('no u'): 0.05,
                  self.lang.gettext('Yes - faggot'): 0.05,
                  self.lang.gettext('Cute question. ISK sent'): 0.05}
        return self.chance(chance)

    @asyncio.coroutine
    def get_description(self, phrase):
        """Gets a description from wikipedia"""
        if phrase == "love":
            return "baby don't hurt me"
        if phrase == "the meaning of life, the universe and everything" or phrase == "the meaning of life" or phrase == "the meaning of life the universe and everything":
            return self.chance(
                {"42": 0.9,
                '420': 0.1})
        if phrase == "the air speed velocity of an unladen swallow":
            return "what do you mean, an African or European Swallow?"
        if phrase == 'best in life' or phrase == 'the best in life':
            return self.chance(
                {'To crush your enemies, see them driven before you, and to hear the lamentation of their women': 0.9,
                 'To crush your biscuits, see them dunked in your tea, and hear the conversation of your auntie': 0.1})


        txheaders = {'User-agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'}
        try:
            summary = wikipedia.summary(phrase, sentences=4)
        except wikipedia.exceptions.PageError:
            traceback.print_exc()
            return "No idea, why dont you google it, fuck.. http://www.google.com/search?q=" + urllib.parse.quote_plus(phrase)
        except:
            traceback.print_exc()
            return "No idea, why dont you google it, fuck.. http://www.google.com/search?q=" + urllib.parse.quote_plus(phrase)
        else:
            return summary
