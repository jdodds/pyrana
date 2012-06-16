import smart_notify
from feather import Plugin

class Notify(Plugin):
    listeners = set(['songloaded', 'songresume', 'show_playing'])
    messengers = set()

    def pre_run(self):
        self.currently_playing = 'Nothing'

    def songloaded(self, payload):
        self.currently_playing = payload
        smart_notify.notify('playing', payload, 'Pyrana')

    def songresume(self, payload):
        smart_notify.notify('playing', self.currently_playing, 'Pyrana')

    def show_playing(self, payload):
        self.songresume(payload)
