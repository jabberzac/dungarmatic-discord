from lib import TimedPersistentPlugin
import asyncio,re,time,traceback,urllib

class ImagesPlugin(TimedPersistentPlugin):
    disabled=True
    persist = ['images']
    dateformat = "%Y%m%d"

    images = {}

    @asyncio.coroutine
    def on_message(self, message, history):
        for attach in message.attachments:
            yield from self.add_image(attach['url'],message.channel.id)

        m = message.content

        regex = r"https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)"
        matches = re.finditer(regex, m, re.MULTILINE)

        for matchNum, match in enumerate(matches):
            url = ''.join(map(str,match.groups()))
            if url.endswith(".png") or url.endswith(".jpg") or url.endswith(".jpeg") or url.endswith(".gif") or url.endswith(".gifv"):
                yield from self.add_image(url, message.channel.id)

    @asyncio.coroutine
    def add_image(self,url,id):
        filename = str(time.time())
        ext = url.split(".")[-1:][0]
        print(filename + "." + ext)
        print(url)

        urlopen = urllib.request.urlopen
        Request = urllib.request.Request
        txheaders = {'User-agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'}
        try:
            req = Request(url, None, txheaders)
            handle = urlopen(req)
        except:
            traceback.print_exc()
        finally:
            CHUNK = 16 * 1024
            with open("static/upload/" + filename+"."+ext, 'wb') as f:
                while True:
                    chunk = handle.read(CHUNK)
                    if not chunk: break
                    f.write(chunk)

            if id not in self.images:
                self.images[id] = []

            if url not in self.images[id]:
                self.images[id].append(filename + "." + ext)
