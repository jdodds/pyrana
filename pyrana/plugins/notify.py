import pynotify
pynotify.init("Basics")

from feather import Plugin

class Notify(Plugin):
    listeners = set(['songloaded'])
    messengers = set()

    def run(self):
        message_funcs = {
            'SHUTDOWN' : self.shutdown,
            'songloaded' : self.handle_songloaded}

        while self.alive:
            message, payload = self.listener.get()
            message_funcs[message](payload)

    def handle_songloaded(self, payload):
        msg = "Playing: %s" % payload
        notification = pynotify.Notification("Pyrana", msg)
        notification.show()

