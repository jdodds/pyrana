import pygst
pygst.require("0.10")
import gst, gobject

from feather import Plugin

class PyGST(Plugin):
    """A player based on gstreamer"""

    listeners = set(['APP_START', 'songloaded', 'pause', 'skipsong', 'skipalbum'])
    messengers = set(['songstart', 'songpause', 'songend', 'songresume'])

    def run(self):
        message_funcs = {
            'APP_START' : self.handle_APP_START,
            'songloaded' : self.handle_songloaded,
            'pause' : self.handle_pause,
            'skipsong' : self.on_eos,
            'skipalbum' : self.on_eos,
            'SHUTDOWN' : self.shutdown}

        while self.alive:
            message, payload = self.listener.get()
            message_funcs[message](payload)

    def on_eos(self, bus=None, msg=None):
        print 'in eos %s %s' % (bus, msg)
        self.player.set_state(gst.STATE_NULL)
        self.playing = False
        self.send('songend')

    def handle_APP_START(self, payload):
        self.player = gst.element_factory_make("playbin2", "player")
        self.playing = False
        
        self.bus = self.player.get_bus()
        self.bus.add_signal_watch()
        self.bus.enable_sync_message_emission()
        def on_eos():
            print 'eos non self'
        self.bus.connect('message::eos', self.on_eos)
        self.bus.connect('message::eos', on_eos)

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

        
