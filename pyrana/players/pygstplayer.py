import pygst
pygst.require("0.10")
import gst, gobject

from feather import Plugin

class PyGST(Plugin):
    """A player based on gstreamer"""

    listeners = set(['songloaded', 'pause', 'skipsong', 'skipalbum'])
    messengers = set(['songstart', 'songpause', 'songend', 'songresume'])

    def run(self):
        gobject.threads_init()
        self.player = gst.element_factory_make("playbin2", "player")
        fakesink = gst.element_factory_make('fakesink', 'fakesink')
        self.player.set_property('video-sink', fakesink)
        self.playing = False
        self.player.connect('about-to-finish', self.on_eos)

        message_funcs = {
            'APP_START' : self.handle_APP_START,
            'songloaded' : self.handle_songloaded,
            'pause' : self.handle_pause,
            'skipsong' : self.stop,
            'skipalbum' : self.stop,
            'SHUTDOWN' : self.shutdown}

        first = True
        while self.alive:
            message, payload = self.listener.get()
            message_funcs[message](payload)

    def on_eos(self, bus=None, msg=None):
        self.stop()
        self.send('songend')
        
    def stop(self, payload=None):
        self.player.set_state(gst.STATE_NULL)
        self.player.set_state(gst.STATE_READY)
        self.playing = False

    def handle_songloaded(self, songpath):
        self.player.set_property('uri', 'file://%s' % songpath)
        self.player.set_state(gst.STATE_PLAYING)
        self.playing = True
        self.send('songstart', songpath)

    def handle_pause(self, payload):
        if self.playing:
            self.player.set_state(gst.STATE_PAUSED)
            self.playing = False
            self.send('songpause')
        else:
            self.player.set_state(gst.STATE_PLAYING)
            self.playing = True
            self.send('songresume')

        
