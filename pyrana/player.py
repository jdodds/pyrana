import pygst
pygst.require("0.10") # pygst requires us to call this before importing gst
import gst


class PyranaPlayer(object):

    """ An abstraction layer on top of our actual music player. """

    def __init__(self, helper):
        self.helper = helper

    def start(self):
        self.player = gst.element_factory_make("playbin2", "player")

        bus = self.player.get_bus()
        bus.add_signal_watch()
        bus.enable_sync_message_emission()
        bus.connect('message', self.on_message)

    def on_message(self, bus, msg):
        if msg.type == gst.MESSAGE_EOS:
            self.helper.end_of_song()
        elif msg.type == gst.MESSAGE_ERROR:
            raise Exception(msg)

    def stop(self):
        self.player.set_state(gst.STATE_NULL)

    @property
    def song(self):
        return self.song

    @song.setter
    def song(self, song):
        self.player.set_property('uri', 'file://%s' % song)

    def play(self):
        self.player.set_state(gst.STATE_PLAYING)

    def pause(self):
        self.player.set_state(gst.STATE_PAUSED)
