import pyglet
from feather import Plugin

class PygletPlayer(Plugin):
    listeners = set(['songloaded', 'pause', 'skipsong', 'skipalbum'])
    messengers = set(['songstart', 'songpause', 'songend', 'songresume'])
    name = 'PygletPlayer'

    def run(self):
        pyglet.options['audio'] = ('alsa', 'directsound', 'openal', 'silent')
        pyglet.options['debug_media'] = True
        pyglet.app.run()

        message_funcs = {
            'songloaded': self.handle_songloaded,
            'pause' : self.handle_pause,
            'skipsong' : self.handle_skipsong,
            'skipalbum' : self.handle_skipalbum,
            'SHUTDOWN' : self.shutdown}
        
        while self.runnable:
            message, payload = self.listener.get()
            message_funcs[message](payload)        

    def handle_songloaded(self, payload):
        try:
            song = pyglet.media.load(payload)
        except pyglet.media.MediaException:
            print 'unsupported file %s' % payload
        else:
            self.playing = True
            if self.player:
                self.player.queue(payload)
                self.player.next()
            else:
                self.player = song.play()
                self.player.volume = 1.0
                self.player.set_handler('on_eos', self.on_eos)
            self.send('songstart', payload)

    def handle_pause(self, payload=None):
        if self.playing:
            self.player.pause()
            self.playing = False
            self.send('songpause')
        else:
            self.player.play()
            self.playing = True
            self.send('songresume')

    def handle_skipsong(self, payload=None):
        self.player.pause()

    def handle_skipalbum(self, payload=None):
        self.player.pause()

    def on_eos(self):
        self.send('songend')
        
            

