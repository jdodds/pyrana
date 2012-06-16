import smart_notify
from feather import Plugin

class Notify(Plugin):
    listeners = set(['songloaded', 'songresume'])
    messengers = set()

    def pre_run(self):
        self.currently_playing = ''

    def songloaded(self, payload):
        self.currently_playing = payload
        smart_notify.notify('playing', payload, 'Pyrana')

    def songresume(self, payload):
        smart_notify.notify('playing', self.currently_playing, 'Pyrana')
